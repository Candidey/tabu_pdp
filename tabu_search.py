import get_initial_path
import get_time_table
import penalty
import sbr
import spi
import wri

def tabu_search(inf_path):
    """
    read file and get information
    """
    global current_solution
    global current_solution_cost
    global op_solution
    global op_solution_cost
    global coordinate
    global time_table
    global depots
    global L_status
    # we need a travel time

    coordinate = []
    time_table = []
    et = []
    lt = []
    load = []
    st = []



    with open(inf_path, 'r') as f:
        data = f.readlines()
        depots = len(data)  # number of depots
    for line in data:
        inf = line.split()
        inf = list(map(int, inf))

        coordinate.append((inf[1], inf[2]))
        load.append(inf[3])
        et.append(inf[4])
        lt.append(inf[5])
        st.append(inf[6])

    time_table.append(et)
    time_table.append(lt)
    time_table.append(load)
    time_table.append((st))


    """
    tabuSzie
    L_status : record and enforce the tabu status
    atwl : A hierarchical multi-neighborhood search strategy, based on average time window length (atwl)
    """

    tabu_length = max(30, depots / 2)
    nodes = [x+1 for x in range(depots)]
    pos_iter = [(0,0) for _ in range(depots)]
    L_status = dict(map(lambda x,y:[x,y],nodes,pos_iter))
    print(L_status)

    """
    A: arrive time, D + t
    D: depart time, max(A,e)
    W: wait time, max(0, e - A)
    load <= C C: capacity

    a penalty structure for time window and load violations associated with each solution:
        Stw and Sld
        Z

    we need a function to compute all kinds of time

    one solution maybe have several different routes
    """


    current_solution = get_initial_path()
    current_solution_cost = penalty()

    current_solution = spi(current_solution)
    current_solution_cost = penalty(current_solution)

    iteration = 0
    while(iteration < 1000):

        current_solution = spi()
        current_solution_cost = penalty()
        # compute the average time window length
        atwl = sum([lt[i] - et[i] for i in range(1, depots + 1)]) / depots
        # if atwl is greater than 25%, after performing an SPI move, the algorithm is directed to perform n/10 successive WRI moves. Else, perform n/25 successive WRI moves.
        if atwl >= 0.25:
            # after moves, get a new solution. and judge if it's better than current solution or not. and new the tabuList and the L_status
            pass
        else:
            pass

        # if 10 unique solutions are visited twice, perform SBR
        # if True:
        #     basin_interation = 0
        #     while(basin_interation < min(len(best_solution)),depots/10):
        #         current_solution = sbr()
        #         basin_interation += 1

        """
        we need function to adjust the size of tabu
        """


        # A hierarchical multi-neighborhood search strategy, based on average time window length (atwl)

        # Detecting and escaping from a chaotic attractor basin

    return 1


if __name__ == "__main__":
    inf_path = '/home/yin/Desktop/pdp_test.txt'
    tabu_search(inf_path)
        # print(inf)