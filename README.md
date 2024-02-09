
[Django (Backend) + React (Frontend) Basic Tutorial](https://medium.com/@gazzaazhari/django-backend-react-frontend-basic-tutorial-6249af7964e4)

[Django: How to profile and improve startup time](https://adamj.eu/tech/2023/03/02/django-profile-and-improve-import-time/)

```
python -X importtime -c 'import django'

```

```
python manage.py runserver
```

```
python manage.py createsuperuser
-
heidless
rob.lockhart@yahoo.co.uk
dafgsdfgdfgadfbdhsfgjdfghadf
-
```

```
python manage.py collectstatic

```

### [django-environ](https://django-environ.readthedocs.io/en/latest/quickstart.html)

# postgres

sudo service postgresql restart
sudo su postgres

psql -U postgres
-
postgres

# create db
CREATE DATABASE  todo_db;

# create user
CREATE USER arjuna WITH PASSWORD 'havana11';

export POSTGRES_HOST=postgres
export POSTGRES_PORT=5432
export POSTGRES_DB=todo_db
export POSTGRES_USER=arjuna
export POSTGRES_PASSWORD=havana11
export DATABASE_URL=postgres://arjuna:havana11@localhost:5432/todo_db

# DATABASE_URL=psql://user:un-githubbedpassword@127.0.0.1:8458/database
