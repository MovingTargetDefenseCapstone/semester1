MYSQL_PHP=("NONE" "mysql_php_to_pg_php.sh" "mysql_php_to_mysql_py.sh" "mysql_php_to_pg_py.sh")
PG_PHP=("pg_php_to_mysql_php.sh" "NONE" "pg_php_to_mysql_py.sh" "pg_php_to_pg_py.sh")
MYSQL_PY=("mysql_py_to_mysql_php.sh" "mysql_py_to_pg_php.sh" "NONE" "mysql_py_to_pg_py.sh")
PG_PY=("pg_py_to_mysql_php.sh" "pg_py_to_pg_php.sh" "pg_py_to_mysql_py.sh" "NONE")   

rand_ind=$(python -S -c "import random; print (random.randrange(4))")
MIGRATION=${MYSQL_PHP[rand_ind]}
while [ $MIGRATION == 'NONE' ]
do
	rand_ind=$(python -S -c "import random; print (random.randrange(4))")
	MIGRATION=${MYSQL_PHP[rand_ind]}
done







			
				
				
		

      
