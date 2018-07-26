import random
import math
import copy
import time
import operator


# add earliest time, latest time, load, service time, and coordinate into a list
def generate_inf(et,lt,load,st,coordinate,inf):
    inf.append(et)
    inf.append(lt)
    inf.append(load)
    inf.append(st)
    inf.append(coordinate)
    return inf

# generate initial solution
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

# get arrive time, depart time, wait time and load at each node
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
                    D[i] = max(A[route[count_route]], inf[0][i])
                    W[i] = D[i] - A[i]
            else:
                load[i] = load[route[count_route - 1]] + inf[2][i]
                A[i] = inf[3][route[count_route - 1]] + D[route[count_route - 1]]
                D[i] = max(A[route[count_route]], inf[0][i])
                W[i] = D[i] - A[i]

            count_route += 1

    AWDL = []
    AWDL.append(A)
    AWDL.append(D)
    AWDL.append(W)
    AWDL.append(load)

    return AWDL

#  the solution satisfy time windows and load constraints or not
def tw_ld_flag(adwl):
    tw_flag = True
    ld_flag = True

    for i in adwl[2]:
        if i < 0:
            tw_flag = False
    for i in adwl[3]:
        if i < 0:
            ld_flag = False

    return tw_flag, ld_flag

# cost of the solution
def cost(x, y, solution, inf, pkn, C):
    c_dist = 0
    c_ld = 0
    c_tw = 0
    f1 = True
    f2 = True


    adwl = get_ADWL(solution, inf, pkn, C)
    A = adwl[0]
    load = adwl[1]
    # violation of time window and load
    for i in range(1,pkn*2+1):
        t = A[i] - inf[1][i]
        if t > 0:
            f1 = False
        c_tw = c_tw + max(0,t)
        l = load[i] - C
        if l > 0:
            f2 = False
        c_ld = c_ld + max(0,l)

    # distance of arc
    # coor = inf[4]
    # for s in solution:
    #     for i in range(len(s)-1):
    #         c_dist += math.sqrt((coor[s[i]][0] - coor[s[i+1]][0]) ** 2 + (coor[s[i]][1] - coor[s[i+1]][1]) ** 2)

    # cost = c_dist + x*c_tw + y*c_ld
    cost = x * c_tw + y * c_ld

    return f1, f2, cost

# an admissble placement is one where the predecessor node satisfies both time window and capacity constraints
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


# single paired insertion
def spi(x, y, f_solution, index_routes, req, pkn, inf, C):
    solution = copy.deepcopy(f_solution)
    init_solution = copy.deepcopy(solution)
    # current solution and cost
    c_solution = copy.deepcopy(solution)
    c_cost = cost(x, y, c_solution, inf, pkn, C)
    # best solution and cost
    b_solution = copy.deepcopy(solution)
    b_cost = c_cost

    solution[index_routes].remove(req)
    solution[index_routes].remove(req+pkn)

    # performs the following process for the predecessor node
    for i in range(len(solution)):
        if i != index_routes:
            # select the placement to insert
            for pre_pos in range(1, len(solution[i])):
                solution[i].insert(pre_pos, req)
                # is it a admissible placement or not
                flag = feasiable(solution[i], pre_pos, inf, pkn*2 +2, C)
                if flag:
                    # insert successor node
                    for suc_pos in range(pre_pos+1, len(solution[i])):
                        solution[i].insert(suc_pos, req+pkn)
                        c_solution = copy.deepcopy(solution)
                        adwl = get_ADWL(c_solution, inf, pkn, C)
                        tw_flag, ld_flag = tw_ld_flag(adwl)
                        # adjust the parameter
                        if tw_flag:
                            x = x / (1 + z)
                        else:
                            x = x * (1 + z)
                        if ld_flag:
                            y = y / (1 + z)
                        else:
                            y = y * (1 + z)
                        c_cost = cost(x, y, c_solution, inf, pkn, C)
                        if c_cost < b_cost:
                            b_solution = copy.deepcopy(c_solution)
                            b_cost = c_cost
                        solution[i].remove(pkn+req)
                solution[i].remove(req)
        solution = copy.deepcopy(init_solution)

        return x, y, b_solution

def sbr(f_solution, pkn):
    solution = copy.deepcopy(f_solution)
    route_n1 = 0
    route_n2 = 0
    flag_n1 = False
    flag_n2 = False
    pre_n2 = 0
    while(route_n1 == route_n2):
        pre_n1 = int(random.randint(1, pkn))
        pre_n2 = int(random.randint(1, pkn))
        for i in range(len(solution)):
            if pre_n1 in solution[i]:
                route_n1 = i
                index_n1 = solution[i].index(pre_n1)
                flag_n1 = True
            if pre_n2 in solution[i]:
                route_n2 = i
                index_n2 = solution[i].index(pre_n2)
                flag_n2 = True
            if flag_n1 and flag_n2:
                break

    suc_n1 = pre_n1 + pkn
    suc_n2 = pre_n2 + pkn
    index_sn1 = solution[route_n1].index(suc_n1)
    index_sn2 = solution[route_n2].index(suc_n2)

    pk1 = solution[route_n1][index_n1]
    s1 = solution[route_n1][index_sn1]
    solution[route_n1][index_n1] = solution[route_n2][index_n2]
    solution[route_n2][index_n2] = pk1
    solution[route_n1][index_sn1] = solution[route_n2][index_sn2]
    solution[route_n2][index_sn2] = s1

    return solution

def moves(solution,pkn):
    nd = []
    for i in range(len(solution)):
        for n in solution[i]:
            if n != 0 and n != (2*pkn +2) and n <= pkn:
                c_solution = copy.deepcopy(solution)
                c_solution[i].remove(n)
                c_solution[i].remove(n + pkn)
                for insert_route in range(len(solution)):
                    if insert_route != i:
                        for pre_pos in range(1, len(solution[insert_route])):
                            c_solution[insert_route].insert(pre_pos, n)
                            # insert successor node
                            for suc_pos in range(pre_pos + 1, len(solution[insert_route])+1):
                                c_solution[insert_route].insert(suc_pos, n + pkn)
                                s_nd = copy.deepcopy(c_solution)
                                nd.append(s_nd)
                                c_solution[insert_route].remove(n+pkn)
                            c_solution[insert_route].remove(n)
    return nd

def inRoute(solution, pkn):
    pass


def tabu(file_path, veh, C):
    global inf
    global  pkn # number of pickup nodes
    global x
    global y
    global z
    global tabu
    global f1
    global f2

    x = 1
    y = 1
    z = 0.5

    et = []
    lt = []
    st = []
    load = []
    coordinate = []
    inf = []
    tabu = []

    # read file and add data into a list
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
    # generate initial solution
    initial_solution = get_initial_solution(pkn, veh)
    current_solution = copy.deepcopy(initial_solution)
    best_solution = copy.deepcopy(initial_solution)
    f1, f2, best_solution_cost = cost(x, y, best_solution, inf, pkn, C)

    print(initial_solution)

    iteration = 0
    while(iteration < 100):
        n_cs = moves(best_solution,pkn)
        for s in n_cs:
            s_f1, s_f2, s_cost = cost(x,y,s,inf,pkn,C)
            # print(s)
            # print(s_cost)
            mark = compare(best_solution, s)
            if s_cost < best_solution_cost:
                if mark not in tabu:
                    tabu.append(mark)
                    print('tabu', tabu)
                    best_solution = copy.deepcopy(s)
                    best_solution_cost = s_cost
            #         f1 = s_f1
            #         f2 = s_f2
            # if f1:
            #     x = x/1.5
            # else:
            #     x = x*1.5
            # if f2:
            #     y = y/1.5
            # else:
            #     y = y*1.5

        iteration += 1
    print('best cost', best_solution_cost)
    return best_solution


def compare(a, b):
    k = 0
    n = 0
    f1 = False
    f2 = True
    for i in range(len(a)):
        if len(b[i]) < len(a[i]):
            k = i
            f1 = True
        elif len(b[i]) > len(a[i]):
            mark = list(set(b[i]).difference(set(a[i])))
            if mark[0] > mark[1]:
                n = mark[1]
            else:
                n = mark[0]
            f2 = True
        if f1 and f2:
            break
    return n,k
if __name__ == "__main__":
    start = time.time()
    inf_path = '/home/yin/Desktop/pdp_test.txt'
    s = tabu(inf_path,3,10)
    print(s)
    stop = time.time()
    print(stop-start)

    # test compare
    # print(compare([[0, 2, 7, 11], [0, 1,4,9, 6,11]],[[0,2,7,4,9,11],[0,1,6,11]]))



    # test moves()
    # solution = [[0,1,2,6,7,11],[0,4,9,11]]
    # print(moves(solution,5))


    # test sbr
    # solution = get_initial_solution(10,3)
    # print(solution)
    # print(sbr(solution, 10))


    # test ADWL
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]
    # solution = [[0, 2, 12, 4, 14, 6, 16, 10, 20, 21], [0, 1, 11, 3, 13, 5, 15, 21], [0, 7, 17, 8, 18, 9, 19, 21]]
    # pkn = 10
    # C = 20
    # print(get_ADWL(solution,inf,pkn,C))

    # test cost
    # inf = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0], [(40, 50), (35, 69), (40, 69), (38, 70), (42, 65), (38, 68), (15, 75), (20, 85), (15, 80), (22, 75), (30, 50), (45, 68), (45, 70), (42, 68), (40, 66), (35, 66), (25, 85), (22, 85), (20, 80), (18, 75), (25, 50), (40, 50)]]
    # # solution = [[0, 21], [0, 2, 9, 12, 19, 3, 13, 4, 14, 6, 16, 7, 17, 8, 18, 10, 20, 21], [0, 1, 11, 5, 15, 21]]
    # solution = [[0, 1, 2, 12, 3, 11, 13, 21], [0, 4, 14, 5, 15, 6, 16, 7, 17, 10, 20, 21], [0, 8, 18, 9, 19, 21]]
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