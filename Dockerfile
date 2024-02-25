FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $8000

RUN python manage.py migrate

CMD gunicorn --bind :$8000 --workers 2 backend.wsgi