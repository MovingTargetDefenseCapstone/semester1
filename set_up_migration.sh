sudo mv /var/run/mysql-default /var/run/mysqld
sudo apt-get -y install postgresql-9.3
sudo chmod -rw ~/semester1/my_pg_hba.conf
sudo cp ~/semester1/my_pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
sudo chmod +rw ~/semester1/my_pg_hba.conf
sudo service postgresql restart
sudo apt-get -y install phpmyadmin # select apache2, enter Y, select No
sudo apt-get -y install php5-pgsql
sudo apt-get -y install python-pip
sudo pip install mysql-connector-python
sudo cp ~/semester1/my-serve-cgi-bin.conf /etc/apache2/conf-available/serve-cgi-bin.conf
sudo cp ~/semester1/my-apache2.conf /etc/apache2/apache2.conf
sudo service apache2 restart
sudo apt-get install python2.7-dev libmysqlclient-dev
sudo pip install psycopg2
