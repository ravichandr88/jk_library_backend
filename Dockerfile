# pull python image
FROM python:3.11-alpine3.19

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2

COPY . .

# CMD ["/bin/bash", "-c", "source entrypoint.sh"]
# CMD python3 manage.py migrate
# gunicorn library_backend.wsgi:application --bind 0.0.0.0:8000
CMD ["python3", "manage.py", "migrate", "&&", "gunicorn", "library_backend.wsgi:application", "--bind 0.0.0.0:8000"]
# ENTRYPOINT  [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]