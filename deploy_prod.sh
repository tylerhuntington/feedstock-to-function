docker-compose \
  -f docker-compose.yml \
	up \
	-d \
	--build \
	&& docker logs ftf_django_web --follow

