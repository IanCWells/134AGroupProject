import os
import pickle
import numpy as np

from algos import *
from infect import infect
from sbm import SBM

import matplotlib.pyplot as plt


def create_communities(s, N, M):
    size = round(N/M)
    communities = []

    for i in range(M):
        if(i == M-1):
            comm = s[i*size:]
        else:
            comm = s[i*size:(i+1)*(size)]
        communities.append(comm)

    return communities


def iter(N,M,q0,q1,p0,p1,time_steps,num_sims,method,dataset='sbm'):

    name = dataset+'N'+str(N)+'_M'+str(M)+'_SIM'+str(num_sims)+'_step'+str(time_steps)+'_q0'+str(q0)+'_q1'+str(q1)+'_p0'+str(p0)+'_p1'+str(p1)+method+'graphs.pkl'
    if not os.path.isfile(name):
        print('Generating synthetic dataset!')
        Gs = np.zeros((num_sims,N,N))
        Communities = dict()
        data = dict()
        Individuals = dict()
        if dataset=='sbm':
            for i in range(num_sims):
                Gs[i] = SBM(N,M,q0,q1)
                Individuals[i] = infect(Gs[i],p0,p1,time_steps)
                s = Individuals[i]
                Communities[i] = create_communities(s, N,M)
        elif dataset=='iid':
            for i in range(num_sims):
                individuals = np.random.choice([0, 1], size=N, p=[1 - p0, p0])
                Individuals[i] = individuals
                s = Individuals[i]
                Communities[i] = create_communities(s, N,M)
        data['graph'] = Gs
        data['communities'] = Communities
        data['individuals'] = Individuals
        with open(name, 'wb') as infile:
            pickle.dump(data,infile) 


    ###################################################
    '''your code for initialization parameters if needed''' 
    fraction_ppl = 0
    fraction_family = 0
    fraction_ppl_in_family = 0
    num_tests = 0
    num_stages = 0
    ###################################################
        
    if os.path.isfile(name):
        with open(name, 'rb') as infile:
            data = pickle.load(infile) 
        print('Data loaded!')
    for i in range(num_sims): 
        '''
        if dataset=='synthetic':
            G = data['graph'][i]
            communities = data['communities'][i]
            individuals = data['individuals'][i]
        '''
        ###################################################
        '''your code to calculate the statistics here''' 
        if(method == "binary"):
            '''
            If dataset = iid
                Then the 'individuals' will be laid out in a randomized way
            If the dataset = sbm
                The 'individuals' are organized such that they are next to members of their community
                B/c within 'infect', the rows of G are organized in such a fashion
            '''
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_bs, num_stages_bs, _ = binary_splitting(individuals)
            num_tests += numtests_bs
            num_stages += num_stages_bs
        elif(method == "Q1"):   # iid
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_q1, num_stages_q1 = Qtesting1(individuals)
            num_tests += numtests_q1
            num_stages += num_stages_q1
        elif(method == "Q2"):   # iid
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_q2, num_stages_q2 = Qtesting2(individuals)
            num_tests += numtests_q2
            num_stages += num_stages_q2
        elif(method == "diag"):
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_diag, num_stages_diag = diag_splitting(individuals)
            num_tests += numtests_diag
            num_stages += num_stages_diag
        elif(method == "comm1"):    # sbm
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_comm1, num_stages_comm1 = Q1_commaware(communities)
            num_tests += numtests_comm1
            num_stages += num_stages_comm1
        elif(method == "comm2"):    # sbm
            G = data['graph']
            communities = data['communities'][i]
            individuals = data['individuals'][i]
            numtests_comm2, num_stages_comm2 = Q2_commaware(communities)
            num_tests += numtests_comm2
            num_stages += num_stages_comm2

        ###################################################

        # interleave the individuals
        #s = Individuals.copy()
        #np.random.shuffle(s)
        # binary
       # numtests_bs, num_stages_bs, _ = binary_splitting(s)
        '''
        # algorithm 1
        numtests_q1, num_stages_q1 = Qtesting1(s)
        # algorithm 2
        numtests_q2, num_stages_q2 = Qtesting2(s)
        # community-aware
        numtests_q1_c, num_stages_q1_c = Qtesting1_comm_aware(Individuals.copy(),communities)
        # community-aware
        numtests_q2_c, num_stages_q2_c = Qtesting2_comm_aware(Individuals.copy(),communities)
        '''

    ###################################################
    '''your code to calculate the statistics here''' 
    '''Do not forget to take the average'''
    num_tests /= num_sims
    num_stages /= num_sims

    ###################################################
            

    return fraction_ppl, fraction_family, fraction_ppl_in_family, num_tests, num_stages
        

def plot_results(N, M, q0, q1, p1, time_steps, num_sims, method, method2, method3, method4,method5, method6, p_values):
    num_tests_list = []
    num_stages_list = []

    num_tests_list2 = []
    num_stages_list2 = []

    num_tests_list3 = []
    num_stages_list3 = []  

    num_tests_list4 = []
    num_stages_list4 = []

    num_tests_comm1 = []
    num_stages_comm1 = []

    num_tests_comm2 = []
    num_stages_comm2 = []  
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method, dataset='sbm')
        num_tests_list.append(num_tests)
        num_stages_list.append(num_stages)

    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method2, dataset='sbm')
        num_tests_list2.append(num_tests)
        num_stages_list2.append(num_stages)

    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method3, dataset='sbm')
        num_tests_list3.append(num_tests)
        num_stages_list3.append(num_stages)     

    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method4, dataset='sbm')
        num_tests_list4.append(num_tests)
        num_stages_list4.append(num_stages) 

    # Community testing 1
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method5, dataset='sbm')
        num_tests_comm1.append(num_tests)
        num_stages_comm1.append(num_stages)      
    plt.figure(figsize=(18, 8))
    
    # Plot for number of tests
    plt.subplot(1, 2, 1)
    plt.plot(p_values, num_tests_list, marker='o', label=method)
    plt.plot(p_values, num_tests_list2, marker='x', label=method2)
    plt.plot(p_values, num_tests_list3, marker='^', label=method3)
    plt.plot(p_values, num_tests_list4, marker='^', label=method4)
    plt.plot(p_values, num_tests_comm1, marker='p', label=method5)
    plt.title('Number of Tests vs p0')
    plt.xlabel('p0')
    plt.ylabel('Number of Tests')
    plt.legend()
    
    # Plot for number of stages
    plt.subplot(1, 2, 2)
    plt.plot(p_values, num_stages_list, marker='o', label=method)
    plt.plot(p_values, num_stages_list2, marker='x', label=method2)
    plt.plot(p_values, num_stages_list3, marker='^', label=method3)
    plt.plot(p_values, num_stages_list4, marker='^', label=method4)
    plt.plot(p_values, num_stages_comm1, marker='p', label=method5)
    plt.title('Number of Stages vs p0')
    plt.xlabel('p0')
    plt.ylabel('Number of Stages')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


def plot_infect(N, M, q0, q1, p1, time_steps, num_sims, method, values):
    frac_infected_list = []
    frac_infected_communities = []
    frac_infected_inCommunity = []

    for p0 in values:
        frac_infected, frac_communities, frac_inCommunity, _, _ = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method, dataset='iid')
        frac_infected_list.append(frac_infected)
        frac_infected_communities.append(frac_communities)
        frac_infected_inCommunity.append(frac_inCommunity)

    #fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    ''' 
    axs[0].plot(values, frac_infected_list, marker='o', linestyle='-', color='b')
    axs[0].set_title('Fraction of Infected Individuals vs p0')
    axs[0].set_xlabel('p0')
    axs[0].set_ylabel('Fraction of Infected Individuals')

    axs[1].plot(values, frac_infected_communities, marker='o', linestyle='-', color='g')
    axs[1].set_title('Fraction of Infected Communities vs p0')
    axs[1].set_xlabel('p0')
    axs[1].set_ylabel('Fraction of Infected Communities')

    axs[2].plot(values, frac_infected_inCommunity, marker='o', linestyle='-', color='r')
    axs[2].set_title('Fraction of Infected Individuals within Communities vs p0')
    axs[2].set_xlabel('p0')
    axs[2].set_ylabel('Fraction of Infected Individuals within Communities')

    plt.tight_layout()
    plt.show() 
    '''

def plot_iid(N, M, q0, q1, p1, time_steps, num_sims, binary, diag, testing1, testing2, p_values):
    num_tests_binary_iid = []
    num_stages_binary_iid = []

    num_tests_diag_iid = []
    num_stages_diag_iid = []

    num_tests_q1 = []
    num_stages_q1 = []  

    num_tests_q2 = []
    num_stages_q2 = []

    # Binary
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, binary, dataset='iid')
        num_tests_binary_iid.append(num_tests)
        num_stages_binary_iid.append(num_stages)

    # Diagonal
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, diag, dataset='iid')
        num_tests_diag_iid.append(num_tests)
        num_stages_diag_iid.append(num_stages)

    # Q1
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, testing1, dataset='iid')
        num_tests_q1.append(num_tests)
        num_stages_q1.append(num_stages)     

    # Q2
    for p0 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, testing2, dataset='iid')
        num_tests_q2.append(num_tests)
        num_stages_q2.append(num_stages) 


    plt.figure(figsize=(18, 8))
    
    # Plot for number of tests
    plt.subplot(1, 2, 1)
    #plt.plot(p_values, num_tests_binary_iid, marker='o', label=binary)
    plt.plot(p_values, num_tests_diag_iid, marker='x', label=diag)
    plt.plot(p_values, num_tests_q1, marker='^', label=testing1)
    plt.plot(p_values, num_tests_q2, marker='^', label=testing2)

    plt.title('Number of Tests vs p0')
    plt.xlabel('p0')
    plt.ylabel('Number of Tests')
    plt.legend()
    
    # Plot for number of stages
    plt.subplot(1, 2, 2)
    #plt.plot(p_values, num_stages_binary_iid, marker='o', label=binary)
    plt.plot(p_values, num_stages_diag_iid, marker='x', label=diag)
    plt.plot(p_values, num_stages_q1, marker='^', label=testing1)
    plt.plot(p_values, num_stages_q2, marker='^', label=testing2)

    plt.title('Number of Stages vs p0')
    plt.xlabel('p0')
    plt.ylabel('Number of Stages')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def plot_comms(N, M, q0, q1, p0, time_steps, num_sims, binary, diag, testingcomm1, testingcomm2, p_values):
    num_tests_binary = []
    num_stages_binary = []

    num_tests_diag = []
    num_stages_diag = []

    num_tests_comm1 = []
    num_stages_comm1 = []

    num_tests_comm2 = []
    num_stages_comm2 = []  
    for p1 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, binary, dataset='sbm')
        num_tests_binary.append(num_tests)
        num_stages_binary.append(num_stages)

    for p1 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, diag, dataset='sbm')
        num_tests_diag.append(num_tests)
        num_stages_diag.append(num_stages)

    # Community testing 1
    for p1 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, testingcomm1, dataset='sbm')
        num_tests_comm1.append(num_tests)
        num_stages_comm1.append(num_stages)     

    for p1 in p_values:
        _, _, _, num_tests, num_stages = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, testingcomm2, dataset='sbm')
        num_tests_comm2.append(num_tests)
        num_stages_comm2.append(num_stages) 
    plt.figure(figsize=(18, 8))
    
    # Plot for number of tests
    plt.subplot(1, 2, 1)
    #plt.plot(p_values, num_tests_binary, marker='o', label=binary)
    plt.plot(p_values, num_tests_diag, marker='x', label=diag)
    plt.plot(p_values, num_tests_comm1, marker='p', label=testingcomm1)
    plt.plot(p_values, num_tests_comm2, marker='o', label=testingcomm2)
    plt.title('Number of Tests vs p1')
    plt.xlabel('p1')
    plt.ylabel('Number of Tests')
    plt.legend()
    
    # Plot for number of stages
    plt.subplot(1, 2, 2)
   # plt.plot(p_values, num_stages_binary, marker='o', label=binary)
    plt.plot(p_values, num_stages_diag, marker='x', label=diag)
    plt.plot(p_values, num_stages_comm1, marker='p', label=testingcomm1)
    plt.plot(p_values, num_stages_comm2, marker='o', label=testingcomm2)
    plt.title('Number of Stages vs p1')
    plt.xlabel('p1')
    plt.ylabel('Number of Stages')
    plt.legend()
    
    plt.tight_layout()
    plt.show()