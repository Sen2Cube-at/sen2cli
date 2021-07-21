## TODO(SR) make this proper click config objects
import os
from typing import Final

HOME_PATH: Final[str] = os.path.expanduser("~")
CONFIG_PATH: Final[str] = os.environ.get('IQ_CLI_CONFIG_PATH', f"{HOME_PATH}/.iq-cli")
CONFIG_PATH_TOKENFILE: Final[str] = os.environ.get('IQ_CLI_CONFIG_PATH_TOKENFILE', f"{CONFIG_PATH}/token.json")

LOGGER_CONFIG_FILE: Final[str] = f"{CONFIG_PATH}/logger.ini"

API_BASE_URL: Final[str] = os.environ.get('IQ_API_BASE_URL', "https://api.sen2cube.at/v1")
AUTH_CLIENT_ID: Final[str] = os.environ.get('IQ_AUTH_CLIENT_ID', "iq-web-client")
AUTH_BASE_URL: Final[str] = os.environ.get('IQ_AUTH_BASE_URL',
                                           "https://auth.sen2cube.at/realms/sen2cube-at/protocol/openid-connect")
AUTH_TOKEN_URL: Final[str] = os.environ.get('IQ_AUTH_TOKEN_URL', f"{AUTH_BASE_URL}/token")
AUTH_USER_INFO_URL: Final[str] = os.environ.get('IQ_AUTH_USER_INFO_URL', f"{AUTH_BASE_URL}/userinfo")

DEFAULT_DELIMITER: Final[str] = os.environ.get('IQ_DEFAULT_CSV_DELIMITER', ";")