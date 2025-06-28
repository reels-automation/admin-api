build-docker:
	docker build -t api-minio-admin .
run:
	fastapi dev main.py --port 9999