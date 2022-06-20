# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# Add user that will be used in the container.
RUN useradd django

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000


# Install system packages required by django and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential wget gdebi \
    libpq-dev libmariadb-dev-compat libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev libwebp-dev \
    git

# Download and install wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.1.4-2/wkhtmltox_0.12.1.4-2.buster_amd64.deb
RUN gdebi --n ./wkhtmltox_0.12.1.4-2.buster_amd64.deb
RUN wkhtmltopdf --version

# Install the application server.
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN pip install "gunicorn==20.0.4"

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "django" user. This django project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown django:django /app

# Copy the source code of the project into the container.
COPY --chown=django:django . .

# copy entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh

# Make ./entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Use user "django" to run the build commands below and the server itself.
USER django

# Collect static files.
# RUN python -m pip install --upgrade pip
RUN python manage.py collectstatic --noinput --clear

ENTRYPOINT ["bash", "./entrypoint.sh"]
CMD gunicorn server.wsgi:application 0.0.0.0:8000 --log-level=DEBUG
