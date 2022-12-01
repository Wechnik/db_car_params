# db_car_params

docker run --name cars_db -p 5432:5432 -d -e POSTGRES_USER='cars_db' -e POSTGRES_PASSWORD='cars_db' -e POSTGRES_DB='cars_db' postgres:11