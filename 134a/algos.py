import numpy as np
import random


# binary spliting
def binary_splitting_round(s):
    # s: np.array the infectious status & test status
    num = 0
    flag = sum(s[:,0])>0
    assert flag
    stages = 0
    if len(s[:,0])==1:
        s[0,1] = s[0,0]
        return num,s,stages
    
    B1, B2 = np.array_split(s.copy(), 2,axis=0)
    flag = sum(B1[:,0])>0
    num+=1
    stages += 1
    
    if flag:
        n,stmp,stage = binary_splitting_round(B1)
        s[:len(B1),1] = stmp[:,1]
    else:
        s[:len(B1),1] = 0
        n,stmp,stage = binary_splitting_round(B2)
        s[len(B1):,1] = stmp[:,1]
    num += n
    stages += stage
    return num,s,stages 

def binary_splitting(s):
    # modified bs
    # s: 1-d array the infectious status
    st = np.zeros((len(s),2))
    st[:,0] = s
    st[:,1] = np.nan
    nums = 0
    count = sum(np.isnan(st[:,1]))
    stages = 0
    # the undetermined people
    while count!=0:
        mask = np.isnan(st[:,1])
        flag = sum(st[mask,0]>0)>0
        nums += 1
        stages+=1
        if not flag:
            st[mask,1] = 0
        else:
            n,stmp,stage = binary_splitting_round(st[mask,:])
            st[mask,1] = stmp[:,1]
            nums += n
            stages += stage
        count = sum(np.isnan(st[:,1]))
        
    assert sum(st[:,0]!=st[:,1])==0
    return nums,stages, st[:,1]

# diag
def diagalg_iter(s):
    # s(np.array): binary string of infection status
    k = int(np.log2(len(s)))
    l = int(2**(k-1))
    lp = 0
    p = np.zeros(k+1)
    group = dict()
    num = np.ones(k+1,dtype=np.int32)
    for i in range(k):
        p[i] = sum(s[lp:lp+l])>0
        group[i] = s[lp:lp+l]
        num[i] = l
        lp+=l
        l = l//2

    p[-1] = s[-1]
    group[k] = np.array([s[-1]])
    # p(array): pattern
    # group(dict): indicate the group information
    # num(array): the group size
    return p.astype(np.int32), group,num


def diag_splitting(s):
    # s(np.array): binary string of infection status
    num_tests = 0
    stages = 0
    pattern, group, nums = diagalg_iter(s)
    stages +=1
    num_tests += len(pattern)
    indices = np.where(pattern == 1)[0]
    flag = 0
    for i in indices:
        if nums[i]>1:
            num_test,stage = diag_splitting(group[i])
            num_tests += num_test
            if not flag:
                stages+=stage
                flag = 1
    return num_tests,stages

def num_infected(s):
    inf_people = 0
    for i in s:
        inf_people += s[i]
    return inf_people


def SG(s, inf_people, num_tests, num_stages):
    print("\n\tTest no: ", num_tests)
    #s is the subgroup we are passing in
    print("s subgroup: ", s)
    num_people = len(s)
    if(inf_people <= 1):
        print("Reached base case")
        # run binary_splitting
        binary_splitting(s)
        return 1, 0
    
    '''
    Other case: when subgroups have relatively equal number of infected people left in them
        ie avg # of infected people in them
        case --> when inf_people = 
    
    '''

    num_in_group = num_people // inf_people
    print("Number in group: ", num_in_group)
    

    for i in range(inf_people):        
        subGroup = s[i*num_in_group:(i+1)*(num_in_group)]
        num_stages += 1
        if(i == inf_people-1):
            subGroup = s[i*num_in_group:]
        else:
            subGroup = s[i*num_in_group:(i+1)*(num_in_group)]
        
        #recursively calls each subgroup
        t, _ = SG(subGroup, num_infected(subGroup), num_tests, num_stages)
        num_tests += t
    
    return num_tests, num_stages
    

def Qtesting1(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    print("RUNNING TEST ON original: ", s, "\n")
    num_tests, stages = SG(s, num_infected(s), num_tests, stages)

    ###################################################

    return num_tests-1,stages-1     # TODO: not sure why it's -1


def Qtesting2(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''

    ###################################################



    return num_tests,stages



def Qtesting1_comm_aware(s,communities):
    '''
    s(np.array): binary string of infection status
    communities(list): the community information
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''

    ###################################################



    return num_tests,stages

def Qtesting2_comm_aware(s,communities):
    '''
    s(np.array): binary string of infection status
    communities(list): the community information
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''

    ###################################################



    return num_tests,stages