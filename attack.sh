TARGET=$1
SOURCE=$2
NUM=$3

COUNT=0
VAL=0
while [ $COUNT -lt $NUM ]
do
	if [ $VAL -eq 0 ]
	then 
		./attacker.sh CVE-2015-3306 $TARGET $SOURCE
		VAL=1
	elif [ $VAL -eq 1 ]
	then
		./attacker.sh CVE-2010-2075 $TARGET $SOURCE
		VAL=0
	fi
	COUNT=$(($COUNT + 1))
done

