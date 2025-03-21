# Papers

The source code for Slam Dunk Software's subscription service(s) which help developers learn new skills and keep the old skills sharp.

## Prerequisites
```sh
brew install uv # if on MacOS
uv python install 3.13.2  # There are alternative ways of managing python versions -- see here https://docs.astral.sh/uv/guides/install-python/

brew install
```
FIXME: Reference Brewfile


## Tasks

Papers uses [Task](https://taskfile.dev/) to manage almost everything -- development tasks, builds, chores (linting, type checking), CI/CD, etc.

Example tasks:
- `task reset_db` -- drop and re-create development database
- `task intstall` -- install dependencies
- `task lint` -- run linter ([ruff](https://github.com/astral-sh/ruff))
- `task typecheck` -- run typechecking ([mypy](https://github.com/python/mypy))
- and many more... see [Taskfile.yaml](Taskfile.yaml) for all definitions
