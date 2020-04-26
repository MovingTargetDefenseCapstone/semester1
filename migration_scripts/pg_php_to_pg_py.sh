sudo cp ~/semester1/postgres_payroll_app.py /var/www/cgi-bin/payroll_app.py
sudo rm /var/www/html/payroll_app.php

sudo updatedb

echo "$(date)   -->    PostgreSQL, Python"
echo "$(date)   -->    PostgreSQL, Python" >> ~/configuration_log.txt
