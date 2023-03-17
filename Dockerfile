# syntax=docker/dockerfile:1

FROM python:3.10.10-bullseye

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD [ "python3" "-m", "flask", "db", "upgrade", "&&", "python3", "app.py" ]