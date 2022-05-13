docker-compose \
  -f docker-compose.molec.yml  \
  up \
  -d \
  --build \
&& \
docker logs --follow ftf_django_prod

