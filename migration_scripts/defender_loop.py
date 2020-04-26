# file takes number of defender migrations as command line argument
import time
import sys
import random
import os
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
    j = random.choice([0, 1, 2, 3])
    
    command = './' + names[i] + '_to_' + names[j] + '.sh'
    os.system(command)
    
    return j

if __name__=='__main__':
    time_periods = int(sys.argv[1])
    i = 0
    while time_periods > 0:
        i = move_defender(T[i], i)
        time_periods -= 1
