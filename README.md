# foodgram-project
### Description
Website where you can publish recipes, subscribe to publications of other users, as well as download a summary list of products required for the preparation of one or more selected dishes.
[Link to website!](http://178.154.213.197/)
Admin: Timofey
Password: haLo3V1q
### Technologies
- Python 3.9
- Django 3.2.3
- PostgreSQL 13.3
- Gunicorn 20.1.0
- Nginx 1.21.0
- Docker 20.10.5
### Launch project in dev-mode
- Install and activate virtual environment
- Install dependency from requrements.txt
``` pip install -r requirements.txt ```
- Collect static files
``` python manage.py collectstatic ```
- To filling the base
``` python manage.py load_ingredient ```
``` python manage.py create_tag ```
- Run local server
``` python manage.py run server ```
### Application launch
``` docker-compose up -d ```
### Creating superuser
``` docker-compose exec python manage.py createsuperuser ```
### To filling the base 
``` docker-compose exec python manage.py load_ingredient ```
``` docker-compose exec python manage.py create_tag ```
### Author
Veselov Timofey
vestimofey@mail.ru