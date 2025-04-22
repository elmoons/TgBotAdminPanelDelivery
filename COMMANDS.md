
docker network create myNetwork

docker run --name panel_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=tg_panel \
    --network=myNetwork \
    --volume pg-panel-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name panel_broker \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:latest

docker run --name tg_panel \
    --network=myNetwork \
    tg_panel_image

docker run --name panel_celery_worker \
    --network=myNetwork \
    tg_panel_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name panel_celery_beat \
    --network=myNetwork \
    tg_panel_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker build -t tg_panel_image .
