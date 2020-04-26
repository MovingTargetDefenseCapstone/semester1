sudo cp ~/semester1/postgres_payroll_app.php /var/www/html/payroll_app.php
sudo rm /var/www/cgi-bin/payroll_app.py

sudo updatedb

echo "$(date)   -->    PostgreSQL, PHP"
echo "$(date)   -->    PostgreSQL, PHP" >> ~/configuration_log.txt
