sleep 10
echo run migrate
python manage.py migrate

echo run loaddata
python manage.py loaddata fixtures.json

echo run gunicorn
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:5002

exec "$@"