# -*- coding: utf-8 -*-
"""

@author: Henger Li

Minor changes were made by Thomas Roginsky
"""

from gurobipy import *
import numpy as np
import time
import multiprocessing as mp
import math
import sys

#Parameters

num_simulation = 1000
tau_min = float(sys.argv[1])
tau_max = float(sys.argv[2])
delta = float(sys.argv[3])
e=0.01
taus = [tau_min+ i*delta for i in range (1+int((tau_max-tau_min)/delta))]
num_alpha = 10
alpha_coef = float(sys.argv[4])
#alpha_min = 0.1
#alpha_max = 1.1


#Multiprocessing alpha loop
def msgIterators():
    mydatas = process_data()
    for i in range(num_alpha):
        yield ([i*alpha_coef, mydatas])

gamma = tau_min
M = 100000000

update_cost = 1.5 # cost of staying in place and updating machine
Cost = [[update_cost, 0.101, 0.588, 0.612],
        [0.103, update_cost, 0.606, 0.565],
        [.443, 2.584, update_cost, 0.108],
        [2.409, 2.449, 0.105, update_cost]]



#Input and Output file
S = len(Cost)
data_file = 'input.txt'
output_msg = 'MSG.txt'
output_tau = 'MSG_tau.txt'
output_p = 'MSG_P.txt'
output_t = 'MSG_t.txt'
output_v = 'MSG_V.txt'





def processMSGJobs(i):
    onealphas = []
    t = SMSG(i[0], i[1])
    onealphas.append(t)
    return onealphas


#Attacking time simulation
def get_a(ES,tau):
    temp_a = tau*np.ones(num_simulation) - np.random.exponential(1.0/ES, num_simulation)
    temp_b = np.maximum(temp_a, np.zeros(num_simulation))
    return np.average(temp_b)

#Reading data from input file and store it for all alphas
def get_data():

    data=[]
    f = open(data_file, 'r')
    X = int(f.readline())
    data.append(X)
    L = int(f.readline())
    data.append(L)

    for l in range(L):
        v = f.readline().strip()
        p = float(v)
        data.append(p)
        Q = int(f.readline())
        data.append(Q)
        cve_names = f.readline().strip().split("|")
        data.append(cve_names)

        # Get reward for attacker and defender
        R = []
        C = []
        E = []
        for i in range(X):
            rewards = f.readline().split()
            r = []
            c = []
            e = []
            for j in range(Q):
                scores = rewards[j].split(",")
                r.append(float(scores[0]))
                c.append(float(scores[1]))
                e.append(float(scores[2]))
            R.append(r)
            C.append(c)
            E.append(e)

        data.append(R)
        data.append(C)
        data.append(E)

    return data

def renew_data(tau):

    data_new = get_data()
    for l in range(data_new[1]):

        R=data_new[5+l*6]
        C=data_new[6+l*6]
        E=data_new[7+l*6]
        # Add attacking time
        for i in range(data_new[0]):
            for j in range(data_new[3+l*6]):
                eta = get_a(E[i][j],tau)
                #eta=1
                R[i][j]=R[i][j]*eta
                C[i][j]=C[i][j]*eta

        data_new[5+l*6]=R
        data_new[6+l*6]=C

    return data_new

def process_data():
    datas = []
    for tau in taus:
        datas.append(renew_data(tau))

    return datas


#Solving the bilevel problem
def MinMax(i,V,alpha,tau, data):
    try:
        #Create a new model
        m = Model("MIQP")

        X=data[0]
        x = []
        for j in range(X):
            n = "x-"+str(j)
            x.append(m.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name=n))
        m.update()

        # Add defender stategy constraints
        con = LinExpr()
        for j in range(X):
            con.add(x[j])
        m.addConstr(con==1)
        m.update()
        obj = QuadExpr()



        for j in range(X):
            obj.add((alpha*Cost[i][j]+gamma*V[j])*x[j])
        
        obj.add((tau-gamma)*V[i])
        L=data[1]


        for l in range(L):

            # Probability of l-th attacker
            p=data[2+l*6]

            # Add l-th attacker info to the model
            Q=data[3+l*6]
            q = []
            cve_names=data[4+l*6]

            for k in range(Q):
                n = str(l)+'-'+cve_names[k]
                q.append(m.addVar(vtype=GRB.BINARY, name=n))

            a = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="a-"+str(l))
            m.update()

            R=data[5+l*6]
            C=data[6+l*6]
            # Update objective function
            for j in range(X):
                for k in range(Q):
                    r = abs(p * float(R[j][k]))
                    obj.add(r * x[j] * q[k])
            

            # Add constraints to make attaker have a pure strategy
            con = LinExpr()
            for j in range(Q):
                con.add(q[j])
            m.addConstr(con==1)

            # Add constrains to make attacker select dominant pure strategy
            for k in range(Q):
                val = LinExpr()
                val.add(a)

                for j in range(X):
                    val.add( float(C[j][k]) * x[j], -1.0)

                m.addConstr( val >= 0.0, q[k].getAttr('VarName')+"lb" )
                m.addConstr( val <= (1.0-q[k]) * M, q[k].getAttr('VarName')+"ub")

        m.setObjective(obj, GRB.MINIMIZE)

        # Solve MIQP
        m.optimize()

        result=[]
        result.append(m.objVal/tau)

        for v in m.getVars()[0:S]:
            result.append(v.x)
            

        return result

    except GurobiError:
        print('Error reported')

#Relative Value Iteration for MTD
def SMSG(alpha, datas):

    t=0
    V= np.zeros(S)
    V0= np.zeros(S)
    V_max= 10.0
    V_min= 0.0
    kappa= 0.5
    W=np.zeros(S)
    fix=0
    
    
    while V_max-V_min >= e:
        for i in range(S):
            V0[i]=V[i]
        t=t+1
        W=V0-V0[fix]*np.ones(S)
        W=kappa*W
        f2 = []
        f1 = []
        
        for i in range(S):
            tau_index = 0
            opt_v = float("inf")
            opt_w = []
            opt_tau = -1.0
            for tau in taus:
                r=MinMax(i,W,alpha,tau,datas[tau_index])
                if r[0] < opt_v:
                    opt_v = r[0]
                    opt_w = r[1:5]
                    opt_tau = tau
                tau_index +=1
            V[i]=opt_v
            f2.append(str(opt_w))
            f1.append(str(opt_tau))

        f4 = []
        f4.append("V= "+str(V)+" V0= "+str(V0))
        V_max = max(V-V0)
        V_min = min(V-V0)
        kappa= t/(1+t)
            
    f3 = []
    f3.append(str(t))
    
    return [str(V[fix]), f1, f2, f3, f4]





if __name__=='__main__':

    # paralell computing
    pool = mp.Pool(mp.cpu_count())
    t0 = time.time()
    alphas = pool.map(processMSGJobs, msgIterators())
    t1 = time.time()
    print ("******Total operation time*******: "+str(t1-t0))
    all_results = [ent for sublist in alphas for ent in sublist]
    pool.close()
    pool.join()

    # write data to files
    f_msg=open(output_msg,'w+')
    f_tau=open(output_tau,'w+')
    f_p=open(output_p,'w+')
    f_t=open(output_t,'w+')
    f_v = open(output_v, 'w+')

    for i in all_results:
        a_msg = i[0]
        a_tau = i[1]
        a_p = i[2]
        a_t = i[3]
        a_v = i[4]
        f_msg.write(str(a_msg)+'\n')
        f_tau.write(str(a_tau)+ '\n')
        f_p.write(str(a_p)+'\n')
        f_t.write(str(a_t)+'\n')
        f_v.write(str(a_v) +'\n')
        
        

    
    f_msg.close()
    f_msg.close()
    f_tau.close()
    f_p.close()
    f_t.close()
    f_v.close()

    