import logging
from typing import List, Union

from jsonapi_client import Filter, Session
from jsonapi_client.exceptions import DocumentError
from oauthlib.oauth2 import OAuth2Token

from .util import ALLOWED_BEFORE_STATUS, DEFAULT_COLUMNS
from ..env import API_BASE_URL
from ..utils import dict_from_resource, filter_string_from_parameter

logger = logging.getLogger(__name__)


def update_inference(token: OAuth2Token,
                     id: Union[int, List, tuple, None] = None,
                     new_status: str = None,
                     dry_run: bool = False
                     ) -> List[dict]:
  with Session(API_BASE_URL,
               request_kwargs=dict(
                   headers={'Authorization': f"{token['token_type']} {token['access_token']}"})) as session:
    try:
      id_filter = Filter(f'filter=[{filter_string_from_parameter("id", id)}]')
      logger.debug(id_filter.url_with_modifiers(''))
      inferences = session.get('inference', id_filter)
      logger.info(f"Inferences loaded: {len(inferences.resources)}")
      updated_inferences = []
      for inference in inferences.resources:
        if inference.status in ALLOWED_BEFORE_STATUS[new_status]:
          inference.status = new_status
          if not dry_run:
            inference.commit()
          else:
            logger.info("Dry run. Skipping commit.")
          updated_inferences.append(inference)
        else:
          logger.warning(
              f"Could not set new status for inference {inference.id}: {inference.status} -> {new_status} is not allowed.")

      return [dict_from_resource(res, DEFAULT_COLUMNS) for res in updated_inferences]
    except DocumentError as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    except Exception as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    finally:
      session.close()
