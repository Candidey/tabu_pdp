def tabu(file_path):
    global coordinate
    global inf
    global current_solution
    global current_solution_cost
    global best_solution
    global best_solution_cost
    global attribute

    coordinate = []
    load = []
    et = []
    lt = []
    st = []
    inf = []
    with open(file_path, 'r') as f:
        data = f.readlines()
        depots = len(data)  # number of depots
    for line in data:
        inf_line = line.split()
        inf_line = list(map(int, inf_line))

        coordinate.append((inf_line[1], inf_line[2]))
        load.append(inf_line[3])
        et.append(inf_line[4])
        lt.append(inf_line[5])
        st.append(inf_line[6])

    inf.append(et)
    inf.append(lt)
    inf.append(load)
    inf.append(st)

    current_solution = get_initial_solution()
    best_solution = current_solution
    iteration = 0
    while(iteration < 1000):
        for index_routes in range(len(current_solution)):

            for req in current_solution[index_routes]:

def get_initial_solution():
    pass

def get_ADWL(solution, inf):
    for _ in inf:
        pick_up = len(_)/2 - 1
        pick_up = int(pick_up)

    vehicles= len(solution)

    A = [0 for _ in range(pick_up*2 +2)]
    D = [0 for _ in range(pick_up*2 +2)]
    W = [0 for _ in range(pick_up*2 +2)]
    M = 10000
    # travle_time = []
    load = [0 for _ in range(pick_up*2 +2)]
    C = 20
    for route in solution:
        count_route = 1
        # count_routes = 0
        for i in route[1:len(route)-1:]:
            # if i > pick_up and route[count+1] > pick_up * 2:
            #     travle_time[i] = time_table[3][i]
            # elif route[count+1] <= pick_up and i > pick_up * 2:
            #     travle_time[i] = time_table[3][0]
            # elif i <= pick_up and route[count+1] > pick_up * 2:
            #     travle_time[i] = M
            # elif route[count+1] > pick_up and i > pick_up * 2:
            #     travle_time[i] = M
            # else:
            #     travle_time[i] = time_table[3][i]

            if count_route == 1:
                load[i] = inf[2][i]
                if i > pick_up:
                    A[i] = M
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
                else:
                    A[i] = 0
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
            elif count_route == len(route) - 2:
                load[i] = load[route[count_route-1]] + inf[2][i]
                if i <= pick_up:
                    A[i] = M
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
                else:
                    load[i] = load[route[count_route - 1]] + inf[2][i]
                    A[i] = inf[3][route[count_route - 1]] + D[route[count_route - 1]]
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
            else:
                load[i] = load[route[count_route-1]] + inf[2][i]
                A[i] = inf[3][route[count_route-1]] + D[route[count_route-1]]
                D[i] = max(A[route[count_route]], inf[0][i])
                W[i] = D[i] - A[i]

            # travle_time[count_routes] = sum
            count_route += 1
    ADWL = []
    ADWL.append(A)
    ADWL.append(D)
    ADWL.append(W)
    ADWL.append(load)
    return ADWL

def cost():
    pass




if __name__ == "__main__":
    # inf_path = '/home/yin/Desktop/pdp_test.txt'
    # tabu(inf_path)
    # print(get_ADWL([[0,1,2,3,11,12,13,21]],[[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]))
    pass