# fastapi_starter_template

### Usage

```shell
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 17
```

```shell
gunicorn main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8002 \
  --timeout 120 \
  --workers 17
```
