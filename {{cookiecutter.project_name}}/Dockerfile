FROM python:3.8

RUN apt-get -qq update
RUN pip install --upgrade pip && pip install pip-tools
RUN apt-get install -y --no-install-recommends g++

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 7000
CMD gunicorn wsgi:app -b  0.0.0.0:7000 --workers=1 --preload
