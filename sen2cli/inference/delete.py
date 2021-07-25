import logging
from typing import List, Union

from jsonapi_client import Filter, Modifier, Session
from jsonapi_client.exceptions import DocumentError
from oauthlib.oauth2 import OAuth2Token

from .util import ALLOWED_BEFORE_STATUS, DEFAULT_COLUMNS
from ..env import API_BASE_URL
from ..utils import dict_from_resource, filter_string_from_parameter

logger = logging.getLogger(__name__)


def delete_inference(token: OAuth2Token,
                     id: Union[int, List, tuple, None] = None,
                     factbase_id: Union[int, List, tuple, None] = None,
                     knowledgebase_id: Union[int, List, tuple, None] = None,
                     status: Union[str, List, tuple, None] = None,
                     dry_run: bool = False
                     ) -> List[dict]:
  with Session(API_BASE_URL,
               request_kwargs=dict(
                   headers={'Authorization': f"{token['token_type']} {token['access_token']}"})) as session:
    try:
      filter_str_list = ','.join(list(filter(None, [
        filter_string_from_parameter('id', id),
        filter_string_from_parameter('factbase_id', factbase_id),
        filter_string_from_parameter('knowledgebase_id', knowledgebase_id),
        filter_string_from_parameter('status', status)
      ])))
      modifier_list: List[Modifier] = []

      if len(filter_str_list) > 0:
        modifier_list.append(Filter(query_str=f'filter=[{filter_str_list}]'))
      else:
        raise ValueError("At least one filter argument needs to be given.")

      merged_filters = sum(modifier_list, Modifier())

      logger.debug(merged_filters.url_with_modifiers(''))
      inferences = session.get('inference', merged_filters)
      logger.info(f"Inferences loaded: {len(inferences.resources)}")
      deleted_inferences = []
      for inference in inferences.resources:
        if inference.status in ALLOWED_BEFORE_STATUS['DELETE']:
          if not dry_run:
            inference.delete()
            inference.commit()
          else:
            logger.info("Dry run. Skipping commit.")
          deleted_inferences.append(inference)
        else:
          logger.warning(
              f"Could not delete inference {inference.id}: {inference.status} -> DELETE is not allowed.")

      return [dict_from_resource(res, DEFAULT_COLUMNS) for res in deleted_inferences]
    except DocumentError as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    except Exception as e:
      logger.error(f"Could not update inference. Reason: {e}", exc_info=True)
    finally:
      session.close()
