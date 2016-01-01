FROM nginx

RUN mkdir -p /var/www

ADD api_backend /var/www/api_backend
ADD requirements.txt /
ADD start.sh /
ADD api_backend.conf /etc/nginx/conf.d/
ADD api_backend.ini /var/www/api_backend/

RUN apt-get update
RUN apt-get install -y python-dev python-pip
RUN pip install -r /requirements.txt

EXPOSE 8888

CMD ["sh", "/start.sh"]
