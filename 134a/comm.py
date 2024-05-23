import os
import pickle
import numpy as np

from algos import *
from infect import infect
from sbm import SBM

R = 2

''' 
Idea:
- select R representatives per family
- test that group of representatives
- if POS:
    individually test

    ASK - do we want to individually, test? what if R = 100 and the test outputs 1 infected person - should we run our algo on this also

if NEG:
    group test whole family
    if NEG --> done
    if POS --> run our original Qtesting1 and Qtesting 2
        TODO: create community sub arrays to pass into these functions
        + remember that when you pass this community into Qtesting1 + 2, it'll count the test of that community for you
            so will probably need to decrement a test by 1

How to reorganize 'leaves'

communities[i] = index of community that person i is in
'''

def create_communities(N, M):
    size = round(N/M)
    communities = np.zeros(N)
    
    for i in range(N):
        i_subgroup = np.floor((i)/size)       # which subgroup this index is in
        communities[i] = i_subgroup
    return communities


def test_communities(s, communities):
    tests = 1

    com_results = []
        # For community i, com_results[i][0] = how many of the R representatives were infected
        #                  com_results[i][1] = total # infected in community i


    com_group = 0
    inf_people = 0
    representative_count = 0
    person = 0
    temp = [0,0]
    while person < len(communities):
        curr_com = communities[person]

        # If this person is in a new community
        if (curr_com != com_group):
            if (representative_count != 0):
                print("resetting REP count")
                temp[0] = inf_people
                temp[1] = inf_people

                
            #print("----------Total infected in ", com_group, ": ", inf_people)
            com_results.append(temp)
            #print("Adding ", temp, " to COM_RESULTS ", com_group)
            temp = [0,0]
            com_group = curr_com
            tests += 1

            #print("\nReached community ", com_group, " at index ", person)
            inf_people = 0
            representative_count = 0
        
        # Once you've tested R representatives in this family
        if (representative_count == R):
            representative_count = 0
            temp[0] = inf_people

            # Skip all the rest of the people in this community
            while (person < len(communities) and communities[person] == com_group):
                inf_people += s[person]
                person += 1
            temp[1] = inf_people

        # Otherwise, count # of infected people w/in R representatives of this community
        else:
            inf_people += s[person]     
            representative_count += 1
            #print("Examining person ", person, " in comm ", com_group)
            person += 1


    #print("----Total infected in ", com_group, ": ", inf_people)
    com_results.append(temp)
    #print("Adding ", temp, " to COM_RESULTS ", com_group)

    return tests, com_results


def comm(s, communities):
    tests, results = test_communities(s, communities)
    print("\n*******************************\nInitial round of testing used ", tests, " tests")

    print(results)

    for c in range(len(results)):
        num_reps = results[c][0]
        num_total = results[c][1]
        print("\nCOMM ", c, " -- Found ", num_reps, " infected representatives and ", num_total, " infected in total")
        if (num_reps == 0):
            print("COM ", c, " is likely NOT infected")