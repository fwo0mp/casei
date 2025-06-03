FROM python:3.11-slim

# these libs are needed for psycopg2
RUN apt-get update && apt-get -y install gcc libpq-dev uwsgi uwsgi-plugin-python3

WORKDIR /casei
#COPY environment .
COPY pyproject.toml uv.lock .

# set up python env first so that application code changes don't require a full rebuild
#RUN pip install --upgrade pip && pip install pipenv && pipenv install
RUN pip install --upgrade pip && pip install uv && uv sync

COPY src .
COPY uwsgi/casei.uwsgi.ini .

#RUN pipenv run python3 manage.py collectstatic --noinput
RUN uv run manage.py collectstatic --noinput

CMD ["uv", "run", "uwsgi", "--ini", "casei.uwsgi.ini"]