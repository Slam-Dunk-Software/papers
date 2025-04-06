# Papers

<img src="https://github.com/user-attachments/assets/baf26b49-1a71-474e-9ba0-635c92fa7b53" width="500" height="300">

---

This is the source code for [Papers](https://get-papers.com), a service which mails research papers, essays, blog posts, and other media to your doorstep.


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

## Shell
Papers has the shell_plus with IPython enabled, so the recommended way to run is:

```shell
uv run python manage.py shell_plus
```

## Database
Papers uses Postgres.

- Generating migrations:
  - For the core app:
    - `uv run python manage.py makemigrations core`
  - For the users app:
    - `uv run python manage.py makemigrations users`
- Running migrations:
  - `uv run python manage.py migrate`


## Deploy

- Deploys are managed in Heroku

## Shopify Webhooks
Papers uses Shopify.

These are the webhooks we're supporting:
- "Customer creation" -> `/webhooks/customers/create`
- "Customer update" -> `/webhooks/customers/update`
- "Order creation" -> `/webhooks/orders/create`
- "Fulfillment Creation" -> `/webhooks/fulfillments/create`
- "Fulfillment Update" -> `/webhooks/fulfillments/update`
  
