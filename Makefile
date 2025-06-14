

clean:
	find . -type f -iname "*.log*" -delete;
	rm -rf logs

format:
	uvx ruff format .

run:
	uv run main.py

dockerbuild:
	uv pip compile pyproject.toml -o requirements.txt
	docker build -f containers/Dockerfile -t my-fastapi-app .

dockerrun: dockerbuild
	docker run -p 9921:8000 -v $(PWD):/app my-fastapi-app