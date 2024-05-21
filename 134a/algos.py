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


def SG(s):
    inf_people = num_infected(s)
    print("\nTESTING group: ", s)

    if (inf_people  == 1):
        binary_tests, binary_stages, _ = binary_splitting(s)
        print("--Num binary tests: ", binary_tests)
        print("--Num binary stages: ", binary_stages)
        return 1 + binary_tests
    elif(inf_people < 1):
        print("0 infected --> ran only 1 test")
        return 1
    else:
        num_per_group = round(len(s)/inf_people)
        
        # for each subgroup, call function again
        tests = 1 # = this testing rou
        for i in range(inf_people):
            if(i == inf_people-1):
                subGroup = s[i*num_per_group:]
            else:
                subGroup = s[i*num_per_group:(i+1)*(num_per_group)]
            
            t = SG(subGroup)
            tests += t   # number of tests in subtree
        return tests
    

def Qtesting1(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    print("RUNNING TEST ON original: ", s, "\n")
    num_tests += SG(s)

    ###################################################

    return num_tests, stages


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

def mona(s, max_stages):
    inf_people = num_infected(s)
    print("\nTESTING group: ", s)
  

    if (inf_people  == 1):
        binary_tests, binary_stages, _ = binary_splitting(s)
        print("--Num binary tests: ", binary_tests)
        print("--Num binary stages: ", binary_stages)
        return 1 + binary_tests, 1 + binary_stages
    elif(inf_people < 1):
        print("0 infected --> ran only 1 test")
        return 1, 1
    else:
        num_per_group = round(len(s)/inf_people)
        
        # for each subgroup, call function again
        tests = 1 # = this testing group
        for i in range(inf_people):
            stages = 1
            if(i == inf_people-1):
                subGroup = s[i*num_per_group:]
            else:
                subGroup = s[i*num_per_group:(i+1)*(num_per_group)]
            
            t, st = mona(subGroup, max_stages)
            stages += st
            tests += t   # number of tests in subtree

            print("Setting stages to ", max(max_stages, stages))
            max_stages = max(max_stages, stages)
        return tests, max_stages
 
def lisa(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    print("RUNNING TEST ON original: ", s, "\n")
    num_tests, stages = mona(s, stages)

    ###################################################

    return num_tests, stages

#Returns a quantized number depending on infections
#0 
#1 (1<= I < 2)
#2 (2 <= I < 4)
#3 (4 <= I < 8)
#4 (>= 8)
def num_infected2(s):
    inf_people = 0
    for i in range(len(s)):
        inf_people += s[i]
    
    if(inf_people == 0):
        return 0
    elif(inf_people == 1):
        return 1
    elif(inf_people == 2 or inf_people == 3):
        return 2
    elif (inf_people < 8):
        return 3
    else:
        return 4
    
    
def pablo(s, max_stages):
    inf_range = num_infected2(s)
    print("\nTESTING group: ", s)
  
    if (inf_range == 0):
        print("0 infected --> ran only 1 test")
        return 1, 1
    elif (inf_range  == 1):
        # Only 1 infected person
        if len(s) == 1:
            return 1,1
        else:
            binary_tests, binary_stages, _ = binary_splitting(s)
            print("--Num binary tests: ", binary_tests)
            print("--Num binary stages: ", binary_stages)
            return 1 + binary_tests, 1 + binary_stages
   
    inf_people = 0
    if (inf_range == 2):
        inf_people = 3
    elif (inf_range == 3):
        inf_people = 7
    else:
        inf_people = 8

    num_per_group = round(len(s)/inf_people)
        
        # for each subgroup, call function again
    tests = 1 # = this testing group
    for i in range(inf_people):
        stages = 1
        if(i == inf_people-1):
            subGroup = s[i*num_per_group:]
        else:
            subGroup = s[i*num_per_group:(i+1)*(num_per_group)]
            
        t, st = pablo(subGroup, max_stages)
        stages += st
        tests += t   # number of tests in subtree

        # delete:
        m = max(max_stages, stages)
        if (m == stages and m != max_stages):
            print("Updating max stages from ", max_stages, " to ", stages)

        max_stages = max(max_stages, stages)
    return tests, max_stages
    

def picasso(s):
    '''
    s(np.array): binary string of infection status
    '''
    num_tests = 0
    stages = 0
    ###################################################
    '''your code here'''
    print("RUNNING TEST ON original: ", s, "\n")
    num_tests, stages = pablo(s, stages)
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