git config user.name "Artem"
git config user.email "gakerchannel@gmail.com"

docker network create myNetwork

docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=postgres `
    -e POSTGRES_PASSWORD=HDjjkdidjhyDSDRUolpe20g2h89du6j `
    -e POSTGRES_DB=booking `
    --network=myNetwork `
    --volume pg-booking-data:/var/lib/postgresql/data `
    -d postgres:16

docker run --name booking_cache `
    -p 7887:6379 `
    --network=myNetwork `
    -d redis:7.4

docker run --name booking_back `
    -p 8345:8000 `
    --network=myNetwork `
    booking_image

docker run --name booking_celery_worker `
    --network=myNetwork `
    booking_image `
    celery --app=app.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_nginx `
    --volume D:/GitHub/StusyProjectGitlab/nginx.conf:/etc/nginx/nginx.conf `
    --network=myNetwork `
    --rm -p 80:80 nginx