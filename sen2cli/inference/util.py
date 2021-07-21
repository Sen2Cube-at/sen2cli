from typing import Final, List

INFERENCE_STATUS = ['ABORTED',
                    'CREATED',
                    'FAILED',
                    'OFFLINE',
                    'SCHEDULED',
                    'STARTED',
                    'SUCCEEDED'
                    ]

ALLOWED_BEFORE_STATUS = {
  'CREATED': ['ABORTED', 'FAILED', 'SUCCEEDED'],
  'ABORTED': ['CREATED', 'SCHEDULED', 'STARTED']
}

DEFAULT_COLUMNS: Final[List[str]] = [
  'factbase_id',
  'favourite',
  'knowledgebase_id',
  'owner',
  'qgis_project_location',
  'output',
  'status',
  'status_message',
  'status_progress',
  'status_timestamp',
  'temp_range_end',
  'temp_range_start',
  'timestamp_created',
  'timestamp_finished',
  'timestamp_started'
]

INFERENCE_SCHEMA = {
  "inference": {
    "properties": {
      "owner": {
        "type": "string"
      },
      "timestamp_created": {
        "type": ["string", "null"]
      },
      "timestamp_started": {
        "type": ["string", "null"]
      },
      "timestamp_finished": {
        "type": ["string", "null"]
      },
      "status": {
        "type": ["string", "null"]
      },
      "status_message": {
        "type": ["string", "null"]
      },
      "temp_range_start": {
        "type": "string"
      },
      "temp_range_end": {
        "type": "string"
      },
      "area_of_interest": {
        "type": "string"
      },
      "qgis_project_location": {
        "type": ["string", "null"]
      },
      "output": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "comment": {
        "type": "string",
      },
      "output_scale_factor": {
        "type": "integer"
      },
      "favourite": {
        "type": "boolean"
      },
      'factbase': {'relation': 'to-one', 'resource': ['factbase']},
      'knowledgebase': {'relation': 'to-one', 'resource': ['knowledgebase']},

    }
  },
  "knowledgebase": {
    "properties": {
      "title": {
        "type": "string"
      },
    }
  },
  "factbase": {
    "properties": {
      "title": {
        "type": "string"
      },
    }
  }
}