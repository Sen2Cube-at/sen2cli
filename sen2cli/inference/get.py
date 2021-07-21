import logging
from typing import List, Union

from jsonapi_client import Session
from jsonapi_client.exceptions import DocumentError
from jsonapi_client.filter import Filter, Modifier
from jsonapi_client.resourceobject import ResourceObject
from oauthlib.oauth2 import OAuth2Token

from ..env import API_BASE_URL
from ..utils import filter_string_from_parameter

logger = logging.getLogger(__name__)


def get_inference(token: OAuth2Token,
                  id: Union[int, List, tuple, None] = None,
                  factbase_id: Union[int, List, tuple, None] = None,
                  knowledgebase_id: Union[int, List, tuple, None] = None,
                  status: Union[str, List, tuple, None] = None,
                  sort_by: str = None,
                  raw_modifier: str = None
                  ) -> List[ResourceObject]:
  """
  Get inferences

  :param token: OAuth2Token for a valid session
  :param id: id(s) of the inference to fetch. None for all.
  :param factbase_id: factbase_id(s) of the inference to fetch. None for all.
  :param knowledgebase_id: knowledgebase_id(s) (models) of the inference to fetch. None for all.
  :param status: Status of the inference to fetch. None for all.
  :return:
  """
  with Session(API_BASE_URL,
               request_kwargs=dict(
                   headers={'Authorization': f"{token['token_type']} {token['access_token']}"})) as session:
    try:
      filter_list = ','.join(list(filter(None, [
        filter_string_from_parameter('id', id),
        filter_string_from_parameter('factbase_id', factbase_id),
        filter_string_from_parameter('knowledgebase_id', knowledgebase_id),
        filter_string_from_parameter('status', status)
      ])))

      merged_filters = Filter(f'filter=[{filter_list}]')

      if not sort_by is None:
        merged_filters += Modifier(f'sort={sort_by}')

      if not raw_modifier is None:
        merged_filters += Modifier(raw_modifier)

      logger.debug(merged_filters.url_with_modifiers(''))
      inferences = session.get('inference', merged_filters)
      logger.info(f"Inferences loaded: {len(inferences.resources)}")
      return inferences.resources
    except DocumentError as e:
      logger.error(f"Could not fetch inference. Reason: {e}", exc_info=True)
    except Exception as e:
      logger.error(f"Could not fetch inference. Reason: {e}", exc_info=True)
    finally:
      session.close()
