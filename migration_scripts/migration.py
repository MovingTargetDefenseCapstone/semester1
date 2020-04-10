import random
import os

migrations = [["NONE", "mysql_php_to_pg_php.sh", "mysql_php_to_mysql_py.sh", "mysql_php_to_pg_py.sh"], 
["pg_php_to_mysql_php.sh", "NONE", "pg_php_to_mysql_py.sh", "pg_php_to_pg_py.sh"], 
["mysql_py_to_mysql_php.sh", "mysql_py_to_pg_php.sh", "NONE", "mysql_py_to_pg_py.sh"],
["pg_py_to_mysql_php.sh", "pg_py_to_pg_php.sh", "pg_py_to_mysql_py.sh", "NONE"]]

current = 0
for i in range(10):
	rand_ind = random.randrange(4)
	mig = migrations[current][rand_ind]
	while (mig == "NONE"):
		rand_ind = random.randrange(4)
		mig = migrations[current][rand_ind]
	print(mig)
	current = rand_ind
	os.system("sleep 2s")
