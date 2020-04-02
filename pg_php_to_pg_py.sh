sudo cp ~/semester1/postgres_payroll_app.py /var/www/cgi-bin/payroll_app.py
sudo rm /var/www/html/payroll_app.php

echo "$(date)   -->    Postgresql, Python" >> ~/configuration_log.txt
