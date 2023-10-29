FROM python:3.10-slim

# these libs are needed for psycopg2
RUN apt-get update && apt-get -y install gcc libpq-dev uwsgi uwsgi-plugin-python3

WORKDIR /casei
COPY environment .

# set up python env first so that application code changes don't require a full rebuild
RUN pip install --upgrade pip && pip install pipenv && pipenv install

COPY src .
COPY uwsgi/casei.uwsgi.ini .

RUN pipenv run python3 manage.py collectstatic --noinput

CMD ["pipenv", "run", "uwsgi", "--ini", "casei.uwsgi.ini"]