# fastapi_starter_template

### Usage

```shell
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --workers 17 \
  --log-level critical \
  --no-access-log
```

### Start the program with gunicorn

```shell
gunicorn main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8002 \
  --workers 17  \
  --timeout 120 
```

### Start the program with docker

```shell
make dockerrun
```