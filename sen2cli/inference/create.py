import logging
from datetime import datetime

from jsonapi_client import Session
from jsonapi_client.exceptions import DocumentError
from oauthlib.oauth2 import OAuth2Token

from .util import INFERENCE_SCHEMA
from ..env import API_BASE_URL
from ..session.oauth_util import get_user_info

logger = logging.getLogger(__name__)


def create_inference(token: OAuth2Token,
                     factbase_id: int,
                     knowldegebase_id: int,
                     temp_range_start: datetime,
                     temp_range_end: datetime,
                     spatial_subset: str,
                     description: str,
                     ) -> int:

  user_info = get_user_info(token)

  with Session(API_BASE_URL, schema=INFERENCE_SCHEMA,
               request_kwargs=dict(
                   headers={'Authorization': f"{token['token_type']} {token['access_token']}"})) as session:
    try:
      trs = temp_range_start.strftime("%Y-%m-%dT00:00:00.000Z")
      tre = temp_range_end.strftime("%Y-%m-%dT23:59:59.999Z")

      desc = "Created by sen2cli" if description is None else description
      inference = session.create('inference',
                                 owner=user_info['preferred_username'],
                                 timestamp_created=None,
                                 timestamp_started=None,
                                 timestamp_finished=None,
                                 status=None,
                                 output=[],
                                 favourite=False,
                                 comment=desc,
                                 fields={
                                   'status_message': None,
                                   'temp_range_start': trs,
                                   'temp_range_end': tre,
                                   'area_of_interest': spatial_subset,
                                   'output_scale_factor': 1,
                                 },
                                 )
      inference.knowledgebase = knowldegebase_id
      inference.factbase = factbase_id
      logger.debug(inference.json)
      inference.commit()
      return inference.id
    except DocumentError as e:
      logger.error(f"Could not create inference. Reason: {e}", exc_info=True)
    except Exception as e:
      logger.error(f"Could not create inference. Reason: {e}", exc_info=True)
    finally:
      session.close()
