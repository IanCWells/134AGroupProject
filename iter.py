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
                ###################################################
                '''your code here'''
                ###################################################
                Individuals[i] = infect(Gs[i],p0,p1,time_steps)
                s = Individuals[i]
                Communities[i] = create_communities(s,N,M)
                print(Communities[i])
        elif dataset=='iid':
            for i in range(num_sims):
                ###################################################
                '''your code here'''
                individuals = np.random.choice([0, 1], size=N, p=[1 - p0, p0])
                Individuals[i] = individuals
                s = Individuals[i]
                print(s)
                Communities[i] = create_communities(s, N,M)
                print(Communities[i])
                ###################################################
        data['graph'] = Gs
        data['communities'] = Communities
        data['individuals'] = Individuals
        with open(name, 'wb') as infile:
            pickle.dump(data,infile) 
    #         print('Dataset done!')


    ###################################################
    '''your code for initialization parameters if needed''' 
    fraction_ppl = 0
    fraction_family = 0
    fraction_ppl_in_family = 0
    num_tests = 0
    num_stages = 0

    frac_total_infected = 0
    
    total_infected_communities = 0
    tot_avg = 0
    
    ###################################################
        
    if os.path.isfile(name):
        with open(name, 'rb') as infile:
            data = pickle.load(infile) 
       # print('Data loaded!')
    for i in range(num_sims): 
        avg1 = 0
        total_infected_communities_thiscycle = 0
        
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
        print(float(len(individuals)))


        
        frac_total_infected += float(float(num_infected(individuals))/float(len(individuals)))
    

        #Should be all infected communities in entire simulation
        for community in communities:
            if num_infected(community) > 0:
                total_infected_communities += 1
                total_infected_communities_thiscycle += 1


        for community in communities:
            # Yields a list of people in that particular community on this simulation
            family_infections = num_infected(community)
            if(family_infections > 0):
                avg1 += (family_infections / len(community))

        if(total_infected_communities_thiscycle > 0):
            avg1 = avg1 / total_infected_communities_thiscycle
            tot_avg += avg1


        if(method == "binary"):
            G = data['graph']
            
            numtests_bs, num_stages_bs, _ = binary_splitting(individuals)
            num_tests += numtests_bs
            num_stages += num_stages_bs
            

        elif(method == "Q1"):
            G = data['graph']
           
            numtests_q1, num_stages_q1 = Qtesting1(individuals)
            num_tests += numtests_q1
            num_stages += num_stages_q1
        elif(method == "Q2"):
            G = data['graph']
            
            numtests_q2, num_stages_q2 = Qtesting2(individuals)
            num_tests += numtests_q2
            num_stages += num_stages_q2
        elif(method == "diag"):
            G = data['graph']
            
            numtests_diag, num_stages_diag = diag_splitting(individuals)
            num_tests += numtests_diag
            num_stages += num_stages_diag

        #elif(method == "Q1_C"):
        #elif(method == "Q2_C"):
        
        ###################################################

        # interleave the individuals
        #s = Individuals.copy()
        #infectedNumber = num_infected(s)
        #print(infectedNumber)
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

    #s = Individuals.copy()
    #num_infected(s)
    #Should average all infected people over total number of people in all simulations 

    #Somehow it is only looping through a part of the population??
    #print(frac_total_infected)
    
    #Problem is not num_sims
    fraction_ppl = float(frac_total_infected) / float(num_sims)

    #Need to figure out how to establish communities properly
    #Fraction family: average infected communities / total communities as a percentage
    fraction_family = total_infected_communities / (M * num_sims)
    
    #fraction_ppl_in_family:  is the number of people infected in a family / total size of family (averaged)
    
    fraction_ppl_in_family = tot_avg / (num_sims)
            

    return fraction_ppl, fraction_family, fraction_ppl_in_family, num_tests, num_stages
        
