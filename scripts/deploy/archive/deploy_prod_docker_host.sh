export DOCKER_HOST="ssh://tylerhuntington222@feedstock-to-function.ese.lbl.gov" \
&& docker-compose \
-f docker-compose.ftf.yml \
up \
--build

