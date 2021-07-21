import logging
from typing import List, Union

from jsonapi_client import Filter, Session
from jsonapi_client.exceptions import DocumentError
from oauthlib.oauth2 import OAuth2Token

from .util import ALLOWED_BEFORE_STATUS
from ..env import API_BASE_URL
from ..utils import filter_string_from_parameter

logger = logging.getLogger(__name__)


def update_inference(token: OAuth2Token,
                     id: Union[int, List, tuple, None] = None,
                     new_status: str = None,
                     ) -> List[int]:
  with Session(API_BASE_URL,
               request_kwargs=dict(
                   headers={'Authorization': f"{token['token_type']} {token['access_token']}"})) as session:
    try:
      id_filter = Filter(f'filter=[{filter_string_from_parameter("id", id)}]')
      logger.critical(id_filter.url_with_modifiers(''))
      inferences = session.get('inference', id_filter)
      logger.info(f"Inferences loaded: {len(inferences.resources)}")
      updated_inferences = []
      for inference in inferences.resources:
        if inference.status in ALLOWED_BEFORE_STATUS[new_status]:
          inference.status = new_status
          inference.commit()
          updated_inferences.append(inference.id)
        else:
          logger.warning(
              f"Could not set new status for inference {inference.id}: {inference.status} -> {new_status} is not allowed.")

      return updated_inferences
    except DocumentError as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    except Exception as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    finally:
      session.close()
