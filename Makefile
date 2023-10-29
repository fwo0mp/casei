docker-app:
	docker build -t casei:0.0.1 -f docker/app.Dockerfile .

docker-nginx:
	docker build -t casei-nginx:0.0.1 -f docker/nginx.Dockerfile .