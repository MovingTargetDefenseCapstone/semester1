# create postgres database
mysqldump --compatible=postgresql --default-character-set=utf8 -r ~/payroll.mysql -uroot payroll -psploitme
python ~/semester1/db_converter.py ~/payroll.mysql ~/payroll.psql
sudo -u postgres createdb payroll
psql payroll -U postgres -f ~/payroll.psql
sudo cp ~/semester1/postgres_payroll_app.php /var/www/html/payroll_app.php
sudo rm /var/www/cgi-bin/payroll_app.py

# drop mysql database
mysql -uroot -psploitme -e "DROP DATABASE payroll;"

echo "$(date)   -->    Postgresql, PHP"
echo "$(date)   -->    Postgresql, PHP" >> ~/configuration_log.txt
