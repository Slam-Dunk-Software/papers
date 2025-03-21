# Papers

The source code for Slam Dunk Software's subscription service(s) which help developers learn new skills and keep the old skills sharp.

## Prerequisites
```sh
brew install uv # if on MacOS
uv python install 3.13.2  # There are alternative ways of managing python versions -- see here https://docs.astral.sh/uv/guides/install-python/

brew install 
```
FIXME: Reference Brewfile

`uv pip compile --output-file requirements.lock --group default`



Django...
```bash
uv run django-admin startproject core
```

After that's done...
```bash
uv run python manage.py startapp usersu
```

Then within core/settings.py's INSTALLED_APPS:
```python
    "users",  # Add the users app
```


HTMX:
```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
```

