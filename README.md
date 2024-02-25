# Online-Store-Project

Quickstart:

1. Start docker on your local machine and use "docker-compose up -d"
   Then type "docker-compose exec web python manage.py migrate"
2. Open http://127.0.0.1:8000/ to try it out

   Also, you can check admin panel

   To do this:

   1. Type "docker-compose exec web manage.py createsuperuser", then enter all required data
   2. Open http://127.0.0.1:8000/admin and enter by using email from step 1
   3. Enjoy
