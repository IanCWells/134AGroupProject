import numpy as np
#import networkx as nx

def SBM(N,M,q0,q1):
    '''This function is designed to generate the Stochastic Block Model.
    input params (consistent with the project description):
    N (int): the number of individuals
    M (int): the number of subgroups
    q0 (float): probability of inter-subgroup connection
    q1 (float): probability of intra-subgroup connection

    output:
    G (N*N): adjacency matrix of the generated graph
    '''
    #################################################
    ''' your code here'''
    G = np.zeros((N,N), dtype=int)

    '''
    i % size = index into subgroup
    '''

    size = round(N/M)
    
    #Testing
    #print("Group size: ", size)

   #  '''
    for i in range(N):
        i_subgroup = np.floor((i)/size)       # which subgroup this index is in
        for j in range(N):
            if i == j:
                continue
            
            j_subgroup = np.floor((j)/size)
            
            if (j_subgroup == i_subgroup):
                connected = np.random.choice([0,1], p=[1-q0, q0])   # for inter-group
            else:
                connected = np.random.choice([0,1], p=[1-q1, q1])   # for intra-group

            G[i][j] = connected
            G[j][i] = connected
    # '''
    #################################################

    return G