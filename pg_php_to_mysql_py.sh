# create mysql database
mysql -uroot -psploitme -e "CREATE DATABASE payroll;" 
mysql -uroot -psploitme payroll < payroll.mysql
sudo cp ~/semester1/mysql_payroll_app.py /var/www/cgi-bin/payroll_app.py
sudo rm /var/www/html/payroll_app.php

# drop postgres database
sudo -u postgres dropdb payroll

echo "$(date)   -->    MySQL, Python"
echo "$(date)   -->    MySQL, Python" >> ~/configuration_log.txt
