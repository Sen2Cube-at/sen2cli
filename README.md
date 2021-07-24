[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Python Version: 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.github.com/ZGIS/sen2cli)
[![License: GNU General Public License 3.0 or later](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Sen2Cube.at - Commandline interface

Commandline interface for Sen2Cube.at backend.

## 🔧 Installation
Install within your current Python environment:
```
pip install git+https://github.com/ZGIS/sen2cli.git@main
```

Run in a Docker container
```
## Download Dockerfile from GitHub
wget https://raw.githubusercontent.com/ZGIS/sen2cli/main/Dockerfile

docker build -t sen2cli:latest .
docker run -it --name sen2cli \
  -v "$(pwd)"/host_data:/home/sen2cli/host_data \
  sen2cli:latest /bin/bash
  
docker rm sen2cli
```

## 🔰 Basic Usage
```
sen2cli --help
sen2cli session --help
sen2cli session login --help

sen2cli session login --username=steffen.reichel --password=$(cat ./_password.txt)
sen2cli session refresh
sen2cli session info

sen2cli inference list --help
sen2cli inference list --knowledgebase_id=218
sen2cli inference list --knowledgebase_id=218 --knowledgebase_id=216 
sen2cli inference list --knowledgebase_id=218 --status=FAILED
sen2cli inference list --knowledgebase_id=218 --status=FAILED

sen2cli inference list --raw_modifier="<filterstring>"

sen2cli inference rerun --id=<id>
sen2cli inference abort --id=<id>

sen2cli inference rerun --id=7769 --id=7770 --id=7771 --id=7772
sen2cli inference abort --id=7769 --id=7770 --id=7771 --id=7772

sen2cli inference create 221 1 2020-03-01 2020-08-01 ./aoi.geojson --description="Very descriptive"
```

## Advanced usage

Create inference for specific files in a folder (on Unix):
```
find ./data -name "id_503*.geojson" -exec sen2cli inference create 221 1 2020-03-01 2020-08-01 {} --description="{}" \;
```

## Todo and wild ideas
```
sen2cli inference delete --id=<id> --knowledgebase_id=123 --force --dryrun

sen2cli inference download --id=123 --id=321     ##all incl qgis_proj
sen2cli inference download --id=123 --id=321 --include_qgis_project=TRUE/FALSE --result="result1" --result="greeness_no_cloud"

sen2cli inference list --knowledgebase_id=218 --status=FAILED --columns=id --headers=FALSE
sen2cli list | awk {extract ids} | for i in - run sen2cli --id={} download

sen2cli knowledgebase list
sen2cli factbase list
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
