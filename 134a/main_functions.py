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
        #print('Data loaded!')
    for i in range(num_sims): 
        '''
        if dataset=='synthetic':
            G = data['graph'][i]
            communities = data['communities'][i]
            individuals = data['individuals'][i]
        '''
        ###################################################
        '''your code to calculate the statistics here'''
        communities = data['communities'][i]
        individuals = data['individuals'][i] 

        if(method == "binary"):
            '''
            If dataset = iid
                Then the 'individuals' will be laid out in a randomized way
            If the dataset = sbm
                The 'individuals' are organized such that they are next to members of their community
                B/c within 'infect', the rows of G are organized in such a fashion
            '''
            s = individuals.copy()
            if dataset == 'sbm':
                np.random.shuffle(s)

            numtests_bs, num_stages_bs, _ = binary_splitting(s)
            num_tests += numtests_bs
            num_stages += num_stages_bs
        elif(method == "Q1"):   # iid
            numtests_q1, num_stages_q1 = Qtesting1(individuals)
            num_tests += numtests_q1
            num_stages += num_stages_q1
        elif(method == "Q2"):   # iid
            numtests_q2, num_stages_q2 = Qtesting2(individuals)
            num_tests += numtests_q2
            num_stages += num_stages_q2
        elif(method == "diag"):
            s = individuals.copy()
            if dataset == 'sbm':
                np.random.shuffle(s)
            
            numtests_diag, num_stages_diag = diag_splitting(s)
            num_tests += numtests_diag
            num_stages += num_stages_diag
        elif(method == "comm1"):    # sbm
            numtests_comm1, num_stages_comm1 = Q1_commaware(communities)
            num_tests += numtests_comm1
            num_stages += num_stages_comm1
        elif(method == "comm2"):    # sbm
            numtests_comm2, num_stages_comm2 = Q2_commaware(communities)
            num_tests += numtests_comm2
            num_stages += num_stages_comm2


    ###################################################
    '''your code to calculate the statistics here''' 
    '''Do not forget to take the average'''
    num_tests /= num_sims
    num_stages /= num_sims
    ###################################################
            

    return fraction_ppl, fraction_family, fraction_ppl_in_family, num_tests, num_stages
        



def plot_infect(N, M, p0, time_steps, num_sims, method):
    # Define the different q0 and q1 pairs
    q_values = [
        (1, 0),
        (0.9, 0.1),
        (0.5, 0.3)
    ]

    # Define the p1 values to iterate over
    p1_values = np.linspace(0.05, 1, 9)

    # Initialize lists to hold the results for each q_value pair
    all_frac_infected = []
    all_frac_communities = []
    all_frac_inCommunity = []

    # Iterate over each q0, q1 pair and collect the data
    for (q0, q1) in q_values:
        frac_infected_list = []
        frac_infected_communities = []
        frac_infected_inCommunity = []

        for p1 in p1_values:
            frac_infected, frac_communities, frac_inCommunity, _, _ = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method, dataset='sbm')
            frac_infected_list.append(frac_infected)
            frac_infected_communities.append(frac_communities)
            frac_infected_inCommunity.append(frac_inCommunity)

        all_frac_infected.append(frac_infected_list)
        all_frac_communities.append(frac_infected_communities)
        all_frac_inCommunity.append(frac_infected_inCommunity)

    # Plotting frac_infected for each q0, q1 pair
    plt.figure(figsize=(8,6))
    for i, (q0, q1) in enumerate(q_values):
        plt.plot(p1_values, all_frac_infected[i], marker='o', linestyle='-', label=f'q0={q0}, q1={q1}')
    plt.title('Fraction of Infected Individuals vs p1')
    plt.xlabel('p1')
    plt.ylabel('Fraction of Infected Individuals')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plotting frac_communities for each q0, q1 pair
    plt.figure(figsize=(8,6))
    for i, (q0, q1) in enumerate(q_values):
        plt.plot(p1_values, all_frac_communities[i], marker='o', linestyle='-', label=f'q0={q0}, q1={q1}')
    plt.title('Fraction of Infected Communities vs p1')
    plt.xlabel('p1')
    plt.ylabel('Fraction of Infected Communities')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plotting frac_inCommunity for each q0, q1 pair
    plt.figure(figsize=(8,6))
    for i, (q0, q1) in enumerate(q_values):
        plt.plot(p1_values, all_frac_inCommunity[i], marker='o', linestyle='-', label=f'q0={q0}, q1={q1}')
    plt.title('Fraction of Infected Individuals within Communities vs p1')
    plt.xlabel('p1')
    plt.ylabel('Fraction of Infected Individuals within Communities')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



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
    plt.plot(p_values, num_tests_binary_iid, marker='o', label=binary)
    plt.plot(p_values, num_tests_diag_iid, marker='x', label=diag)
    plt.plot(p_values, num_tests_q1, marker='^', label=testing1)
    plt.plot(p_values, num_tests_q2, marker='^', label=testing2)

    plt.title('Number of Tests vs p0')
    plt.xlabel('p0')
    plt.ylabel('Number of Tests')
    plt.legend()
    
    # Plot for number of stages
    plt.subplot(1, 2, 2)
    plt.plot(p_values, num_stages_binary_iid, marker='o', label=binary)
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
    plt.plot(p_values, num_tests_binary, marker='o', label=binary)
    plt.plot(p_values, num_tests_diag, marker='x', label=diag)
    plt.plot(p_values, num_tests_comm1, marker='^', label=testingcomm1)
    plt.plot(p_values, num_tests_comm2, marker='o', label=testingcomm2)
    plt.title('Number of Tests vs p1')
    plt.xlabel('p1')
    plt.ylabel('Number of Tests')
    plt.legend()
    
    # Plot for number of stages
    plt.subplot(1, 2, 2)
    plt.plot(p_values, num_stages_binary, marker='o', label=binary)
    plt.plot(p_values, num_stages_diag, marker='x', label=diag)
    plt.plot(p_values, num_stages_comm1, marker='^', label=testingcomm1)
    plt.plot(p_values, num_stages_comm2, marker='o', label=testingcomm2)
    plt.title('Number of Stages vs p1')
    plt.xlabel('p1')
    plt.ylabel('Number of Stages')
    plt.legend()
    
    plt.tight_layout()
    plt.show()