# foodgram-project
### Description
Website where you can publish recipes, subscribe to publications of other users, as well as download a summary list of products required for the preparation of one or more selected dishes.
[Link to website!](http://178.154.213.197/)
- Admin: Timofey
- Password: haLo3V1q
### Technologies
- Python 3.9
- Django 3.2.3
- PostgreSQL 13.3
- Gunicorn 20.1.0
- Nginx 1.21.0
- Docker 20.10.5
### Before launching the project, enter the values of your database and SMTP-server into .env file
- "ENGINE" = the path to your database, like "django.db.backends.your_database"
- "NAME" = name your database
- "USER" = username django will use to access the database
- "PASSWORD" = password django will use to access the database
- "HOST" = ip adress your database
- "PORT" = access port your database
- "SECRET_KEY" = django secret key
- "EMAIL_HOST" = Host to be used to send email
- "EMAIL_PORT" = Port used for SMTP server
- "EMAIL_HOST_USER" = The name of the email that the smtp server will use
- "EMAIL_HOST_PASSWORD" = email password
- "EMAIL_USE_TLS" = Whether to use TLS (secure) connection when communicating with the SMTP server.
### Launch project with django server
- Install and activate virtual environment
- Install dependency from requrements.txt
``` pip install -r requirements.txt ```
- Make migrations
``` python manage.py migrate ```
- Collect static files
``` python manage.py collectstatic ```
- Create superuser
``` python manage.py createsuperuser ```
- To fill the database (full commands your options)
``` pg_restore --host "HOST" --port "PORT" --username "USER" --dbname "NAME" --section=data --verbose "~/foodgram_db.dump" ```
- Run local server
``` python manage.py run server ```
### Launch project with docker-compose
- Application launch
``` docker-compose up -d ```
- Make migrations
``` docker-compose exec web python manage.py migrate ```
- Collect static files
``` docker-compose exec web python manage.py collectstatic ```
- Creating superuser
``` docker-compose exec web python manage.py createsuperuser ```
- To fill the base (full commands your options)
``` docker-compose exec db pg_restore --host "HOST" --port "PORT" --username "USER" --dbname "NAME" --section=data --verbose "~/foodgram_db.dump" ```
### Author
Veselov Timofey
vestimofey@mail.ru