def plot_infect(N, M, q0, q1, p0, time_steps, num_sims, method, values):

    #plot_infect(N, M, q0, q1, p0, time_steps, num_sims, method, p1_values)
    #def iter(N,M,q0,q1,p0,p1,time_steps,num_sims,method,dataset='sbm'):
    frac_infected_list = []
    frac_infected_communities = []
    frac_infected_inCommunity = []
    print(p0)
    for p1 in values:
        frac_infected, frac_communities, frac_inCommunity, _, _ = iter(N, M, q0, q1, p0, p1, time_steps, num_sims, method, dataset='sbm')
        frac_infected_list.append(frac_infected)
        frac_infected_communities.append(frac_communities)
        frac_infected_inCommunity.append(frac_inCommunity)

    plt.figure(figsize=(10, 8))

    plt.plot(values, frac_infected_list, marker='o', linestyle='-', color='b', label='Fraction of Infected Individuals')
    plt.plot(values, frac_infected_communities, marker='o', linestyle='-', color='g', label='Fraction of Infected Communities')
    plt.plot(values, frac_infected_inCommunity, marker='o', linestyle='-', color='r', label='Fraction of Infected Individuals within Communities')

    plt.title('Fraction of Infected Metrics vs p1')
    plt.xlabel('p1')
    plt.ylabel('Fraction')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
