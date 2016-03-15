FROM nginx

RUN mkdir -p /var/www

ADD code /var/www/data_interface
ADD misc/requirements.txt /
ADD misc/start.sh /
ADD misc/data_interface.conf /etc/nginx/conf.d/
ADD misc/data_interface.ini /var/www/data_interface/

ENV C_FORCE_ROOT true

RUN apt-get update
RUN apt-get install -y python-dev python-pip
RUN pip install -r /requirements.txt

EXPOSE 4567

CMD ["sh", "/start.sh"]
