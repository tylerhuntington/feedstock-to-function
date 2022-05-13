docker-compose \
  -f docker-compose.ftf.sanslets.yml \
  down \
  &&
docker-compose \
  -f docker-compose.ftf.sanslets.yml \
	up \
	-d \
	--build \
	--force-recreate \
	&& docker logs ftf_django_web --follow
