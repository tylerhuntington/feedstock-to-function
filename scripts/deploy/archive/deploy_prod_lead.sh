docker-compose \
  -f docker-compose.lead.yml  \
	up \
	-d \
	--build \
	--force-recreate \
	&& docker logs web_ftf_django --follow

