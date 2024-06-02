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
    for i in range(len(s)):
        inf_people += s[i]
    return inf_people


def Q1_round(s, max_stages):
    inf_people = num_infected(s)
    n = round(len(s)/10)

    if(inf_people == 0 or len(s)<=1):    # Only one test + one stage b/c don't need to go any further
        return 1,1
    elif(n <= 1 or (inf_people <= n and inf_people >=1)):
        diag_tests, diag_stages = diag_splitting(s)
        return 1 + diag_tests, 1 + diag_stages
    else:   # run a recursive version of HGBSA
        num_per_group = round(len(s)/inf_people)
        
        # for each subgroup, call function again
        tests = 1 # = this testing group
        for i in range(int(inf_people)):
            stages = 1
            if(i == inf_people-1):
                subGroup = s[i*num_per_group:]
            else:
                subGroup = s[i*num_per_group:(i+1)*(num_per_group)]
            
            t, st = Q1_round(subGroup, max_stages)
            stages += st
            tests += t   # number of tests in subtree

            max_stages = max(max_stages, stages)
        return tests, max_stages

def Qtesting1(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    num_tests, stages = Q1_round(s, stages)

    ###################################################

    return num_tests, stages

def Qtesting1(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    num_tests, stages = Q1_round(s, stages)

    ###################################################

    return num_tests, stages

# ************************************ Qtesting2 ************************************

def Q2_round(s, max_stages):
    real_inf_people = num_infected(s)
    n = round(len(s)/10)
    inf_est = 0

    # Imitation of the range testing capabilities
    if (real_inf_people == 0):
        inf_est = 0
    elif(real_inf_people == 1):
        inf_est = 1
    elif(real_inf_people == 2 or real_inf_people == 3):
        inf_est = 2
    elif(real_inf_people < 8):
        inf_est = 4
    else:
        inf_est = max(8, round(len(s)/7))
    

    if (inf_est == 0 or len(s) <= 1): # If negative test or only one person in test
        return 1,1
    elif(n <= 1 or (inf_est <= n )): # if 10 or less people, or k is below threshold
        diag_tests, diag_stages = diag_splitting(s)
        return 1+diag_tests, 1+diag_stages
    else:   # run a recursive version of HGBSA
        num_per_group = round(len(s)/inf_est)
        
        # for each subgroup, call function again
        tests = 1 # = this testing group
        for i in range((inf_est)):
            stages = 1
            if(i == inf_est-1):
                subGroup = s[i*num_per_group:]
            else:
                subGroup = s[i*num_per_group:(i+1)*(num_per_group)]
            
            t, st = Q2_round(subGroup, max_stages)
            stages += st
            tests += t   # number of tests in subtree

            max_stages = max(max_stages, stages)
        print("TOTAL TESTS: ", tests, "\n")
        return tests, max_stages
  
def Qtesting2(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    num_tests, stages = Q2_round(s, stages)

    ###################################################
    return num_tests, stages

# ************************************ Community Aware ************************************

def Q1_commaware(communities):
    tests = 0
    max_stages = 0
    for family in communities:
        t, st = Qtesting1(family)
        tests += t
        max_stages = max(st, max_stages)
    return tests, max_stages+1

def Q2_commaware(communities):
    tests = 0
    max_stages = 0
    for family in communities:
        t, st = Qtesting2(family)
        tests += t
        max_stages = max(st, max_stages)
    return tests, max_stages+1

