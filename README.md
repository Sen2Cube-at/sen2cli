[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Python Version: 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.github.com/ZGIS/sen2cli)
[![License: GNU General Public License 3.0 or later](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Sen2Cube.at - Commandline interface

Commandline interface for Sen2Cube.at backend.

## 🔧 Installation

### 🐍 Local Python envirionment

Install latest commit from `main` in your current Python environment run
```bash
pip install git+https://github.com/ZGIS/sen2cli.git@main
```

You can also specify a version instead of `@main` e.g. 
```bash
pip install git+https://github.com/ZGIS/sen2cli.git@v0.2.0
```

### 🐳 Docker

Download [`Dockerfile`](https://github.com/ZGIS/sen2cli/blob/main/Dockerfile) from GitHub. To build the image for the
latest release version run

```
docker build -t sen2cli .
```

You can specify a version / tag / commit ref via build args. E.g

```
docker build --build-arg SEN2CLI_VERSION='v0.2.0' -t sen2cli .
```

To run the image and mount `./host_data` into `/home/sen2cli/host_data` run
```
docker run -it --name sen2cli \
  -v "$(pwd)"/host_data:/home/sen2cli/host_data \
  sen2cli /bin/bash
```

After you are done, you might want to remove the container.  
```
docker rm sen2cli
```

## 🔰 Basic Usage

All commands and parameters as documented in the help screen.
```
$ sen2cli --help

Usage: sen2cli [OPTIONS] COMMAND [ARGS]...

Options:
  --log_file FILE  Write log to this file instead of StdErr.
  -v, --verbose    Verbose log output. Can be added up to three times for even
                   more verbosity (WARNING, INFO, DEBUG).  [x>=0]
  --help           Show this message and exit.

Commands:
  inference  Display / create / modify inferences
  session    Session related commands like 'login'
  version    Prints program version
```


```
$ sen2cli inference --help
Usage: sen2cli inference [OPTIONS] COMMAND [ARGS]...

  Display / create / modify inferences

Options:
  --tokenfile FILE                File that stores the token.  [env var:
                                  S2C_TOKENFILE]
  -f, --output_format [csv|csv_no_hdr|json]
                                  Specify output format (CSV, CSV without
                                  header, JSON)
  --help                          Show this message and exit.

Commands:
  abort   Abort running / scheduled inferences
  create  Create and schedule inference
  delete  Delete inferences.
  ls      List inferences
  rerun   Rerun finished / stopped / failed inferences
```

### Start session / login
First you need to start a session. 
```
$ sen2cli session login
Username: steffen.reichel
Password: 

Trying to authenticate against https://auth.sen2cube.at/realms/sen2cube-at/protocol/openid-connect/token with client iq-web-client
Login successful. Session expires at 1970-01-01 00:05:00.000000
```

```
$ sen2cli session info
Logged in as:  steffen.reichel
Expires at:    1970-01-01 00:05:00.000000
Refresh until: 1970-01-01 00:30:00.000000
```

You can manually refresh the session

```
$ sen2cli session refresh
Refresh successful. Session expires at 1970-01-01 00:15:00.000000
```

```
$ sen2cli session info
Logged in as:  steffen.reichel
Expires at:    1970-01-01 00:15:00.000000
Refresh until: 1970-01-01 00:40:00.000000
```

**NOTE** To login in a script you can specify the environment variables `S2C_USERNAME` and `S2C_PASSWORD`.

**NOTE** For convenience the session will automatically be refreshed by commands like `inference ls`. 

### Working with inferences

The output format of the `inference` defaults to CSV. All log messages are written to `STD_ERR` (details see below)

Schedule an inference
```
$ sen2cli inference create 218 1 2020-03-01 2020-08-01 ./host_data/geodata/id_50101.geojson --description="Scheduled for documentation"
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8341;1;False;218;steffen.reichel;;[];CREATED;Inference sucessfully created;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:42:55.796924+00:00;;
```

List inferences without filter
```
$ sen2cli inference ls
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8343;1;False;218;steffen.reichel;;[];STARTED;The inference was accepted by the inference engine;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:20.449208+00:00;;2021-07-25T20:46:19.984137+00:00
8342;1;False;218;steffen.reichel;;[];STARTED;The inference was accepted by the inference engine;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:11.031368+00:00;;2021-07-25T20:46:10.288988+00:00
8341;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8341.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8341, ""value_type"": ""numerical"", ""value_range"": [356.0, 5215.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8341_4326.tiff"", ""bytes"": 5400877, ""band_value_ranges"": [[356.0, 5215.5], [572.5, 3839.0], [802.0, 4391.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:42:55.796924+00:00;2021-07-25T20:46:02.843996+00:00;2021-07-25T20:42:54.826214+00:00
```

Get inferences with filter
```
$ sen2cli inference ls --id=8343
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8343;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8343.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8343, ""value_type"": ""numerical"", ""value_range"": [330.0, 2611.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8343_4326.tiff"", ""bytes"": 2037934, ""band_value_ranges"": [[330.0, 2296.0], [547.0, 2240.0], [768.0, 2611.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:20.449208+00:00;2021-07-25T20:47:22.156676+00:00;2021-07-25T20:46:19.984137+00:00
```

```
$ sen2cli inference ls --id=8343 --id=8341
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8343;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8343.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8343, ""value_type"": ""numerical"", ""value_range"": [330.0, 2611.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8343_4326.tiff"", ""bytes"": 2037934, ""band_value_ranges"": [[330.0, 2296.0], [547.0, 2240.0], [768.0, 2611.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:20.449208+00:00;2021-07-25T20:47:22.156676+00:00;2021-07-25T20:46:19.984137+00:00
8341;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8341.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8341, ""value_type"": ""numerical"", ""value_range"": [356.0, 5215.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8341_4326.tiff"", ""bytes"": 5400877, ""band_value_ranges"": [[356.0, 5215.5], [572.5, 3839.0], [802.0, 4391.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:42:55.796924+00:00;2021-07-25T20:46:02.843996+00:00;2021-07-25T20:42:54.826214+00:00
```

Valid filters are: `--id`, `--knowledgebase_id`, `--factbase_id`, `--status`. All filters can be added multiple times.
Filter with the same name are combined with `OR`. Different filters with `AND`. So

```sen2cli inference ls --status=FAILED --knowledgebase_id=218 --knowledgebase_id=221```

will result in a filter

```(status in ['FAILED']) AND (knowledgebase_id in [218,221])```

Sorting inference ls with the `--sort` option.
```
$ sen2cli inference ls --id=8357 --id=8356 --id=8355 --id=8354 --id=8353 --sort=status
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8354;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:42.475198+00:00;2021-07-25T21:16:54.250457+00:00;2021-07-25T21:15:31.810449+00:00
8357;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:47.710966+00:00;2021-07-25T21:17:00.174409+00:00;2021-07-25T21:16:58.742892+00:00
8355;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:44.445165+00:00;2021-07-25T21:17:02.535571+00:00;2021-07-25T21:15:32.080859+00:00
8353;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8353.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8353, ""value_type"": ""numerical"", ""value_range"": [383.0, 7426.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8353_4326.tiff"", ""bytes"": 9156158, ""band_value_ranges"": [[383.0, 7426.5], [621.0, 6010.0], [865.5, 5697.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:41.393191+00:00;2021-07-25T21:21:07.064940+00:00;2021-07-25T21:16:45.956145+00:00
8356;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8356.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8356, ""value_type"": ""numerical"", ""value_range"": [536.0, 2522.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8356_4326.tiff"", ""bytes"": 87112, ""band_value_ranges"": [[536.0, 2399.5], [777.0, 2336.5], [954.0, 2522.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:46.428738+00:00;2021-07-25T21:17:23.391463+00:00;2021-07-25T21:15:32.401723+00:00
```

The `--sort` option can be a list of columns. Descending sort order by adding a `-` in front of the column name.
```
$ sen2cli inference ls --id=8357 --id=8356 --id=8355 --id=8354 --id=8353 --sort=status,-id
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8357;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:47.710966+00:00;2021-07-25T21:17:00.174409+00:00;2021-07-25T21:16:58.742892+00:00
8355;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:44.445165+00:00;2021-07-25T21:17:02.535571+00:00;2021-07-25T21:15:32.080859+00:00
8354;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:42.475198+00:00;2021-07-25T21:16:54.250457+00:00;2021-07-25T21:15:31.810449+00:00
8356;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8356.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8356, ""value_type"": ""numerical"", ""value_range"": [536.0, 2522.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8356_4326.tiff"", ""bytes"": 87112, ""band_value_ranges"": [[536.0, 2399.5], [777.0, 2336.5], [954.0, 2522.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:46.428738+00:00;2021-07-25T21:17:23.391463+00:00;2021-07-25T21:15:32.401723+00:00
8353;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8353.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8353, ""value_type"": ""numerical"", ""value_range"": [383.0, 7426.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8353_4326.tiff"", ""bytes"": 9156158, ""band_value_ranges"": [[383.0, 7426.5], [621.0, 6010.0], [865.5, 5697.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:41.393191+00:00;2021-07-25T21:21:07.064940+00:00;2021-07-25T21:16:45.956145+00:00
```

Restart finished / failed inferences. This will not reschedule running inferences! Abort them first.
```
$ sen2cli inference rerun --id=8343
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8343;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8343.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8343, ""value_type"": ""numerical"", ""value_range"": [330.0, 2611.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8343_4326.tiff"", ""bytes"": 2037934, ""band_value_ranges"": [[330.0, 2296.0], [547.0, 2240.0], [768.0, 2611.0]]}]";CREATED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:20.449208+00:00;2021-07-25T20:47:22.156676+00:00;2021-07-25T20:46:19.984137+00:00
```

Abort running / scheduled inferences.
```
$ sen2cli inference abort --id=8342
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8342;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8342.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8342, ""value_type"": ""numerical"", ""value_range"": [382.0, 3122.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8342_4326.tiff"", ""bytes"": 689508, ""band_value_ranges"": [[382.0, 3122.0], [647.5, 2730.0], [865.5, 2621.0]]}]";ABORTED;The inference was accepted by the inference engine;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:11.031368+00:00;2021-07-25T21:00:36.828885+00:00;2021-07-25T21:00:55.640893+00:00
```

Delete inferences
```
$ sen2cli inference delete --id=8341
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8341;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8341.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8341, ""value_type"": ""numerical"", ""value_range"": [356.0, 5215.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8341_4326.tiff"", ""bytes"": 5400877, ""band_value_ranges"": [[356.0, 5215.5], [572.5, 3839.0], [802.0, 4391.0]]}]";ABORTED;The inference was aborted.;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:42:55.796924+00:00;2021-07-25T21:02:11.942261+00:00;2021-07-25T21:00:55.105278+00:00
```



All filters can also be applied to `rerun`, `abort`, and `delete`.
```
$ sen2cli inference rerun --knowledgebase_id=218
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8341;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8341.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8341, ""value_type"": ""numerical"", ""value_range"": [356.0, 5215.5], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8341_4326.tiff"", ""bytes"": 5400877, ""band_value_ranges"": [[356.0, 5215.5], [572.5, 3839.0], [802.0, 4391.0]]}]";CREATED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:42:55.796924+00:00;2021-07-25T20:46:02.843996+00:00;2021-07-25T20:42:54.826214+00:00
8342;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8342.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8342, ""value_type"": ""numerical"", ""value_range"": [382.0, 3122.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8342_4326.tiff"", ""bytes"": 689508, ""band_value_ranges"": [[382.0, 3122.0], [647.5, 2730.0], [865.5, 2621.0]]}]";CREATED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:11.031368+00:00;2021-07-25T20:47:45.398702+00:00;2021-07-25T20:46:10.288988+00:00
8343;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8343.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8343, ""value_type"": ""numerical"", ""value_range"": [330.0, 2611.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8343_4326.tiff"", ""bytes"": 2047434, ""band_value_ranges"": [[330.0, 2296.0], [547.0, 2240.0], [768.0, 2611.0]]}]";CREATED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T20:46:20.449208+00:00;2021-07-25T20:58:38.723913+00:00;2021-07-25T20:57:39.019024+00:00
```

To preview what inferences would be affected by `rerun`, `abort`, and `delete` you can use the option `--dry-run`.
```
$ sen2cli inference delete --status=FAILED --dry-run
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8346;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:25.077964+00:00;2021-07-25T21:16:40.303429+00:00;2021-07-25T21:15:28.514281+00:00
8354;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:42.475198+00:00;2021-07-25T21:16:54.250457+00:00;2021-07-25T21:15:31.810449+00:00
8357;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:47.710966+00:00;2021-07-25T21:17:00.174409+00:00;2021-07-25T21:16:58.742892+00:00
8358;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'mask' because of ""ValueError('zero-size array to reduction operation fmin which has no identity')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:49.843503+00:00;2021-07-25T21:17:42.217461+00:00;2021-07-25T21:15:30.031904+00:00
8355;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:44.445165+00:00;2021-07-25T21:17:02.535571+00:00;2021-07-25T21:15:32.080859+00:00
8361;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:54.850137+00:00;2021-07-25T21:17:13.503607+00:00;2021-07-25T21:15:33.750006+00:00
8367;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:12:05.651447+00:00;2021-07-25T21:16:40.411747+00:00;2021-07-25T21:15:36.545195+00:00
8349;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:31.692110+00:00;2021-07-25T21:17:13.516873+00:00;2021-07-25T21:16:44.912674+00:00
8366;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:12:04.080897+00:00;2021-07-25T21:17:06.487459+00:00;2021-07-25T21:17:04.758312+00:00
```


## 🎓 Advanced usage

For further processing output can be redirected. 

```
$ sen2cli inference ls > inferences.csv
```

If the default CSV is not desireable there are more output formats:
- `csv_no_hdr` - same as `csv` but without header line
- `json` - JSON array 

```
$ sen2cli inference --output_format=json ls > inferences.json
```

Create inference for specific files in a folder (on Unix):
```
find ./host_data/geodata -name "id_9*01.geojson" -exec sen2cli inference create 218 1 2020-03-01 2020-08-01 {} --description="{}" \;
```

### Advanced filtering

For more advanced filters `ls` has a `--raw_modifier` option. The content of this option will be added as URL parameter
to the query. For example if you want to filter for specific error messages, you can create a file `filter.json` with
the following contents
```json
[
  {
    "name": "status_message",
    "op": "ilike",
    "val": "%psycopg2.OperationalError%"
  }
]
```

```
$ sen2cli inference ls --raw_modifier="filter=$(cat ./filter.json)"
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8367;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:12:05.651447+00:00;2021-07-25T21:16:40.411747+00:00;2021-07-25T21:15:36.545195+00:00
8366;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:12:04.080897+00:00;2021-07-25T21:17:06.487459+00:00;2021-07-25T21:17:04.758312+00:00
8361;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:54.850137+00:00;2021-07-25T21:17:13.503607+00:00;2021-07-25T21:15:33.750006+00:00
8357;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:47.710966+00:00;2021-07-25T21:17:00.174409+00:00;2021-07-25T21:16:58.742892+00:00
8355;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:44.445165+00:00;2021-07-25T21:17:02.535571+00:00;2021-07-25T21:15:32.080859+00:00
8354;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:42.475198+00:00;2021-07-25T21:16:54.250457+00:00;2021-07-25T21:15:31.810449+00:00
8349;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:31.692110+00:00;2021-07-25T21:17:13.516873+00:00;2021-07-25T21:16:44.912674+00:00
8346;1;False;218;steffen.reichel;;[];FAILED;"The inference failed: Evaluation failed at 'data' because of ""OperationalError('(psycopg2.OperationalError) FATAL:  remaining connection slots are reserved for non-replication superuser connections\\n')""";;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:25.077964+00:00;2021-07-25T21:16:40.303429+00:00;2021-07-25T21:15:28.514281+00:00
```

For full documentation on the filter language see [flask-rest-jsonapi filterring](https://flask-rest-jsonapi.readthedocs.io/en/latest/filtering.html).

**NOTE** this might have unforseen consquences and side-effects when using in combination with other filters. As this
parameter is just added as a URL parameter, it can be used for other shenanigans like pagination, or sparse result sets.
For that reason it's only available in `ls` and not the rest. USE AT YOUR OWN RISK! ;-)

### Working with verbose logs / log files

All log output is written to `STD_ERR` per default and only errors are logged. There is
a `-v` option that can be used to switch on more verbose logging.

- `-v` logs errors, and warnings
- `-vv` logs errors, warnings, and info
- `-vvv` logs errors, warnings, info, and debug

```
$ sen2cli -vv inference ls --id 8345
2021-07-26 12:17:00 [INFO] - load_or_refresh_token:108 - Token expired. Trying refresh.
2021-07-26 12:17:00 [INFO] - refresh_token:60 - Token refresh successful.
2021-07-26 12:17:00 [INFO] - __enter__:261 - Entering session
2021-07-26 12:17:00 [INFO] - _fetch_json:487 - Fetching document from url ParseResult(scheme='https', netloc='api.sen2cube.at', path='/v1/inference', params='', query='&filter=[{"name":"id", "op": "in", "val": [8345]}]&sort=-id', fragment='')
2021-07-26 12:17:00 [INFO] - get_inference:59 - Inferences loaded: 1
2021-07-26 12:17:00 [INFO] - __exit__:271 - Exiting session
2021-07-26 12:17:00 [INFO] - _commit_sync:601 - Committing dirty resources
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8345;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8345.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8345, ""value_type"": ""numerical"", ""value_range"": [467.0, 4031.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8345_4326.tiff"", ""bytes"": 2056211, ""band_value_ranges"": [[467.0, 4031.0], [696.0, 3521.0], [911.5, 3440.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:22.927903+00:00;2021-07-25T21:18:26.814518+00:00;2021-07-25T21:15:36.628143+00:00
```

```
$ sen2cli -vvv inference ls --id 8345
2021-07-26 12:17:47 [DEBUG] - load_token:83 - Loading token from /Users/steffen/.sen2cli/token.json...
2021-07-26 12:17:47 [INFO] - __enter__:261 - Entering session
2021-07-26 12:17:47 [DEBUG] - filter_string_from_parameter:66 - {"name":"id", "op": "in", "val": [8345]}
2021-07-26 12:17:47 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:17:47 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:17:47 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:17:47 [DEBUG] - get_inference:57 - ?&filter=[{"name":"id", "op": "in", "val": [8345]}]&sort=-id
2021-07-26 12:17:47 [INFO] - _fetch_json:487 - Fetching document from url ParseResult(scheme='https', netloc='api.sen2cube.at', path='/v1/inference', params='', query='&filter=[{"name":"id", "op": "in", "val": [8345]}]&sort=-id', fragment='')
2021-07-26 12:17:47 [DEBUG] - _new_conn:971 - Starting new HTTPS connection (1): api.sen2cube.at:443
2021-07-26 12:17:47 [DEBUG] - _make_request:452 - https://api.sen2cube.at:443 "GET /v1/inference?&filter=%5B%7B%22name%22:%22id%22,%20%22op%22:%20%22in%22,%20%22val%22:%20%5B8345%5D%7D%5D&sort=-id HTTP/1.1" 200 188645
2021-07-26 12:17:48 [INFO] - get_inference:59 - Inferences loaded: 1
2021-07-26 12:17:48 [INFO] - __exit__:271 - Exiting session
2021-07-26 12:17:48 [INFO] - _commit_sync:601 - Committing dirty resources
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8345;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8345.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8345, ""value_type"": ""numerical"", ""value_range"": [467.0, 4031.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8345_4326.tiff"", ""bytes"": 2056211, ""band_value_ranges"": [[467.0, 4031.0], [696.0, 3521.0], [911.5, 3440.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:22.927903+00:00;2021-07-25T21:18:26.814518+00:00;2021-07-25T21:15:36.628143+00:00
```

As all normal output is written to `STD_OUT` it can be easily separated from the logging with output redirection.

```
$ sen2cli -vvv inference ls --id 8345 1> inferences.csv 2> logfile.txt
$ cat inferences.csv 
id;factbase_id;favourite;knowledgebase_id;owner;qgis_project_location;output;status;status_message;status_progress;status_timestamp;temp_range_end;temp_range_start;timestamp_created;timestamp_finished;timestamp_started
8345;1;False;218;steffen.reichel;/output/sen2cube/steffen.reichel/qgis-project-id8345.zip;"[{""name"": ""Cloud_free_composite"", ""inference_id"": 8345, ""value_type"": ""numerical"", ""value_range"": [467.0, 4031.0], ""dims"": [""band"", ""y"", ""x""], ""file_type"": ""geotiff"", ""vis_type"": ""composite"", ""data"": ""/output/sen2cube/steffen.reichel/Cloud_free_composite_id8345_4326.tiff"", ""bytes"": 2056211, ""band_value_ranges"": [[467.0, 4031.0], [696.0, 3521.0], [911.5, 3440.0]]}]";SUCCEEDED;The inference was successfully processed;;;2020-08-01T23:59:59.999000+00:00;2020-03-01T00:00:00+00:00;2021-07-25T21:11:22.927903+00:00;2021-07-25T21:18:26.814518+00:00;2021-07-25T21:15:36.628143+00:00

$ cat logfile.txt 
2021-07-26 12:21:51 [DEBUG] - load_token:83 - Loading token from ~/.sen2cli/token.json...
2021-07-26 12:21:51 [INFO] - __enter__:261 - Entering session
2021-07-26 12:21:51 [DEBUG] - filter_string_from_parameter:66 - {"name":"id", "op": "in", "val": [8345]}
2021-07-26 12:21:51 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:21:51 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:21:51 [DEBUG] - filter_string_from_parameter:69 - List/Tuple was empty
2021-07-26 12:21:51 [DEBUG] - get_inference:57 - ?&filter=[{"name":"id", "op": "in", "val": [8345]}]&sort=-id
2021-07-26 12:21:51 [INFO] - _fetch_json:487 - Fetching document from url ParseResult(scheme='https', netloc='api.sen2cube.at', path='/v1/inference', params='', query='&filter=[{"name":"id", "op": "in", "val": [8345]}]&sort=-id', fragment='')
2021-07-26 12:21:51 [DEBUG] - _new_conn:971 - Starting new HTTPS connection (1): api.sen2cube.at:443
2021-07-26 12:21:51 [DEBUG] - _make_request:452 - https://api.sen2cube.at:443 "GET /v1/inference?&filter=%5B%7B%22name%22:%22id%22,%20%22op%22:%20%22in%22,%20%22val%22:%20%5B8345%5D%7D%5D&sort=-id HTTP/1.1" 200 188645
2021-07-26 12:21:51 [INFO] - get_inference:59 - Inferences loaded: 1
2021-07-26 12:21:51 [INFO] - __exit__:271 - Exiting session
2021-07-26 12:21:51 [INFO] - _commit_sync:601 - Committing dirty resources
```

If that is inconvenient the logfile can also be set via the `--log_file` option. If the logfile already exists, the new
log will be appended to the current file.

```
$ sen2cli -vvv --log_file="./logfile.txt" inference ls --id 8345 > inferences.csv
```


#  License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
