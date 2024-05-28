import numpy as np
import random

def infect_step(G,p1,individuals,N):
    '''The function serves as the infection model for each day.
    input params (consistent with the project description):

    
    G (ndarray N*N): the adjacency matrix.
    p1: the probability each individual infects neighbours.
    individuals = who's already infected
    N = # of people in 'individuals'
    '''

    ###################################################
    '''your code here'''
    individuals_updated = np.copy(individuals)
    for i in range(N):
        if individuals[i] == 1:     # this individual is infected
            ''' Need to find all of their neighbors and infect them w/
                probability p1 '''
            for neighbor_indx in range(N):
                if G[i][neighbor_indx] == 1:    # if i is neighbors w/ neighbor_indx

                    if individuals_updated[neighbor_indx] == 0: # if this person is NOT already infected
                        individuals_updated[neighbor_indx] = np.random.choice([0,1], p=[1-p1, p1])

                    # for debugging purposes:
                    #if individuals_updated[neighbor_indx] == 1:
                     #   print("\tInfecting ", neighbor_indx, ", who is a neighbor of ", i)
        
    ###################################################
    return individuals_updated



def infect(G,p0,p1,time_steps):
    '''The function serves as the infection model for each day.
    input params (consistent with the project description):
    G (ndarray N*N): the adjacency matrix.
    p0: the infection probability for initial status.
    p1: the probability each individual infects neighbours.
    time_steps: log N
    '''
    N = G.shape[0]
    individuals = np.zeros(N)
    ###################################################
    '''your code here'''
    for i in range(N):
        # infect everyone w/ initial probability p0
        individuals[i] = np.random.choice([0,1], p=[1-p0, p0])
    #print("Original infected individuals: ", individuals)
    
    for _ in range(time_steps):
        individuals = infect_step(G, p1, individuals, N)
        #print("Infected individuals after step ", _, " - ", individuals)
        
    ###################################################

    return individuals