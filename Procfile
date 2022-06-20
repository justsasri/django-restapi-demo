release: bash ./release.sh
web: gunicorn server.wsgi
worker: python manage.py rqworker default
