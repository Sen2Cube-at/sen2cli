# Sen2CLI session module click group / commands
import json
import logging
from datetime import datetime

import click

from utils import s2cli_command_config
from ..env import AUTH_CLIENT_ID, AUTH_TOKEN_URL, CONFIG_PATH_TOKENFILE

from .oauth_util import fetch_token, get_user_info, load_token, refresh_token, save_token

logger = logging.getLogger(__name__)


# class SessionCommandConfig(object):
#   def __init__(self):
#     self.tokenfile = None
#
#
# session_command_config = click \
#   .make_pass_decorator(SessionCommandConfig, ensure=True)


@click.group(help="Session related commands like 'login'")
@s2cli_command_config
def session(s2cli_command_config, tokenfile):
  s2cli_command_config.tokenfile = tokenfile


@session.command(help="Login with username and password")
@click.option('--username', help="Login with this username", envvar="S2C_USERNAME", prompt=True, show_envvar=True)
@click.option('--password', help="Login with this password", envvar="S2C_PASSWORD", prompt=True, hide_input=True,
              show_envvar=True)
@s2cli_command_config
def login(s2cli_command_config, username, password):
  click.echo(f"Trying to authenticate against {AUTH_TOKEN_URL} with client {AUTH_CLIENT_ID}")
  token = fetch_token(username, password, auth_token_url=AUTH_TOKEN_URL, auth_client_id=AUTH_CLIENT_ID)
  if token is not None:
    expires_at = datetime.fromtimestamp(token['expires_at'])
    click.echo(f"Login successful. Session expires at {expires_at}")
    save_token(s2cli_command_config.tokenfile, token)


@session.command(help="Use saved refresh token to refresh session")
@s2cli_command_config
def refresh(s2cli_command_config):
  token = load_token(s2cli_command_config.tokenfile)
  if token is None:
    click.echo("Could not load session token.")
  else:
    token = refresh_token(token, auth_token_url=AUTH_TOKEN_URL, auth_client_id=AUTH_CLIENT_ID)
    if not token is None:
      expires_at = datetime.fromtimestamp(token['expires_at'])
      click.echo(f"Refresh successful. Session expires at {expires_at}")
      save_token(s2cli_command_config.tokenfile, token)

@session.command(help="Show info for current session")
@s2cli_command_config
def info(s2cli_command_config):
  token = load_token(s2cli_command_config.tokenfile)

  if token is None:
    click.echo("Could not load session token.")
  else:
    expires_at = datetime.fromtimestamp(token['expires_at'])
    refresh_until = datetime.fromtimestamp(token['expires_at'] - token['expires_in'] + token['refresh_expires_in'])
    if datetime.now() > expires_at:
      if (datetime.now() > refresh_until):
        click.echo("Session expired.")
      else:
        click.echo(f"Token expired on: {expires_at}")
        click.echo(f"Refresh until:    {refresh_until}")
    else:
      user_info = get_user_info(token)
      click.echo(f"Logged in as:  {user_info['preferred_username']}")
      click.echo(f"Expires at:    {expires_at}")
      click.echo(f"Refresh until: {refresh_until}")
