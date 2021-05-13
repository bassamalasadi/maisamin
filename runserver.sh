python manage.py collectstatic --no-input

python manage.py migrate

python manage.py runserver
# gunicorn --worker-tmp--dir /dev/shm webshop.wsgi
