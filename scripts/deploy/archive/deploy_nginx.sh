docker-compose \
    -f docker-compose.yml \
    -f docker-compose.stag.yml \
    up \
    --force-recreate \
    --remove-orphans \
    --build \
    -d \
    nginx-gen \
&& \
docker-compose \
    -f docker-compose.yml \
    -f docker-compose.stag.yml \
    up \
    --force-recreate \
    --build \
    -d \
    nginx

