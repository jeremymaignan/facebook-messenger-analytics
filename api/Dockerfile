FROM python:3.7

ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=0

COPY . /var/app/api/
WORKDIR /var/app/api/

EXPOSE 5000

WORKDIR /var/app/api/

RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "-c"]
CMD ["/var/app/api/entrypoint.sh"]