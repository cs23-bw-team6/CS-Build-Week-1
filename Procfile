release: ./release-tasks.sh
web: gunicorn adv_project.wsgi:application --log-file -
worker: python ./util/world.py