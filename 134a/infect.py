import numpy as np
import random

def infect_step(G,p1,individuals,N):
    '''The function serves as the infection model for each day.
    input params (consistent with the project description):
    G (ndarray N*N): the adjacency matrix.
    p1: the probability each individual infects neighbours.
    '''

    ###################################################
    '''your code here'''

                        
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

    ###################################################

    return individuals