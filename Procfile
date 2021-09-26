web: bash -c "cd iclinic_api && python manage.py migrate && gunicorn iclinic_api.wsgi:application --bind 0.0.0.0:$PORT -t 120 --reload"
