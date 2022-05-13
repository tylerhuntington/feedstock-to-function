docker-compose \
    -f docker-compose.yml \
    -f docker-compose.stag.yml \
    build \
    --build-arg django_settings_module=staging \
    web-stag \
&& \
docker-compose \
    -f docker-compose.yml \
    -f docker-compose.stag.yml \
    up \
    -d \
    web-stag \
&& \
docker logs --follow jbei_lead_stag



