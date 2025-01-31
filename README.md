docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=postgres `
    -e POSTGRES_PASSWORD=admin `
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
