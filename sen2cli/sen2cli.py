# Sen2Commandline Interface
# Simple commandline interface for Sen2Cube backend via JSONApi
import logging
import os.path

import click

from  .__version__ import __version__
from .env import CONFIG_PATH, CONFIG_PATH_TOKENFILE
from .inference import cli as inference_cli
from .session import cli as session_cli
from .utils import configure_logging, s2cli_command_config


@click.group()
@click.option('--tokenfile', help="File that stores the token.",
              envvar="S2C_TOKENFILE",
              show_envvar=True,
              type=click.Path(exists=False, file_okay=True, dir_okay=False, writable=True, readable=True),
              default=CONFIG_PATH_TOKENFILE)
@click.option('--log_file', type=click.Path(dir_okay=False, writable=True),
              help="Write log to this file instead of StdErr.")
@click.option('-v', '--verbose', count=True,
              help="Verbose log output. Can be added up to three times for even more verbosity (WARNING, INFO, DEBUG).")
@s2cli_command_config
def cli(s2cli_command_config, tokenfile, log_file, verbose: int):
  log_level = logging.ERROR
  if verbose >= 3:
    log_level = logging.DEBUG
  elif verbose >= 2:
    log_level = logging.INFO
  elif verbose >= 1:
    log_level = logging.WARNING

  configure_logging(log_file, log_level)
  if not os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)

  s2cli_command_config.tokenfile = tokenfile

@cli.command(help="Prints program version")
def version():
  click.echo(f"{__version__}")

cli.add_command(session_cli.session)
cli.add_command(inference_cli.inference)
