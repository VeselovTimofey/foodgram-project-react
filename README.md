# foodgram-project
### Description
Website where you can publish recipes, subscribe to publications of other users, as well as download a summary list of products required for the preparation of one or more selected dishes.
[Link to docker!](https://hub.docker.com/repository/docker/vestimofey/foodgram)
- Admin: Timofey
- Password: haLo3V1q
### Screenshot
- main page
![main page](https://raw.githubusercontent.com/VeselovTimofey/foodgram-project-react/assets/main_page.bmp)
- registration page
![registration page](https://raw.githubusercontent.com/VeselovTimofey/foodgram-project-react/assets/registration_page.bmp)
- subscribe page
![purchase page](https://raw.githubusercontent.com/VeselovTimofey/foodgram-project-react/assets/purchase_page.bmp)
- purchase list page
![purchase list page](https://raw.githubusercontent.com/VeselovTimofey/foodgram-project-react/assets/purchase_list_page.bmp)
### Technologies
- Python 3.9
- Django 3.2.3
- PostgreSQL 13.3
- Gunicorn 20.1.0
- Nginx 1.21.0
- Docker 20.10.5
### Launch project 
- Pull repository or copy docker-compose.yaml, foodgram_db.dump and nginx folder
- Application launch
``` docker compose up -d ```
- Make migrations
``` docker compose exec foodgram python manage.py migrate ```
### To full base
- To send dumb in postgres container
``` docker cp foodgram_db.dump postgres:/home/ ```
- To full the base(use twice to bring tags to recipes)
``` docker compose exec postgres pg_restore --host "127.0.0.1" --port "5432" --username "Timofey" --password --role "Timofey" --dbname "foodgram_db" --section=pre-data --section=data --section=post-data --verbose "/home/foodgram_db.dump" ```
### Status
Complete.
### Author
Veselov Timofey <br />
vestimofey@mail.ru