# numpy requires python 3.5, which may make attacks invalid, so we may need to make slight chagtes to choosing j

# file takes number of defender migrations as command line argument
# need to install numpy on defender for this to work
from numpy.random import choice
import time
import subprocess
import sys
P = [[0.2, 0.4, 0.2, 0.2],
     [0.3, 0.1, 0.1, 0.5],
     [0.2, 0.5, 0.2, 0.1],
     [0.2, 0.1, 0.7, 0.0]]

T = [3, 4, 3, 5]

names = {0: 'mysql_php', 1: 'mysql_py', 2:'pg_php', 3:'pg_py'}

def move_defender(tau, i):
    # wait tau seconds
    time.sleep(tau)
    
    # get next state
    j = choice([0, 1, 2, 3], 1, p=P[i])[0]
    
    command = './' + names[i] + '_to_' + names[j] + '.sh'
    m = subprocess.run([command], capture_output=True, text=True)
    
    if 'ERROR' in m.stdout:
        subprocess.run(['sudo mv /var/run/mysql-default /var/run/mysqld'])
        subprocess.run([command])
        
    return j

if __name__=='__main__':
    time_periods = int(sys.argv[1])
    i = 0
    while time_periods > 0:
        i = move_defender(T[i], i)
        time_periods -= 1
