import copy
import random
import math
import time

def tabu(file_path,veh,C):
    global coordinate
    global inf
    global tabu
    global depots
    global current_solution
    global current_solution_cost
    global best_solution
    global best_solution_cost
    global attribute

    global penalty # it's a dict, like penalty = {(1,0):1,(1,2):1,...,(10,2):3}. Record the number of times attribute ði; kÞ has been added to the solution during the search.


    coordinate = []
    load = []
    et = []
    lt = []
    st = []
    inf = []

    tabu = []

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

    inf = generate_inf(et,lt,load,st,coordinate,inf)



    current_solution = get_initial_solution(depots, veh)
    best_solution = copy.deepcopy(current_solution)
    best_solution_cost = cost(best_solution,inf,C)
    print(current_solution)
    # atwl = sum([lt[i] - et[i] for i in range(1, depots + 1)]) / depots
    iteration = 0
    while(iteration < 1):
        # attribute = attribute(best_solution)
        for index_routes in range(len(best_solution)):
            for req in best_solution[index_routes]:
                if req != 0 and req != depots and (req, index_routes) not in tabu and req <= (depots-2)/2:
                    tabu.append((req, index_routes))
                    # 还没有设置tabu的size
                    current_solution = spi(best_solution, index_routes, req, depots,inf,C)
                    # if atwl > 0.25:
                    #     current_solution = wri()
                    # else:
                    #     if True:
                    #         current_solution = wri()
                    #     else:
                    #         wri()
                    #         spi()
                    #         sbr()
                    current_solution_cost = cost(current_solution,inf,C)
                    if current_solution_cost < best_solution_cost:
                        best_solution = copy.deepcopy(current_solution)
                        best_solution_cost = current_solution_cost
        # print(best_solution)
        # if iteration/10 == 0:
        #     # intra-route
        #     best_solution = wri(best_solution)
        iteration += 1
    return best_solution


def generate_inf(et,lt,load,st,coordinate,inf):
    inf.append(et)
    inf.append(lt)
    inf.append(load)
    inf.append(st)
    inf.append(coordinate)
    return inf

def get_initial_solution(depots, veh):
    solution = [[],[],[]]
    list = []
    route = []
    for i in range(1,int((depots-2)/2)+1):
        route = int(random.randint(0,veh-1))
        solution[route].append(i)
        solution[route].append(int(i+(depots-2)/2))
        list.append(i)
    for i in range(3):
        solution[i].insert(0,0)
        solution[i].append(depots-1)
    return solution


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

def cost(solution, inf, C):
    adwl = get_ADWL(solution, inf)
    A = adwl[0]
    load = adwl[1]
    s_tw = 0
    s_ld = 0
    depots = 0
    for i in range(len(solution)):
        depots += len(solution[i])

    depots = depots - 2 * (len(solution)-1)
    depots = int(depots)

    for i in range(1, depots-1):
        t = A[i] - inf[1][i]
        s_tw = s_tw + max(0, t)
        l = load[i] - C
        s_ld = s_ld + max(0, l)

    # cost of the arc should be added
    dis = inf[4]
    distance = 0
    for s in solution:
        for i in range(len(s)-1):
            length = math.sqrt((dis[s[i]][0] - dis[s[i+1]][0]) ** 2 + (dis[s[i]][1] - dis[s[i+1]][1]) ** 2)
            distance += length

    Z = 1*s_tw + 1*s_ld + distance
    return Z

def attribute(solution):
    return attribute

def spi(solution, index_routes, req, depots,inf,C):

    c_solution = copy.deepcopy(solution)
    c_cost = cost(c_solution,inf,C)
    b_solution = copy.deepcopy(solution)
    b_cost = c_cost

    solution[index_routes].remove(req)
    solution[index_routes].remove(int(req+(depots-2)/2))
    init_solution = copy.deepcopy(solution)
    for i in range(len(solution)):
        if i != index_routes:
            # insert req to solution[i] and get cost
            # compare the cost to best_cost
            for pre_pos in range(1, len(solution[i])):
                solution[i].insert(pre_pos, req)
                flag = feasiable(solution[i],pre_pos,inf, depots,C)
                if flag:
                    for suc_pos in range(pre_pos+1,len(solution[i])):
                        solution[i].insert(suc_pos, int((depots-2)/2+req))
                        c_solution = copy.deepcopy(solution)
                        c_cost = cost(c_solution, inf, C)
                        if c_cost < b_cost:
                            b_solution = copy.deepcopy(c_solution)
                            b_cost = c_cost
                        solution[i].remove(int((depots-2)/2+req))
                solution[i].remove(req)
        solution = copy.deepcopy(init_solution)
    #get the best solution
    return b_solution

def feasiable(route,pre_pos,inf, depots,C):
    flag = True
    req = int((depots-2)/2)
    L = [0 for _ in range(depots)]
    A = [0 for _ in range(depots)]
    D = [0 for _ in range(depots)]
    site = 0
    for i in route:
        if site != 0 and site != len(route):
            A[site] = D[site-1] + inf[3][i]
            D[site] = max(A[site], inf[0][i])
            L[site] = L[site-1] + inf[2][i]

            if D[site] > inf[1][i] or L[site] > C:
                flag = False
                break
        if site == pre_pos:
            break
        site += 1
    return flag

def wri():
    return 0

if __name__ == "__main__":
    start = time.time()
    inf_path = '/home/yin/Desktop/pdp_test.txt'
    print(tabu(inf_path,3,10))
    stop = time.time()
    print(stop-start)



    # print(get_ADWL([[0,1,2,3,11,12,13,21]],[[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]))

    # print(get_initial_solution(22, 3))

    # depots = 22
    # C = 20
    # solution = [[0, 4, 14, 21], [0, 1, 11, 3, 13, 5, 15, 6, 16, 7, 17, 8, 18, 10, 20, 21], [0, 2, 12, 9, 19, 21]]
    # print(solution)
    # req = 4
    #
    # index_routes = 0
    #
    #
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0],
    #        [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144,
    #         1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0],
    #        [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0], [(40, 50), (35, 69), (40, 69), (38, 70), (42, 65), (38, 68), (15, 75), (20, 85), (15, 80), (22, 75), (30, 50), (45, 68), (45, 70), (42, 68), (40, 66), (35, 66), (25, 85), (22, 85), (20, 80), (18, 75), (25, 50), (40, 50)]]
    # print(cost(solution,inf,C))
    # cost(solution, inf, C)
    # solution = spi(solution, index_routes, req, depots,inf, 10)
    # print(solution)

    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]
    # print(cost(solution,inf,10))

    # print(feasiable([0, 1, 11, 3, 13, 5, 15, 6, 16, 7, 17, 8, 18, 10, 20, 21],2, inf, depots, C))