#!/bin/bash

# build postgres database
sudo mv /var/run/mysql-default /var/run/mysqld
mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -uroot payroll -psploitme 
sudo apt-get -y install postgresql-9.3 
python ~/semester1/db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll
sudo chmod -rw ~/semester1/my_pg_hba.conf
sudo cp ~/semester1/my_pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
sudo chmod +rw ~/semester1/my_pg_hba.conf
sudo service postgresql restart
psql payroll -U postgres -f payroll.psql

# drop mysql payroll database
mysql -uroot -psploitme -e "DROP DATABASE payroll;"

# rebuild mysql database
mysql -uroot -psploitme -e "CREATE DATABASE payroll;" 
mysql -uroot -psploitme payroll < payroll.mysql
sudo cp ~/semester1/mysql_payroll_app.php /var/www/html/payroll_app.php

# code to change ip address
# sudo ifconfig eth0 xxx.xxx.xx.xx
