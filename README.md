# db_car_params

docker run --name cars_db -p 5432:5432 -d -e POSTGRES_USER='cars_db' -e POSTGRES_PASSWORD='cars_db' -e POSTGRES_DB='cars_db' postgres:11

python core/manage.py loaddata core/db_manager/fixtures/params_value.json.gz  --app db_manager

git remote set-url origin https://<token>@github.com/<username>/<repo>
