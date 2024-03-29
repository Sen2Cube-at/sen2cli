# Sen2CLI utility functions
import io
import logging
from csv import DictWriter
from typing import Final, List, Union

from jsonapi_client.resourceobject import ResourceObject

from .env import DEFAULT_DELIMITER

logger = logging.getLogger(__name__)


def configure_logging(log_file: str = None, log_level: int = logging.WARNING) -> None:
  """Configures basic logging.
  Default configuration will output to StrErr on WARNING.
  Args:
    log_file (str): path + filename of logfile. If None, then StdErr will be used
    log_level (int): Log Level. Default: WARNING.
  """
  log_handlers: Final[list] = []

  if log_file:
    log_handlers.append(
        logging.FileHandler(log_file, mode="w")
    )
  else:
    log_handlers.append(
        logging.StreamHandler()  # defaults to strerr
    )

  logging.basicConfig(
      format='%(asctime)s [%(levelname)s] - %(funcName)s:%(lineno)d - %(message)s',
      level=log_level,
      datefmt="%Y-%m-%d %H:%M:%S",
      handlers=log_handlers
  )

def _get_or_none(res: ResourceObject, field_name: str) -> any:
  try:
    return res[field_name]
  except KeyError as e:
    logger.warning(f"Could not find '{field_name}' in Resource. Returning none.")
    return None

def dict_from_resource(res: ResourceObject, columns: List[str]) -> dict:
  resource_id = {'id': res.id}
  ret = {col: _get_or_none(res, col) for col in columns}
  return {**resource_id, **ret}


def csv_from_dictlist(list: List[dict], with_headers: bool = True) -> str:
  if not list is None and len(list) > 0:
    with io.StringIO() as csv_string:
      csv_writer = DictWriter(csv_string, fieldnames=list[0].keys(), delimiter=DEFAULT_DELIMITER)
      if with_headers:
        csv_writer.writeheader()
      csv_writer.writerows(list)
      return csv_string.getvalue()


def filter_string_from_parameter(column: str, value: Union[str, int, List, tuple, None]) -> str:
  if value is None:
    return None
  elif (isinstance(value, List) or isinstance(value, tuple)):
    if len(value) > 0:
      if isinstance(value[0], str):  # we need to quote string values
        fval = ','.join(map(lambda v: f'"{v}"', value))
      else:
        fval = ','.join(map(str, value))
      filter_string = (f'{{"name":"{column}", "op": "in", "val": [{fval}]}}')
      logger.debug(filter_string)
      return filter_string
    else:
      logger.debug(f"List/Tuple was empty")
      return None
  elif isinstance(value, int):
    filter_string = (f'{{"name":"{column}", "op": "in", "val": [{value}]}}')
    logger.debug(filter_string)
    return filter_string
  elif isinstance(value, str):
    filter_string = (f'{{"name":"{column}", "op": "in", "val": ["{value}"]}}')
    logger.debug(filter_string)
    return filter_string
  else:
    logger.error(f"Type not supported: {type(value)}")
    return None
