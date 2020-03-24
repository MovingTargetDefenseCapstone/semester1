sudo mv /var/run/mysql-default /var/run/mysqld
mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -u root payroll -p 
# enter sploitme as password
wget https://raw.github.com/lanyrd/mysql-postgresql-converter/master/db_converter.py
chmod +rx db_converter.py
sudo apt-get install postgresql-9.3
python db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll
# one more command needed
sudo nano /etc/postgresql/9.3/main/pg_hba.conf  # everywhere it says peer change to trust
sudo service postgresql restart # try doing this before the previous step to see if it works
psql payroll -U postgres 


# code to chane ip address
sudo ifconfig eth0 xxx.xxx.xx.xx
