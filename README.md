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
### Before launching the project, enter the values of your database into .env file
- "ENGINE" = the path to your database, like "django.db.backends.your_database"
- "NAME" = name your database
- "USER" = username django will use to access the database
- "PASSWORD" = password django will use to access the database
- "HOST" = ip adress your database
- "PORT" = access port your database
- "SECRET_KEY" = django secret key
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
- To fill the database ingredient and tag
``` python manage.py load_ingredient ```
``` python manage.py create_tag ```
- Run local server
``` python manage.py run server ```
### Launch project with docker-compose
- Application launch
``` docker-compose up -d ```
- Make migrations
``` docker-compose exec python manage.py migrate ```
- Collect static files
``` docker-compose exec python manage.py collectstatic ```
- Creating superuser
``` docker-compose exec python manage.py createsuperuser ```
- To fill the base ingredient and tag
``` docker-compose exec python manage.py load_ingredient ```
``` docker-compose exec python manage.py create_tag ```
### Author
Veselov Timofey
vestimofey@mail.ru