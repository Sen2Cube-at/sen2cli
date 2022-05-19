# Sen2CLI inference module click group / commands
import logging
from io import TextIOWrapper
from typing import List, Union

import click

from .create import create_inference
from .delete import delete_inference
from .get import get_inference
from .update import update_inference
from .util import DEFAULT_COLUMNS, INFERENCE_STATUS
from ..env import AUTH_CLIENT_ID, AUTH_TOKEN_URL
from ..session.oauth_util import load_or_refresh_token
from ..utils import csv_from_dictlist, dict_from_resource, S2CliCommandConfig, s2cli_command_config

logger = logging.getLogger(__name__)


def _click_echo_output(output_format: str, resources: List[dict]):
  """Print output to whatever click.echo points in the correct format."""
  if output_format == 'csv':
    click.echo(csv_from_dictlist(resources, with_headers=True))
  elif output_format == 'csv_no_hdr':
    click.echo(csv_from_dictlist(resources, with_headers=False))
  elif output_format == 'json':
    click.echo(resources)
  else:
    raise ValueError(f'Unsupported output_format: {output_format}')

class InferenceCommandConfig(object):
  def __init__(self):
    self.output_format = None
    self.id: Union[int, List[int], tuple, None] = None
    self.factbase_id: Union[int, List[int], tuple, None] = None
    self.knowledgebase_id: Union[int, List[int], tuple, None] = None
    self.status: Union[str, List[str], tuple, None] = None
    self.sort_by: str = None
    self.page_size: int = 30
    self.page_num: int = 1
    self.page_fetch_follows: bool = False
    self.result_count_only: bool = False
    self.raw_modifier: str = None

inference_command_config = click \
  .make_pass_decorator(InferenceCommandConfig, ensure=True)


@click.group(help="Display / create / modify inferences")
@click.option('--output_format', '-f', help="Specify output format (CSV, CSV without header, JSON)",
              type=click.Choice(['csv', 'csv_no_hdr', 'json']), default='csv')
@click.option('--id', help="Filter for inference ID",
              type=click.INT, multiple=True)
@click.option('--factbase_id', help="Filter for factbase ID",
              type=click.INT, multiple=True)
@click.option('--knowledgebase_id', help="Filter for model ID",
              type=click.INT, multiple=True)
@click.option('--status', help="Filter for status",
              type=click.Choice(INFERENCE_STATUS), multiple=True)
@click.option('--sort', help="Columns to sort by. Example: owner,-knowledgebase_id",
              type=click.STRING, default="-id")
@click.option('--page_size', help="Numbers of results to fetch per page. 0 to disable fetch all. --page_number will be ignored. (DEFAULT: 30)",
              type=click.INT, default=30)
@click.option('--page_number', help="Page to fetch. 0 for all pages (in badges of page_size). (DEFAULT: 1)",
              type=click.INT, default=1)
@click.option('--raw_modifier',
              help="This will be added to the query string and can be used to build lmore sophisticated filters etc.",
              type=click.STRING)
@inference_command_config
def inference(inference_command_config: InferenceCommandConfig,
              output_format: str,
              id: int,
              factbase_id: int,
              knowledgebase_id: int,
              status: str,
              sort: str,
              page_number: int,
              page_size: int,
              raw_modifier: str
              ):
  inference_command_config.output_format = output_format

  inference_command_config.id = id
  inference_command_config.factbase_id = factbase_id
  inference_command_config.knowledgebase_id = knowledgebase_id
  inference_command_config.status = status
  inference_command_config.sort_by = sort
  inference_command_config.page_size = page_size
  inference_command_config.page_num = (page_number if page_number > 0 else 1)
  inference_command_config.page_fetch_follows = (page_number <= 0)
  inference_command_config.result_count_only = False
  inference_command_config.raw_modifier = raw_modifier


@inference.command(help="List inferences")
@click.option('--count_only', help="Only returns total number of inferences matching the query. (DEFAULT: False)",
              type=click.BOOL, default=False, is_flag=True)
@s2cli_command_config
@inference_command_config
def ls(inference_command_config: InferenceCommandConfig,
       s2cli_command_config: S2CliCommandConfig,
       count_only: bool
       ):
  """Lists inferences"""
  token = load_or_refresh_token(s2cli_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
  if not token is None:
    inferences = get_inference(token,
                               id=inference_command_config.id,
                               factbase_id=inference_command_config.factbase_id,
                               knowledgebase_id=inference_command_config.knowledgebase_id,
                               status=inference_command_config.status,
                               sort_by=inference_command_config.sort,
                               raw_modifier=inference_command_config.raw_modifier,
                               page_size=inference_command_config.page_size,
                               page_num=inference_command_config.page_num,
                               page_fetch_follows=inference_command_config.page_fetch_follows,
                               result_count_only=count_only)
    if not count_only:
      resources = [dict_from_resource(res, DEFAULT_COLUMNS) for res in inferences]
      _click_echo_output(inference_command_config.output_format, resources)
    else:
      _click_echo_output(inference_command_config.output_format, [{'inference_count': inferences}])
  else:
    click.echo("No active Session or invalid token.")


@inference.command(help="Rerun finished / stopped / failed inferences")
@click.option('--dry-run', help="Will only display the inferences affected by rerun but not schedule them.", type=click.BOOL, default=False, is_flag=True)
@inference_command_config
def rerun(inference_command_config: InferenceCommandConfig,
          dry_run: bool):
  if len(inference_command_config.id) == 0 \
    and len(inference_command_config.factbase_id) == 0 \
    and len(inference_command_config.knowledgebase_id) == 0 \
    and len(inference_command_config.status) == 0:
    click.echo("At least one filter needs to be specified.")
  else:
    token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
    if not token is None:
      updated = update_inference(token, id, factbase_id, knowledgebase_id, status, 'CREATED', dry_run=dry_run)
      _click_echo_output(inference_command_config.output_format, updated)
    else:
      click.echo("No active Session or invalid token.")


@inference.command(help="Abort running / scheduled inferences")
@click.option('--id', help="Which inference to abort.", type=click.INT, multiple=True)
@click.option('--factbase_id', help="Filter for factbase ID",
              type=click.INT, multiple=True)
@click.option('--knowledgebase_id', help="Filter for model ID",
              type=click.INT, multiple=True)
@click.option('--status', help="Filter for status",
              type=click.Choice(INFERENCE_STATUS), multiple=True)
@click.option('--dry-run', help="Will only display the inferences affected by abort but not abort them.", type=click.BOOL, default=False, is_flag=True)
@inference_command_config
def abort(inference_command_config: InferenceCommandConfig,
          id: int,
          factbase_id: int,
          knowledgebase_id: int,
          status: str,
          dry_run: bool):
  if len(id) == 0 and len(factbase_id) == 0 and len(knowledgebase_id) == 0 and len(status) == 0:
    click.echo("At least one filter needs to be specified.")
  else:
    token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
    if not token is None:
      updated = update_inference(token, id, factbase_id, knowledgebase_id, status, 'ABORTED', dry_run=dry_run)
      _click_echo_output(inference_command_config.output_format, updated)
    else:
      click.echo("No active Session or invalid token.")

@inference.command(help="Delete inferences.")
@click.option('--id', help="Which inference to abort.", type=click.INT, multiple=True)
@click.option('--factbase_id', help="Filter for factbase ID",
              type=click.INT, multiple=True)
@click.option('--knowledgebase_id', help="Filter for model ID",
              type=click.INT, multiple=True)
@click.option('--status', help="Filter for status",
              type=click.Choice(INFERENCE_STATUS), multiple=True)
@click.option('--dry-run', help="Will only display the inferences affected by delete but not delete them.", type=click.BOOL, default=False, is_flag=True)
@inference_command_config
def delete(inference_command_config: InferenceCommandConfig,
          id: int,
          factbase_id: int,
          knowledgebase_id: int,
          status: str,
          dry_run: bool):
  if len(id) == 0 and len(factbase_id) == 0 and len(knowledgebase_id) == 0 and len(status) == 0:
    click.echo("At least one filter needs to be specified.")
  else:
    token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
    if not token is None:
      deleted = delete_inference(token, id, factbase_id, knowledgebase_id, status, dry_run=dry_run)
      _click_echo_output(inference_command_config.output_format, deleted)
    else:
      click.echo("No active Session or invalid token.")


@inference.command(help="Create and schedule inference")
@click.argument('knowledgebase_id', type=click.INT)
@click.argument('factbase_id', type=click.INT)
@click.argument('temporal_subset_start', type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument('temporal_subset_end', type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument('spatial_subset', type=click.File('r'))
@click.option('--description', help="Description of the inference", type=click.STRING)
@click.option('--dry-run', help="Will only display the inference but not create it.", type=click.BOOL, default=False, is_flag=True)
@inference_command_config
def create(inference_command_config, knowledgebase_id, factbase_id, temporal_subset_start, temporal_subset_end,
           spatial_subset: TextIOWrapper, description, dry_run: bool):
  token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
  if not token is None:
    geojson = spatial_subset.read().replace("\n", " ")
    created = create_inference(token,
                               factbase_id=factbase_id,
                               knowldegebase_id=knowledgebase_id,
                               temp_range_start=temporal_subset_start,
                               temp_range_end=temporal_subset_end,
                               spatial_subset=geojson,
                               description=description,
                               dry_run=dry_run)
    _click_echo_output(inference_command_config.output_format, [created])
  else:
    click.echo("No active Session or invalid token.")
