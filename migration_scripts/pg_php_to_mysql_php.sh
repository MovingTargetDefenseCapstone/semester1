# create mysql database
mysql -uroot -psploitme -e "CREATE DATABASE payroll;" 
mysql -uroot -psploitme payroll < ~/semester1/add_rows_to_users.mysql
sudo cp ~/semester1/mysql_payroll_app.php /var/www/html/payroll_app.php

# drop postgres database
sudo -u postgres dropdb payroll

sudo updatedb

echo "$(date)   -->    MySQL, PHP"
echo "$(date)   -->    MySQL, PHP" >> ~/configuration_log.txt
