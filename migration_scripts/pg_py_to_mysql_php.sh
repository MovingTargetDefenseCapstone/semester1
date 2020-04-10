# create mysql database
mysql -uroot -psploitme -e "CREATE DATABASE payroll;" 
mysql -uroot -psploitme payroll < ~/payroll.mysql
sudo cp ~/semester1/mysql_payroll_app.php /var/www/html/payroll_app.php
sudo rm /var/www/cgi-bin/payroll_app.py

# drop postgres database
sudo -u postgres dropdb payroll

echo "$(date)   -->    MySQL, PHP"
echo "$(date)   -->    MySQL, PHP" >> ~/configuration_log.txt
