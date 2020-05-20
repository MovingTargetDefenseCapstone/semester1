# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:58:27 2019

@author: Henger

Minor changes were made by Thomas Roginsky
"""

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
    #f=open('3_layer.txt', 'r')
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

#def renew_data(data, tau):
def renew_data(tau):    
    #data_new=data
    data_new = get_data()
    
    for l in range(data_new[1]):
        
        R=data_new[5+l*6]
        C=data_new[6+l*6]
        E=data_new[7+l*6]
        
        # Add attacking time
        for i in range(data_new[0]):
            for j in range(data_new[3+l*6]):
                eta=get_a(E[i][j],tau)
                
                R[i][j]=R[i][j]*eta
                C[i][j]=C[i][j]*eta   
        
        #fe.close()
        data_new[5+l*6]=R
        data_new[6+l*6]=C
        
    return data_new

def process_data(tau_min, tau_max, delta):
    datas = []
    for tau in range(1+int((tau_max-tau_min)/delta)):
        datas.append(renew_data(tau_min+tau*delta))
    return datas


from gurobipy import *
import numpy

def BSG(alpha,tau, data):
    #Create a new model
    m = Model("MIQP")

    # Add defender stategies to the model
    X=data[0]
    x = []
    for i in range(X):
        n = "x-"+str(i)
        x.append(m.addVar(lb=0, ub=1, vtype=GRB.CONTINUOUS, name=n))
    m.update()

    # Add defender's switching cost
    update_cost = 1.5 # cost of staying in place and updating machine
    cost = [[update_cost, 0.101, 0.588, 0.612],
            [0.103, update_cost, 0.606, 0.565],
            [.443, 2.584, update_cost, 0.108],
            [2.409, 2.449, 0.105, update_cost]]

    
    
    
    # Add defender stategy constraints
    con = LinExpr()
    for i in range(X):
        con.add(x[i])
    m.addConstr(con==1)
    m.update()

    # Add transition cost variables
    w = []
    to_config_constr = [LinExpr() for i in range(X)]
    for i in range(X):
        _w = []
        from_config_constr = LinExpr()
        for j in range(X):
            n = "w-"+str(i)+str(j)
            temp = m.addVar(vtype=GRB.CONTINUOUS, name=n)
            # Use McCormick_envelopes to find upper and lower bounds for the
            # non-convex function x_i * x_j
            if i == j:
                m.addConstr(temp == 0)
            else:
                m.addConstr(temp >= 0)
                m.addConstr(temp >= x[i]+x[j]-1)
                m.addConstr(temp <= x[i])
                m.addConstr(temp <= x[j])
            _w.append(temp)
            from_config_constr.add( temp )
            to_config_constr[j].add( temp )
        m.addConstr(from_config_constr == x[i])
        w.append(_w)

    for i in range(X):
        m.addConstr(to_config_constr[i] == x[i])

    m.update()

    # subtract costs from the objective function
    obj = QuadExpr()
    two_step_configs = LinExpr()
    for i in range(X):
        for j in range(X):
            obj.add( alpha * cost[i][j] * w[i][j], -1)
            two_step_configs.add( w[i][j] )
    m.addConstr( two_step_configs == 1 ) 

    ''' Start processing for attacker types '''
    L = data[1]
    M = 100000000

    for l in range(L):

        # Probability of l-th attacker
        
        p=data[2+l*6]

        # Add l-th attacker info to the model
        Q=data[3+l*6]
        q = []
        cve_names=data[4+l*6]
        
        for i in range(Q):
            n = str(l)+'-'+cve_names[i]
            q.append(m.addVar(lb=0, ub=1, vtype=GRB.INTEGER, name=n))

        a = m.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="a-"+str(l))

        m.update()
        
        R=data[5+l*6]
        C=data[6+l*6]
        
        for i in range(X):
            for j in range(Q):
                r = p * float(R[i][j])
                obj.add( r * x[i] * q[j] )

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
                val.add( float(C[i][j]) * x[i], -1.0)
            m.addConstr( val >= 0, q[j].getAttr('VarName')+"lb" )
            m.addConstr( val <= (1-q[j]) * M, q[j].getAttr('VarName')+"ub" )

    # Set objective funcion as all attackers have now been considered
    m.setObjective(obj, GRB.MAXIMIZE)

    # Solve MIQP
    m.optimize()

    results=[]
    results.append(-m.objVal/tau)
    
    for v in m.getVars()[0:X]:
        results.append(v.x)

    return results

def BSG_tau(alpha, datas, tau_min, tau_max, delta):
    v=[]
    w=[]
    results=[]
    for i in range(1+int((tau_max-tau_min)/delta)):
        r=BSG(alpha,i*delta+tau_min, datas[i])
        w.append(r[1:9])
        v.append(r[0])
    
    obj=min(v)
    results.append(obj)
    idx = v.index(obj)
    tau = idx*delta+tau_min
    results.append(tau)
    p = w[idx]
    results.append(p)
    return results

v=[]
tau_min = 5
tau_max = 30
delta = 5
data = get_data()
datas = process_data(tau_min, tau_max, delta)
f = open('BSG_costs.txt','w+')
f0 = open('uBSG.txt','w+')
f1 = open('BSG_tau.txt','w+')
f2 = open('uBSG_P.txt','w+')

costs = ''
num_alpha = 10
alpha_coef = 10
for alpha in range(num_alpha):
    r=BSG_tau(alpha*alpha_coef, datas, tau_min, tau_max, delta)
    #r=BSG((alpha+1)*alpha_coef, 1.0, data)
    print("r:")
    print(r)
    v.append(r[0])

    f1.write(str(r[1]))
    f1.write('\n')
    #f2.write(",".join(str(x) for x in r[2]))
    f2.write(str(r[1:data[0]+1]))
    f2.write('\n')


    
    costs = costs + str(r[0]) + '\n'
f.write(str(costs))
f.close()
f0.write(str(v))
f0.close()
f1.close()
f2.close()
