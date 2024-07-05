# fastapi_starter_template

## Getting Started

### Installation

- The Poetry package manager is required for
  installation. [Poetry Installation](https://python-poetry.org/docs/#installation)
  Depending on your environment, this might work:

```bash
pip install poetry
poetry install
poetry shell # activates virtual environment
```

### Usage

```shell
uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --workers 17
```

```shell
gunicorn src.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8002 \
  --workers 17
```
