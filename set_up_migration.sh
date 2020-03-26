sudo mv /var/run/mysql-default /var/run/mysqld
sudo apt-get -y install postgresql-9.3
sudo chmod -rw ~/semester1/my_pg_hba.conf
sudo cp ~/semester1/my_pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
sudo chmod +rw ~/semester1/my_pg_hba.conf
sudo service postgresql restart
sudo apt-get -y install phpmyadmin
sudo apt-get install php5-pgsql
sudo service apache2 restart
