git clone https://github.com/MovingTargetDefenseCapstone/semester1.git
sudo mv /var/run/mysql-default /var/run/mysqld
mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -uroot payroll -psploitme 
wget https://raw.github.com/lanyrd/mysql-postgresql-converter/master/db_converter.py
chmod +rx db_converter.py
sudo apt-get install postgresql-9.3
python db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll
sudo nano /etc/postgresql/9.3/main/pg_hba.conf  # everywhere it says peer change to trust
sudo service postgresql restart # try doing this before the previous step to see if it works
psql payroll -U postgres -f payroll.psql

# drop mysql payroll database
mysql -uroot -psploitme -e "DROP DATABASE payroll;"
sudo cp ~/semester1/mysql_payroll_app.php /var/www/html/payroll_app.php

# rebuild mysql database
mysql -uroot -psploitme -e "CREATE DATABASE payroll;" 
mysql -uroot -psploitme payroll < payroll.mysql

# code to change ip address
sudo ifconfig eth0 xxx.xxx.xx.xx
