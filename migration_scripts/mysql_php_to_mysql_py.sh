sudo cp ~/semester1/mysql_payroll_app.py /var/www/cgi-bin/payroll_app.py
sudo rm /var/www/html/payroll_app.php
sudo updatedb

echo "$(date)   -->    MySQL, Python"
echo "$(date)   -->    MySQL, Python" >> ~/configuration_log.txt
