mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -u root payroll -p sploitme
wget https://raw.github.com/lanyrd/mysql-postgresql-converter/master/db_converter.py
chmod +rx db_converter.py
sudo apt-get install postgresql-9.3
python db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll

