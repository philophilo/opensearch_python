FROM python:alpine3.16

WORKDIR /app

COPY . /app

RUN rm certs/* config/*

RUN pip install -r requirements.txt

CMD ["/bin/sh", "-c", "/app/script-prod.sh"]