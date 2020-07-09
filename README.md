# A Python and Django Store API Example

## Installation

```bash

# Clone de repository
git clone https://github.com/gustavo-fonseca/pythonstore

# Go to project`s folder and copy .env.example to .env
cd /project-folder
cp .env.example .env

# Run docker-compose and make the initial migrations
docker-compose up -d
docker exec store_backend python manage.py makemigrations
docker exec store_backend python manage.py migrate
docker exec store_backend python manage.py loaddata initial.json

# Running in development mode
docker exec -it store_backend python manage.py runserver 0:8000

```
