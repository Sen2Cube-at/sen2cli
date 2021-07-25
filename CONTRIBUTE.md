# How to contribute to this repository

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other
method with the maintainers of this repository before making a change.

Please have a look at the [GitHub guides](https://guides.github.com/) before contributing. Especially the
[GitHub workflow guide](https://guides.github.com/introduction/flow/). 

## General guidelines
  - **Do** create [feature requests / issues](/issues) before working on a new feature or fixing a bug.
  - **Do** create a [feature / bugfix branch](https://guides.github.com/introduction/flow/) whenever possible. No code
    related commits should go directly to `main`. This will help to keep merge conflicts at a minimum and the history
    of `main` tidy.
  - **Do** [reference issues](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) in your
    commit comments and PR. This will help to see the reason for a change. While it might be clear to you now why you
    made a certain change, you might have forgotten it in a few weeks.
  - **Do** use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) style for your commit messages. 
  - **Do** stick to the templates when writing an issue or pull request whenever possible.
  - **Do** use [Google style pydoc](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) strings for documentation.
  - **Don't** merge your own pull requets! Let someone else check your work before it goes into `main`. 

## Pull requests
  - **Do** address a single concern in the least number of changes as possible.
  - **Do** make sure your PR can be auto-merged into the branch you want to merge against e.g. `main`.
  - **Do** use squash commits on merging feature branches to `main` / `develop` to keep their history clean. Rule of
    thumb: Every merge should result in one [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) for the CHANGELOG. 
  - **Do** use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) style for your PR comments. 
 
## Releasing new version

  1. Merge all changes to `develop` branch.
  1. TEST EVERYTHING!   
  1. Update all version numbers. (setup.py, Dockerfile).  Use [semantic versioning](https://semver.org/).
  1. Create a version bump commit with comment `chore(release): <VERSION>`
  1. Create version tag locally. Name it `v<version>`.
  1. Run `auto-changelog -u -d "Commandline interface for Sen2Cube.at backend." --tag-prefix=v --github`
  1. Amend `v<VERSION>` commit with generated `CHANGELOG.md`
  1. Push everything and create GitHub release.
