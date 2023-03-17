# syntax=docker/dockerfile:1

FROM python:3.10.10-bullseye

WORKDIR /var/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /var/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /var/app

CMD [ "python3" "-m", "flask", "db", "upgrade" ]
CMD [ "python3", "app.py" ]