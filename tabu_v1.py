import random
import math
import copy
import time
import operator

def generate_inf(et,lt,load,st,coordinate,inf):
    inf.append(et)
    inf.append(lt)
    inf.append(load)
    inf.append(st)
    inf.append(coordinate)
    return inf

def get_initial_solution(pkn, veh):
    solution = [[] for _ in range(veh)]
    list = []
    route = []
    for i in range(1, pkn + 1):
        route = int(random.randint(0, veh - 1))
        solution[route].append(i)
        solution[route].append(i+pkn)
        list.append(i)
    for i in range(3):
        solution[i].insert(0, 0)
        solution[i].append(pkn*2+1)
    return solution

def get_ADWL(solution, inf, pkn, C):
    A = [0 for _ in range(pkn*2+2)]
    D = [0 for _ in range(pkn*2+2)]
    W = [0 for _ in range(pkn*2+2)]
    M = 100000
    load = [0 for _ in range(pkn*2+2)]

    for route in solution:
        count_route = 1
        for i in route[1:len(route)-1]:
            if count_route == 1:
                load[i] = inf[2][i]
                if i > pkn:
                    A[i] = M
                    D[i] = max(A[route[count_route]],inf[0][i])
                    W[i] = D[i] - A[i]
                else:
                    A[i] = 0
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
            elif count_route == len(route) - 2:
                load[i] = load[route[count_route-1]] + inf[2][i]
                if i <= pkn:
                    A[i] = M
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
                else:
                    load[i] = load[route[count_route-1]] + inf[2][i]
                    A[i] = inf[3][route[count_route-1]] + D[route[count_route-1]]
                    D[i] = max(A[route[count_route-1]], inf[0][i])
                    W[i] = D[i] - A[i]
            else:
                load[i] = load[route[count_route - 1]] + inf[2][i]
                A[i] = inf[3][route[count_route - 1]] + D[route[count_route - 1]]
                D[i] = max(A[route[count_route - 1]], inf[0][i])
                W[i] = D[i] - A[i]

            count_route += 1

    AWDL = []
    AWDL.append(A)
    AWDL.append(D)
    AWDL.append(W)
    AWDL.append(load)

    return AWDL

def tw_ld_flag(adwl):
    tw_flag = True
    ld_flag = True

    for i in adwl[1]:
        if i < 0:
            tw_flag = False
    for i in adwl[3]:
        if i < 0:
            ld_flag = False

    return tw_flag, ld_flag

def cost(x, y, solution, inf, pkn, C):
    c_dist = 0
    c_ld = 0
    c_tw = 0


    adwl = get_ADWL(solution, inf, pkn, C)
    A = adwl[0]
    load = adwl[1]

    # violation of time window and load
    for i in range(1,pkn*2+1):
        t = A[i] - inf[1][i]
        c_tw = c_tw + max(0,t)
        l = load[i] - C
        c_ld = c_ld + max(0,l)

    # cost of arc
    coor = inf[4]
    for s in solution:
        for i in range(len(s)-1):
            c_dist += math.sqrt((coor[s[i]][0] - coor[s[i+1]][0]) ** 2 + (coor[s[i]][1] - coor[s[i+1]][1]) ** 2)

    cost = c_dist  + x*c_tw + y*c_ld

    return cost

def feasiable(route, pre_pos, inf, depots,C):
    flag = True

    L = [0 for _ in range(depots)]
    A = [0 for _ in range(depots)]
    D = [0 for _ in range(depots)]
    site = 0
    for i in route:
        if site != 0 and site != len(route):
            A[site] = D[site - 1] + inf[3][i]
            D[site] = max(A[site], inf[0][i])
            L[site] = L[site - 1] + inf[2][i]

            if D[site] > inf[1][i] or L[site] > C:
                flag = False
                break
        if site == pre_pos:
            break
        site += 1
    return flag

def spi(x, y, f_solution, index_routes, req, pkn, inf, C):
    solution = copy.deepcopy(f_solution)
    init_solution = copy.deepcopy(solution)
    c_solution = copy.deepcopy(solution)
    c_cost = cost(x, y, c_solution, inf, pkn, C)
    b_solution = copy.deepcopy(solution)
    b_cost = c_cost

    solution[index_routes].remove(req)
    solution[index_routes].remove(req+pkn)

    for i in range(len(solution)):
        if i != index_routes:
            for pre_pos in range(1, len(solution[i])):
                solution[i].insert(pre_pos, req)
                flag = feasiable(solution[i], pre_pos, inf, pkn*2 +2, C)
                if flag:
                    for suc_pos in range(pre_pos+1, len(solution[i])):
                        solution[i].insert(suc_pos, req+pkn)
                        c_solution = copy.deepcopy(solution)
                        c_cost = cost(x, y, c_solution, inf, pkn, C)

                        if c_cost < b_cost:
                            b_solution = copy.deepcopy(c_solution)
                            b_cost = c_cost
                        solution[i].remove(pkn+req)
                solution[i].remove(req)
        solution = copy.deepcopy(init_solution)

        return b_solution

def tabu(file_path, veh, C):
    global inf
    global  pkn
    global x
    global y
    global z
    global tabu
    x = 0.00001
    y = 0.00001
    z = 0.5

    et = []
    lt = []
    st = []
    load = []
    coordinate = []
    inf = []
    tabu = []

    with open(file_path, 'r') as f:
        data = f.readlines()
        depots = len(data)
        pkn = int((depots-2)/2)
    for line in data:
        inf_line = line.split()
        inf_line = list(map(int, inf_line))

        coordinate.append((inf_line[1],inf_line[2]))
        load.append(inf_line[3])
        et.append(inf_line[4])
        lt.append(inf_line[5])
        st.append(inf_line[6])

    inf = generate_inf(et,lt,load,st,coordinate,inf)

    initial_solution = get_initial_solution(pkn, veh)
    current_solution = copy.deepcopy(initial_solution)
    best_solution = copy.deepcopy(initial_solution)
    best_solution_cost = cost(x, y, best_solution, inf, pkn, C)

    print(initial_solution)

    iteration = 0
    while(iteration < 1):
        for index_routes in range(len(current_solution)):
            for req in initial_solution[index_routes]:
                if req != 0 and req != depots and (req, index_routes) not in tabu and req <= pkn:
                    if len(tabu) > 5:
                        del tabu[0]
                    instant_s = spi(x, y, current_solution, index_routes, req, pkn, inf, C)
                    if not operator.eq(instant_s,current_solution):
                        tabu.append((req, index_routes))
                        current_solution = copy.deepcopy(instant_s)
                        current_solution_cost = cost(x, y, current_solution, inf, pkn, C)
                        # print('current solution', current_solution)
                        # print('curretn cost', current_solution_cost)
                        adwl = get_ADWL(current_solution, inf, pkn, C)
                        tw_flag, ld_flag = tw_ld_flag(adwl)
                        if tw_flag:
                            x = x / (1+z)
                        else:
                            x = x * (1+z)
                        if ld_flag:
                            y = y / (1+z)
                        else:
                            y = y * (1+z)
                        if current_solution_cost < best_solution_cost:
                            best_solution = copy.deepcopy(current_solution)
                            best_solution_cost = current_solution_cost

        print('best solution', best_solution)
        print('cost', best_solution_cost)
        initial_solution = copy.deepcopy(best_solution)
        current_solution = copy.deepcopy(best_solution)
        iteration += 1
        print(tw_ld_flag(get_ADWL(best_solution,inf,pkn,C)))
    return best_solution



if __name__ == "__main__":
    start = time.time()
    inf_path = '/home/yin/Desktop/pdp_test.txt'
    s = tabu(inf_path,3,10)
    stop = time.time()
    print(stop-start)


    # test ADWL
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]
    # solution = [[0, 2, 12, 4, 14, 6, 16, 10, 20, 21], [0, 1, 11, 3, 13, 5, 15, 21], [0, 7, 17, 8, 18, 9, 19, 21]]
    # pkn = 10
    # C = 20
    # print(get_ADWL(solution,inf,pkn,C))

    # test cost
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0], [(40, 50), (35, 69), (40, 69), (38, 70), (42, 65), (38, 68), (15, 75), (20, 85), (15, 80), (22, 75), (30, 50), (45, 68), (45, 70), (42, 68), (40, 66), (35, 66), (25, 85), (22, 85), (20, 80), (18, 75), (25, 50), (40, 50)]]
    # solution = [[0, 2, 12, 4, 14, 6, 16, 10, 20, 21], [0, 1, 11, 3, 13, 5, 15, 21], [0, 7, 17, 8, 18, 9, 19, 21]]
    # pkn = 10
    # C = 20
    # print(cost(1,1,solution,inf,pkn,C))



    # test spi
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0],
    #        [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144,
    #         1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0],
    #        [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0],
    #        [(40, 50), (35, 69), (40, 69), (38, 70), (42, 65), (38, 68), (15, 75), (20, 85), (15, 80), (22, 75),
    #         (30, 50), (45, 68), (45, 70), (42, 68), (40, 66), (35, 66), (25, 85), (22, 85), (20, 80), (18, 75),
    #         (25, 50), (40, 50)]]
    # C = 20
    # solution = [[0, 2, 12, 4, 14, 5, 15, 21], [0, 1, 11, 7, 17, 9, 19, 21], [0, 3, 13, 6, 16, 8, 18, 10, 20, 21]]
    # [[0, 3, 1, 2, 13, 12, 11, 4, 14, 5, 15, 21], [0, 7, 17, 9, 19, 21], [0, 6, 16, 8, 18, 10, 20, 21]]
    # ini_solution = copy.deepcopy(solution)
    # c_solution = copy.deepcopy(solution)
    # for index_routes in range(len(solution)):
    #     for req in solution[index_routes]:
    #         if req != 0 and req != 21 and req <= 10:
    #             print(req)
    #             c_solution = spi(1,1,c_solution,index_routes,req,10,inf,C)
    #             print(c_solution)
    # solution = copy.deepcopy(ini_solution)