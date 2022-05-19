#!/usr/bin/env python
# This file is meant to start this whole kerfuffle without installing sen2cli.

from sen2cli import sen2cli

if __name__ == '__main__':
##  sen2cli.cli()
  filter = '''
[
  {
    "and": [
      {
        "name": "timestamp_started",
        "op": "gt",
        "val": "2021-07-25T22:06:22"
      },
      {
        "name": "status",
        "op": "eq",
        "val": "SUCCEEDED"
      }
    ]
  }
]
  '''

#sen2cli.cli(['inference', '--help'])
#  sen2cli.cli(['session', 'login'])

  sen2cli.cli(['-vv'
               , 'inference'
               , '--output_format=csv'
               , 'ls'
               , '--count_only'
               , '--id=8366'
               ,'--status=FAILED'
              ,f'--raw_modifier=filter={filter}'
              ])
