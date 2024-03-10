FROM ubuntu
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils RUN apt-get -y install python3 libapache2-mod-wsgi-py3 
RUN ln /usr/bin/python3 /usr/bin/python 
RUN apt-get -y install python3-pip RUN ln /usr/bin/pip3 /usr/bin/pip RUN pip install --upgrade pip 
RUN pip install django ptvsd ADD ./site-config.conf /etc/apache2/sites-available/000-default.conf ADD ./requirements.txt /var/www/html WORKDIR /var/www/html 
RUN pip install -r requirements.txt 
RUN chmod 775 /var/www/html/escalasv1/logs 
RUN chown :www-data /var/www/html/escalasv1/logs 
EXPOSE 80 3500 
CMD ["apache2ctl", "-D", "FOREGROUND"]