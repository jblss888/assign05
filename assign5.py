"""
Juliet Smith
For this assignment there is no automated testing. You will instead submit
your *.py file in Canvas. I will download and test your program from Canvas.
"""
import copy
import time
import sys
import random
INF = sys.maxsize


def adjMatFromFile(filename):
    """ Create an adj/weight matrix from a file with verts, neighbors, and weights. """
    f = open(filename, "r")
    n_verts = int(f.readline())
    print(f" n_verts = {n_verts}")
    adjmat = [[None] * n_verts for i in range(n_verts)]
    for i in range(n_verts):
        adjmat[i][i] = 0
    for line in f:
        int_list = [int(i) for i in line.split()]
        vert = int_list.pop(0)
        assert len(int_list) % 2 == 0
        n_neighbors = len(int_list) // 2
        neighbors = [int_list[n] for n in range(0, len(int_list), 2)]
        distances = [int_list[d] for d in range(1, len(int_list), 2)]
        for i in range(n_neighbors):
            adjmat[vert][neighbors[i]] = distances[i]
    f.close()
    return adjmat


def TSPwGenAlgo(
        g,
        max_num_generations=5,
        population_size=10,
        mutation_rate=0.01,
        explore_rate=0.5
    ):
    """ A genetic algorithm to attempt to find an optimal solution to TSP  """

    # NOTE: YOU SHOULD CHANGE THE DEFAULT PARAMETER VALUES ABOVE TO VALUES YOU
    # THINK WILL YIELD THE BEST SOLUTION FOR A GRAPH OF ~100 VERTS AND THAT CAN
    # RUN IN 5 MINUTES OR LESS (ON AN AVERAGE LAPTOP COMPUTER)

    solution_path = [] # list of n+1 verts representing sequence of vertices with lowest total distance found
    solution_distance = INF # distance of final solution path, note this should include edge back to starting vert
    avg_path_each_generation = [INF] * max_num_generations # store average path length path across individuals in each generation
    """This is where the individuals are initualized"""
    # create individual members of the population
    verts = list(range(len(g)))  # this is list of vectors in g
    population = [0] * population_size # this will hold lists of randomized vectors
    # initialize individuals to an initial 'solution'
    # This will initialize the population based on the vector list.
    # 0 and last spot should be the same vector
    for i in range(population_size):
        population[i] = (random.sample(verts[1:], len(verts) - 1))
    # loop for x number of generations (can also choose to add other early-stopping criteria)
    min_dist = INF
    for i in range(max_num_generations):
        # calculate fitness of each individual in the population
        fitness = [INF]*population_size  # this stores the distane for each individuale in tuples (distance, index in p)
        for j in range(population_size):
            # my assumption is that the start and finish is always the first vertex
            # this grabs the distances from the first to secound and last to first
            distance = g[0][population[j][0]] + g[0][population[j][-1]]
            for k in range(len(g)-1):
                distance += g[0][population[j][k]]
            if(distance < min_dist):
                # this isnures that the best solution though all generations is kept
                min_dist = distance
                solution_path = copy.deepcopy(population[j])
            fitness[j] = (distance, j)
        solution_distance = min_dist
        # calculate average path length across individuals in this generation
        avg_path_length = 0
        for h in range(population_size):
            dist = fitness[h]
            avg_path_length += dist[0]
        avg_path_length = avg_path_length/population_size
        # and store in avg_path_each_generation
        avg_path_each_generation[i] = avg_path_length
        # select the individuals to be used to spawn the generation, then create
        fitness.sort()  # this sort the population bast of their distances
        breaders = []
        if(i < max_num_generations // 2):
            rando = random.randint(len(breaders), len(fitness) - 1)
            rando = fitness[rando]
            rando = population[rando[1]]
            breaders = fitness[0:(population_size // 2) - 1]
            for j in range(len(breaders)):
                temp = breaders[j]
                breaders[j] = population[temp[1]]
            breaders.append(rando)
        else:
            breaders = fitness[0:population_size // 2]
            for j in range(len(breaders)):
                temp = breaders[j]
                breaders[j] = population[temp[1]]
        # individuals of the new generation (using some form of crossover)
        for p in range(population_size // 2):
            index = p * 2
            mom = breaders[p]
            dad = random.randint(0, len(breaders) - 1)
            while(dad == p):
                dad = random.randint(0, len(breaders) - 1)
            dad = breaders[dad]
            mom = population
        # allow for mutations (shuold be based on mutation_rate, should not happen too often)

        # ...
    # calculate and *verify* final solution
    solution_path.insert(0,0)
    solution_path.append(0)

    # update solution_path and solution_distance

    # ...

    return {
            'solution_path': solution_path,
            'solution_distance': solution_distance,
            'evolution': avg_path_each_generation
           }
def crossOver(mom, dad):
    pass


def TSPwDynProg(g):
    """ (10pts extra credit) A dynamic programming approach to solve TSP """
    solution_path = [] # list of n+1 verts representing sequence of vertices with lowest total distance found
    solution_distance = INF # distance of solution path, note this should include edge back to starting vert

    #...

    return {
            'solution_path': solution_path,
            'solution_distance': solution_distance,
           }


def TSPwBandB(g):
    """ (10pts extra credit) A branch and bound approach to solve TSP """
    solution_path = [] # list of n+1 verts representing sequence of vertices with lowest total distance found
    solution_distance = INF # distance of solution path, note this should include edge back to starting vert

    #...

    return {
            'solution_path': solution_path,
            'solution_distance': solution_distance,
           }


def assign05_main():
    """ Load the graph (change the filename when you're ready to test larger ones) """
    g = adjMatFromFile("complete_graph_n08.txt")

    # Run genetic algorithm to find best solution possible
    start_time = time.time()
    res_ga = TSPwGenAlgo(g)
    elapsed_time_ga = time.time() - start_time
    print(f"GenAlgo runtime: {elapsed_time_ga:.2f}")
    print(f"  sol dist: {res_ga['solution_distance']}")
    print(f"  sol path: {res_ga['solution_path']}")

    # (Try to) run Dynamic Programming algorithm only when n_verts <= 10
    if len(g) <= 10:
        start_time = time.time()
        res_dyn_prog = TSPwDynProg(g)
        elapsed_time = time.time() - start_time
        if len(res_dyn_prog['solution_path']) == len(g) + 1:
            print(f"Dyn Prog runtime: {elapsed_time:.2f}")
            print(f"  sol dist: {res_dyn_prog['solution_distance']}")
            print(f"  sol path: {res_dyn_prog['solution_path']}")

    # (Try to) run Branch and Bound only when n_verts <= 10
    if len(g) <= 10:
        start_time = time.time()
        res_bnb = TSPwBandB(g)
        elapsed_time = time.time() - start_time
        if len(res_bnb['solution_path']) == len(g) + 1:
            print(f"Branch & Bound runtime: {elapsed_time:.2f}")
            print(f"  sol dist: {res_bnb['solution_distance']}")
            print(f"  sol path: {res_bnb['solution_path']}")


# Check if the program is being run directly (i.e. not being imported)
if __name__ == '__main__':
    assign05_main()
