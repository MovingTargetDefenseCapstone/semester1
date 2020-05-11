# file takes number of defender migrations as command line argument
import time
import sys
import random
import os

os.system('sudo mv /var/run/mysql-default /var/run/mysqld')

P = [[0.2, 0.4, 0.2, 0.2],
     [0.3, 0.1, 0.1, 0.5],
     [0.2, 0.5, 0.2, 0.1],
     [0.2, 0.1, 0.7, 0.0]]

T = [3, 4, 3, 5]

names = {0: 'mysql_php', 1: 'mysql_py', 2:'pg_php', 3:'pg_py'}

def make_choice(choices):
   total_weight = sum(weight for choice, weight in choices)
   rand_val = random.uniform(0, total_weight)
   cutoff = 0
   for choice, weight in choices:
      if cutoff + weight >= rand_val:
         return choice
      cutoff += weight

def move_defender(tau, i):
    # wait tau seconds
    time.sleep(tau)
    
    # combine P and choices
    pchoices = [(0, P[i][0]), (1, P[i][1]), (2, P[i][2]), (3, P[i][3])]
	
    # get next state
    j = make_choice(pchoices)    

    command = './' + names[i] + '_to_' + names[j] + '.sh'
    os.system(command)
    
    return j

if __name__=='__main__':
    time_periods = int(sys.argv[1])
    i = 0
    while time_periods > 0:
        i = move_defender(T[i], i)
        time_periods -= 1
