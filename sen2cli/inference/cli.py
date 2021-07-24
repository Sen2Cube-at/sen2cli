# Sen2CLI inference module click group / commands
import logging
from io import TextIOWrapper

import click

from .create import create_inference
from .get import get_inference
from .update import update_inference
from .util import DEFAULT_COLUMNS, INFERENCE_STATUS
from ..env import AUTH_CLIENT_ID, AUTH_TOKEN_URL, CONFIG_PATH_TOKENFILE
from ..session.oauth_util import load_or_refresh_token
from ..utils import csv_from_dictlist, dict_from_resource

logger = logging.getLogger(__name__)


class InferenceCommandConfig(object):
  def __init__(self):
    self.tokenfile = None


inference_command_config = click \
  .make_pass_decorator(InferenceCommandConfig, ensure=True)


@click.group(help="Start/Stop/List/Delete etc inferences.")
@click.option('--tokenfile', help="File that stores the token.",
              envvar="S2C_TOKENFILE",
              show_envvar=True,
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True),
              default=CONFIG_PATH_TOKENFILE)
@inference_command_config
def inference(inference_command_config, tokenfile):
  inference_command_config.tokenfile = tokenfile
  pass


@inference.command(help="List inferences.")
@click.option('--format', help="Specify output format (CSV, CSV without header, JSON)",
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
@click.option('--raw_modifier',
              help="This will be added to the query string and can be used to build lmore sophisticated filters etc.",
              type=click.STRING)
@inference_command_config
def ls(inference_command_config: InferenceCommandConfig,
       format: str,
       id: int,
       factbase_id: int,
       knowledgebase_id: int,
       status: str,
       sort: str,
       raw_modifier: str):
  """Lists inferences"""
  token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
  if not token is None:
    inferences = get_inference(token, id=id, factbase_id=factbase_id, knowledgebase_id=knowledgebase_id, status=status,
                               sort_by=sort, raw_modifier=raw_modifier)
    resources = [dict_from_resource(res, DEFAULT_COLUMNS) for res in inferences]
    if format == 'csv':
      click.echo(csv_from_dictlist(resources, with_headers=True))
    elif format == 'csv_no_hdr':
      click.echo(csv_from_dictlist(resources, with_headers=False))
    elif format == 'json':
      click.echo(resources)
    else:
      raise

  else:
    click.echo("Token was none")


@inference.command()
@click.option('--id', help="Which inference to rerun.", type=click.INT, multiple=True)
@inference_command_config
def rerun(inference_command_config, id):
  if len(id) == 0:
    click.echo("At least one --id needs to be given.")
  else:
    token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
    if not token is None:
      updated = update_inference(token, id, 'CREATED')
      click.echo(f"Restarted inferences: {updated}.")
    else:
      click.echo("Token was none")


@inference.command()
@click.option('--id', help="Which inference to rerun.", type=click.INT, multiple=True)
@inference_command_config
def abort(inference_command_config, id):
  if len(id) == 0:
    click.echo("At least one --id needs to be given.")
  else:
    token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
    if not token is None:
      updated = update_inference(token, id, 'ABORTED')
      click.echo(f"Aborted inferences: {updated}.")
    else:
      click.echo("Token was none")


@inference.command()
@click.argument('knowledgebase_id', type=click.INT)
@click.argument('factbase_id', type=click.INT)
@click.argument('temporal_subset_start', type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument('temporal_subset_end', type=click.DateTime(formats=['%Y-%m-%d']))
@click.argument('spatial_subset', type=click.File('r'))
@click.option('--description', help="Description of the inference", type=click.STRING)
@inference_command_config
def create(inference_command_config, knowledgebase_id, factbase_id, temporal_subset_start, temporal_subset_end,
           spatial_subset: TextIOWrapper, description):
  token = load_or_refresh_token(inference_command_config.tokenfile, AUTH_TOKEN_URL, AUTH_CLIENT_ID)
  if not token is None:
    geojson = spatial_subset.read().replace("\n", " ")
    created = create_inference(token,
                               factbase_id=factbase_id,
                               knowldegebase_id=knowledgebase_id,
                               temp_range_start=temporal_subset_start,
                               temp_range_end=temporal_subset_end,
                               spatial_subset=geojson,
                               description=description)
    click.echo(f"Created inference: {created}.")
  else:
    click.echo("Token was none")
