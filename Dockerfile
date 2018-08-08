FROM python:3.7

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server

COPY . /var/app/
WORKDIR /var/app

RUN pip3.7 install -r requirements.txt

ENV MYSQL_DATABASE=facebook_messenger \
    MYSQL_USER=jeremy \
    MYSQL_PASSWORD=password \
    MYSQL_PORT=3306 \
    MYSQL_HOST=fbm_db \
    MYSQL_ROOT_PASSWORD=password

ENTRYPOINT ["bash", "-c"]
CMD ["/var/app/entrypoint.sh"]