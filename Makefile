datetime := $(shell date +%Y%m%d%H%M%S)
projectname := $(shell basename $(PWD))

clean:
	find . -type f -iname "*.log*" -delete
	find src -type d -name "__pycache__"  | xargs rm -rf
	rm -rf logs

format:
	uvx ruff format .

run:
	uv run main.py

docker_build:
	uv pip compile pyproject.toml -o requirements.txt
	docker build -f containers/Dockerfile -t $(projectname):$(datetime) .

docker_run: docker_build
	docker run -p 9921:8000 -v $(PWD):/app $(projectname):$(datetime)

docker_clean_image:
	docker images | grep "$(projectname)" | awk '{print $3}' | xargs docker rmi -f

docker_clean_task:
	docker ps -a | grep "my-fastapi-app" | awk '{print $1}' | xargs docker rm -f