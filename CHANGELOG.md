# Changelog

Commandline interface for Sen2Cube.at backend.

## 0.2.0 (2021-07-26)

#### New Features

* (inference): Add `inference delete` command to inference (close [#3](https://github.com/ZGIS/sen2cli/issues/3))
* (inference): Add `--factbase_id`, `knowledgebase_id`, and `--status` filter to inference rerun and abort command (close [#10](https://github.com/ZGIS/sen2cli/issues/10))
* (inference): add --dry-run option to `create`(close [#9](https://github.com/ZGIS/sen2cli/issues/9))
* (inference): add --dry-run option to `rerun` and `abort` command (close [#6](https://github.com/ZGIS/sen2cli/issues/6), close [#7](https://github.com/ZGIS/sen2cli/issues/7))
* (docker): add SEN2CLI_VERSION build arg to Dockerfile to specify tag / commit to use.
* (sen2cli): add version command to display current version.
#### Fixes

* (session): make token loading / refreshing more robust.
#### Refactorings

* (inference): move --output_format parameter from ls command to inference
* (inference): move --output_format parameter from ls command to inference
#### Docs

* (sen2cli): update help texts
* Update README.md and CONTRIBUTE.md
#### Others

* (release): 0.2.0
* (git): update .gitignore
* set default config directory to ~/.sen2cli

Full set of changes: [`v0.1.0...0.2.0`](https://github.com/ZGIS/sen2cli/compare/v0.1.0...0.2.0)

## v0.1.0 (2021-07-25)

#### Docs

* add empty Changelog
* update CONTRIBUTE.md and 'run in docker' section
#### Others

* release 0.1.0
* add editor and linter config
* (inference): code reformatted
