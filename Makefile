docker-app:
	docker build -t bscheinman/casei:0.0.1 -f docker/app.Dockerfile .

docker-nginx:
	docker build -t bscheinman/casei-nginx:0.0.1 -f docker/nginx.Dockerfile .
