# create postgres database
#mysqldump --compatible=postgresql --default-character-set=utf8 -r ~/payroll.mysql -uroot payroll -psploitme
#python ~/semester1/db_converter.py ~/payroll.mysql ~/payroll.psql
sudo -u postgres createdb payroll
psql payroll -U postgres -f ~/semester1/add_rows_to_users.psql
sudo cp ~/semester1/postgres_payroll_app.php /var/www/html/payroll_app.php

# drop mysql database
mysql -uroot -psploitme -e "DROP DATABASE payroll;"

sudo updatedb

echo "$(date)   -->    Postgresql, PHP"
echo "$(date)   -->    Postgresql, PHP" >> ~/configuration_log.txt
