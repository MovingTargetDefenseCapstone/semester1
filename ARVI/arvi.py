"""
Most of this file comes from Henger Li's repo which can be found here:
https://github.com/HengerLi/SPT-MTD/tree/master/RVI_MTD_e%3D0.01

I created the ARVI and individual_state functions based on functions in the sychronous version of this code, as well as making changes to MinMaxARVI.
"""

from gurobipy import *
import numpy as np
import time
import multiprocessing as mp


#Multiprocessing alpha loop
def msgIterators():
    mydatas = process_data()
    for i in range(num_alpha):
        yield ([i*alpha_coef, mydatas, ])

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
        cve_names=data_new[4+l*6]
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
                eta_key = str(l) + "-" + str(i) + "-" + str(j)
                eta_dict[eta_key] = eta

        data_new[5+l*6]=R
        data_new[6+l*6]=C

    return data_new

def process_data():
    datas = []
    for tau in taus:
        datas.append(renew_data(tau))

    return datas


#Solving the bilevel problem
def MinMaxARVI(i, V, alpha, tau, data, g):
    try:
        V = V_global[:]
        
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
        
        # subtract gt-1
        obj.addConstant(-g)
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
        
        # write model to file
        #m.write("a_write.lp")

        return result

    except GurobiError:
        print('Error reported')

# Calculates the P and tau values for a particular defender state
def individual_state(alpha, datas, i):
    returned_p_i = 0
    returned_tau = [0 for x in range(datas[0][0])]
    while V_max.value - V_min.value > e:
        #g = g_global.value
        g = g_global[:]
        V = V_global[:]
        K = K_global[:]
        N = N_global[:]
    
        
        tau_index = 0
        opt_v = float("inf")
        opt_w = []
        opt_tau = -1.0
        opt_tau_index = 0
        for tau in taus:
            r=MinMaxARVI(i,V,alpha,tau,datas[tau_index], g[i])
            if r[0] < opt_v:
                opt_v = r[0]
                opt_w = r[1:5]
                opt_tau = tau
                opt_tau_index = tau_index
            tau_index +=1
                
        opt_data = datas[opt_tau_index]
        X=opt_data[0]
        L=opt_data[1]
        
        # calculate K
        # Right half of objective function.
        K_new = 0
        sum_pm = 0
        for j in range(X):
            pm = opt_w[j] * Cost[i][j]
            sum_pm += pm * K[j]
        
        # Left side of objective function.
        pi_C_sum = 0
        for l in range(L):
            Q=opt_data[3+l*6]
            cve_names=opt_data[4+l*6]
            R=opt_data[5+l*6]
            C=opt_data[6+l*6]
            E=opt_data[7+l*6]
            
            w_C_sum = 0
            for j in range(X):
                
                max_a_index = 0
                # Finding best attack
                for k in range(Q):
                    a = R[j][k]
                    if a < R[j][max_a_index]:
                        max_a_index = k
                        
                unit_cost = C[j][max_a_index]
                exp_score = E[j][max_a_index]
                
                # Calculate attack time
                eta_key = str(l) + "-" + str(j) + "-" + str(k)
                eta = eta_dict[eta_key]
                #eta = get_a(exp_score, opt_tau)
                w_C = eta * unit_cost * opt_w[j]
                w_C_sum += w_C
                
            pi_C_sum += w_C_sum * opt_data[2+l*6]
            
        
        k_p_tilde = 0
        for j in range(X):
            n_delta = int(i == j)
            p_tilde = gamma * ((opt_w[j] - n_delta)/opt_tau) + n_delta
            k_p_tilde += (p_tilde * K[j])
            
        new_K = pi_C_sum + sum_pm + k_p_tilde
                
        # calculate N
        new_N = 0
        sum_p_tilde = 0
        for j in range(X):
            n_delta = int(i == j)
            p_tilde = gamma * ((opt_w[j] - n_delta)/opt_tau) + n_delta
            sum_p_tilde += (p_tilde * N[j])
        new_N = 1 + sum_p_tilde
        
        returned_p_i = opt_w
        returned_tau = opt_tau
        
        if V_max.value - V_min.value > e:
            my_lock.acquire()

            #returned_p_i = opt_w
            #returned_tau = opt_tau
                
            # transmit global variables
            if i != fixed_state_r:
                V_global[i] = opt_v
                K_global[i] = new_K
                N_global[i] = new_N

            else:
                new_g = new_K / new_N
                g_global[i] = new_g
            
        
            V = np.array(V)
            V_new = np.array(V)
            V_new[i] = opt_v
            V_max.value = max(V_new - V)
            V_min.value = min(V_new - V)

            print("*****************") 
            print("i:" + str(i) +
                "\nV1: " + str(V_new) + "\nV0: " + str(V) + 
                "\nV_max: " + str(V_max.value) + "\nV_min: " + str(V_min.value) + "\n")
            print("*****************")


            my_lock.release()

    # returns row i of P*, as well as tau*
    return [returned_p_i, returned_tau]


alpha = 0.1
num_simulation = 1000
tau_min = 1
tau_max = 1
delta = 1
e=0.01
taus = [tau_min+ i*delta for i in range (1+int((tau_max-tau_min)/delta))]

gamma = tau_min
M = 100000000

Cost=[[2,4,8,12],[4,2,11,7],[8,11,2,12],[12,7,12,2]]

#Input and Output file
S = len(Cost)
data_file = 'input.txt'
output_msg = 'MSG.txt'
output_tau = 'MSG_tau.txt'
output_p = 'MSG_P.txt'

msg_out = open(output_msg,'w+')
tau_out = open(output_tau,'w+')
p_out = open(output_p,'w+')

g_global = mp.Array('d', S)
V_global = mp.Array('d', S)
K_global = mp.Array('d', S)
N_global = mp.Array('d', S)
V_max = mp.Value('d', 10.0)
V_min = mp.Value('d', 0.0)
fixed_state_r = 0



eta_dict = {}

# creates lock to be shared between processes;
def init(l):
    global my_lock
    my_lock = l

def ARVI(alpha, datas):
    lock = mp.Lock()
    gVKN_list = [g_global, V_global, K_global, N_global]
    
    # generate arguments for each process
    args_list = ([alpha, datas, i] for i in range(S))
    
    # add lock as global variable to pool
    pool = mp.Pool(mp.cpu_count(), initializer=init, initargs=(lock,))
    t0 = time.time()
    # pool contains a process for each defender state
    results = pool.starmap(individual_state, args_list)
    pool.close()
    pool.join()
    t1 = time.time()
    print ("******Total operation time*******: "+str(t1-t0))
    print("core number:"+str(mp.cpu_count()))
    return [gVKN_list, results]


a = ARVI(alpha, process_data())

states = a[1]
found_p = []
found_taus = []
for i in states:
    found_p.append(i[0])
    found_taus.append(i[1])

# output P to MSG_P.txt
for row in found_p:
    p_out.write(str(row)+'\n')

# output tau to MSG_tau.txt
tau_out.write(str(found_taus))

# output global variables to MSG.txt
g = a[0][0]
V = a[0][1]
K = a[0][2]
N = a[0][3]
msg_out.write("g:")
for i in g:
    msg_out.write(" " + str(i))
msg_out.write("\nV:")
for i in V:
    msg_out.write(" " + str(i))
msg_out.write("\nK:")
for i in K:
    msg_out.write(" " + str(i))
msg_out.write("\nN:")
for i in N:
    msg_out.write(" " + str(i))

msg_out.close()
tau_out.close()
p_out.close()