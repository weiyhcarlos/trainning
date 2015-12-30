FROM nginx

RUN mkdir -p /var/www

ADD data_interface /var/www/data_interface
ADD requirements.txt /
ADD start.sh /
ADD data_interface.conf /etc/nginx/conf.d/
ADD data_interface.ini /var/www/data_interface/

RUN apt-get update
RUN apt-get install -y python-dev python-pip
RUN pip install -r /requirements.txt

EXPOSE 4567


