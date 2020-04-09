# create postgres database
mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -uroot payroll -psploitme
python ~/semester1/db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll
psql payroll -U postgres -f payroll.psql
sudo cp ~/semester1/postgres_payroll_app.py /var/www/cgi-bin/payroll_app.py
sudo rm /var/www/html/payroll_app.php


# drop mysql database
mysql -uroot -psploitme -e "DROP DATABASE payroll;"

echo "$(date)   -->    Postgresql, Python"
echo "$(date)   -->    Postgresql, Python" >> ~/configuration_log.txt
