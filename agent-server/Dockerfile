FROM nginx

RUN mkdir -p /var/www

ADD . /var/www/api_backend
ADD misc/requirements.txt /
ADD misc/start.sh /
ADD misc/api_backend.conf /etc/nginx/conf.d/
ADD misc/api_backend.ini /var/www/api_backend/

RUN apt-get update
RUN apt-get install -y python-dev python-pip
RUN pip install -r /requirements.txt

EXPOSE 8888

CMD ["sh", "/start.sh"]
