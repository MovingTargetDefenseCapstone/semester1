mysqldump --compatible=postgresql --default-character-set=utf8 -r payroll.mysql -u root payroll -p sploitme
python db_converter.py payroll.mysql payroll.psql
sudo -u postgres createdb payroll

