# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 12:52:00 2019

@author: Henger
"""

from gurobipy import *
import numpy


import numpy
def get_a(ES,tau):
    sum = 0
    for i in range(1000):
        sum = sum + max(tau-numpy.random.exponential(1.0/ES, None),0)
    a=sum/1000        
    return a

def get_data():
    
    data=[]
    f = open('input.txt', 'r')
    #f=open('3_layer.txt','r')
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
                #print(scores)
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
    
    data_new=get_data()
    for l in range(data_new[1]):
        
        R=data_new[5+l*6]
        C=data_new[6+l*6]
        E=data_new[7+l*6]
        # Add attacking time
        #f0=open('eta.txt','w')
        for i in range(data_new[0]):
            for j in range(data_new[3+l*6]):
                eta=get_a(E[i][j],tau)
                #f0.write(str(eta))
                #f0.write(', ')
                R[i][j]=R[i][j]*eta
                C[i][j]=C[i][j]*eta   
        
        #f0.close()
        data_new[5+l*6]=R
        data_new[6+l*6]=C
        
    return data_new

def process_data(tau_min, tau_max, delta):
    datas = []
    for tau in range(1+int((tau_max-tau_min)/delta)):
        datas.append(renew_data(tau_min+tau*delta))
    
    return datas




def URG(alpha, tau, data):
    #Create a new model
    m = Model("MILP")
    
    #f= open('data3.txt','r')
    #if layer == 1:
        #f = open('1-layer.txt', 'r')
    #else layer == 2:
     #   f = open('2-layer.txt', 'r')
    #else:
      #  f = open('3-layer.txt', 'r')
    # Add defender stategies to the model
    #X = int(f.readline())
    X=data[0]
    
    
    update_cost = 1.5 # cost of staying in place and updating machine
    cost = [[update_cost, 0.101, 0.588, 0.612],
            [0.103, update_cost, 0.606, 0.565],
            [.443, 2.584, update_cost, 0.108],
            [2.409, 2.449, 0.105, update_cost]]

    # subtract costs from the objective function
    obj = QuadExpr()

    #alpha = 1
    for i in range(X):
        for j in range(X):
            obj.add( alpha * cost[i][j]/(X*X), -1)
            #two_step_configs.add( w[i][j] )
    #m.addConstr( two_step_configs == 1 ) 

    ''' Start processing for attacker types '''
    #L = int(f.readline())
    L=data[1]
    M = 100000000

    for l in range(L):

        # Probability of l-th attacker
        #v = f.readline().strip()
        #p = float(v)
        p=data[2+l*6]
        # Add l-th attacker info to the model
        #Q = int(f.readline())
        Q=data[3+l*6]
        q = []
        #cve_names = f.readline().strip().split("|")
        cve_names=data[4+l*6]
        for i in range(Q):
            n = str(l)+'-'+cve_names[i]
            q.append(m.addVar(lb=0, ub=1, vtype=GRB.INTEGER, name=n))

        a = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="a-"+str(l))

        m.update()
        
        R=data[5+l*6]
        C=data[6+l*6]
        # Update objective function
        for i in range(X):
            for j in range(Q):
                r = p * float(R[i][j])
                obj.add( r * 1/X * q[j] )

        # Add constraints to make attaker have a pure strategy
        con = LinExpr()
        for j in range(Q):
            con.add(q[j])
        m.addConstr(con==1)

        # Add constrains to make attacker select dominant pure strategy
        for j in range(Q):
            val = LinExpr()
            val.add(a)
            for i in range(X):
                val.add( float(C[i][j]) * 1/X, -1.0)
            m.addConstr( val >= 0, q[j].getAttr('VarName')+"lb" )
            m.addConstr( val <= (1-q[j]) * M, q[j].getAttr('VarName')+"ub" )

    # Set objective funcion as all attackers have now been considered
    m.setObjective(obj, GRB.MAXIMIZE)

    # Solve MIQP
    m.optimize()


    return -m.objVal/tau

def URG_tau(alpha, datas, tau_min, tau_max, delta):
    v=[]
    for i in range(1+int((tau_max-tau_min)/delta)):
        v.append(URG(alpha, i*delta+tau_min, datas[i]))
    return min(v)

v=[]
tau_min = 5
tau_max = 30
delta = 5
data = get_data()
datas = process_data(tau_min, tau_max, delta)
f = open('URG_costs.txt','w+')
#f0=open('URG.txt','w')
#f1=open('URG_tau.txt','w')
num_alpha = 10
alpha_coef = 10
costs = ''
for alpha in range(num_alpha):
    r=URG_tau(alpha*alpha_coef, datas, tau_min, tau_max, delta)
    #r=URG((alpha+1)*alpha_coef, 1.0, data)
    print(r)
    costs = costs + str(r) + '\n'
    #obj=min(r)
    #v.append(r)
    #f1.write(str(r.index(obj)*delta+tau_min))
    #f1.write('\n')

#f0.write(str(r))
f.write(str(costs))
#f0.close()
#f1.close()