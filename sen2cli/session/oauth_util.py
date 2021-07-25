import json
import logging
import os
from datetime import datetime
from typing import Final

from oauthlib.oauth2 import InvalidGrantError, LegacyApplicationClient, OAuth2Token, \
  UnauthorizedClientError
from requests import Response
from requests_oauthlib import OAuth2Session

from ..env import AUTH_CLIENT_ID, AUTH_USER_INFO_URL

logger = logging.getLogger(__name__)


def fetch_token(username: str, password: str,
                auth_token_url: str,
                auth_client_id: str,
                ) -> OAuth2Token:
  """
  Get OAuth token from auth_token_url and store in config_path_tokenfile

  :return: OAuth2Token with session information or None if any error
  """
  try:
    client: Final[LegacyApplicationClient] = LegacyApplicationClient(client_id=auth_client_id)

    with OAuth2Session(client=client) as oauth_session:
      token: Final[OAuth2Token] = oauth_session.fetch_token(
        token_url=auth_token_url,
        client_id=auth_client_id,
        username=username,
        password=password
      )
      logger.debug(f"Login successful. Got token: {token}")
      return token

  except UnauthorizedClientError:
    logger.critical(
      f"Authorisation failed for token url {auth_token_url} as client {auth_client_id}.",
      exc_info=True,
    )
  except InvalidGrantError as e:
    logger.critical(f"Login failed. Reason {str(e)}", exc_info=False)
  except Exception:
    logger.critical(
      f"Unknown error on authentication for token url {auth_token_url} as client {auth_client_id}.",
      exc_info=True,
    )


def refresh_token(token: OAuth2Token, auth_token_url: str, auth_client_id: str) -> OAuth2Token:
  try:
    client: Final[LegacyApplicationClient] = LegacyApplicationClient(client_id=auth_client_id)

    with OAuth2Session(client=client, token=token) as oauth_session:
      token: Final[OAuth2Token] = oauth_session.refresh_token(auth_token_url, client_id=auth_client_id)
      logger.debug(f"Got token: {token}")
      logger.info(f"Token refresh successful.")
      return token

  except UnauthorizedClientError:
    logger.critical(
      f"Authorisation failed for token url {auth_token_url} as client {auth_client_id}.",
      exc_info=True,
    )
  except InvalidGrantError as e:
    logger.critical(f"Login failed. Reason {str(e)}", exc_info=False)
  except Exception:
    logger.critical(
      f"Unknown error on authentication for token url {auth_token_url} as client {auth_client_id}.",
      exc_info=True,
    )


def load_token(token_file_path: str) -> OAuth2Token:
  """  Load token from tokenfile.
  :return: OAuth2Token with session information or None if any error
  """
  if os.path.isfile(token_file_path):
    with open(token_file_path, 'r') as tokenfile:
      logger.debug(f'Loading token from {token_file_path}...')
      token_dict: dict = json.load(tokenfile)
      if token_dict is not None and all(
        elem in token_dict.keys() for elem in ['expires_at', 'access_token', 'token_type']):
        token = OAuth2Token(token_dict)
        return token
      else:
        logger.critical("Tokenfile was invalid or empty.")
        return None
  else:
    logger.warning(f'Token file does not exist: {token_file_path}')
    return None


def save_token(token_file_path: str, token: OAuth2Token) -> None:
  ## TODO(SR) make sure this file is set correctly to only be readable by current user
  with open(token_file_path, 'w') as tokenfile:
    json.dump(token, tokenfile)


def load_or_refresh_token(token_file_path: str, auth_token_url: str, auth_client_id: str,
                          save: bool = True) -> OAuth2Token:
  token = load_token(token_file_path)
  if token is not None and len(token) > 0:
    if datetime.now() > datetime.fromtimestamp(token['expires_at']):
      logger.info("Token expired. Trying refresh.")
      token = refresh_token(token, auth_token_url, auth_client_id)
      if save:
        save_token(token_file_path, token)
  return token


def get_user_info(token: OAuth2Token) -> dict:
  """
  Checks if token is still valid.

  :param token: OAuth2Token with session
  :return: User Info
  """
  client: Final[LegacyApplicationClient] = LegacyApplicationClient(client_id=AUTH_CLIENT_ID)
  with OAuth2Session(client=client, token=token) as oauth_session:
    user_info: Response = oauth_session.get(AUTH_USER_INFO_URL)
    if user_info.ok:
      user_info_json: dict = user_info.json()
      return user_info_json
    else:
      return None
