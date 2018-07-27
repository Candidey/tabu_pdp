import random
import copy
import time
import math

# add earliest time, latest time, load, service time, and coordinate into a list
def generate_inf(et,lt,load,st,coordinate,inf):
    inf.append(et)
    inf.append(lt)
    inf.append(load)
    inf.append(st)
    inf.append(coordinate)
    return inf

def admissible(route, inf, C):
    A = [0 for _ in range(len(route))]
    D = [0 for _ in range(len(route))]
    load = [0 for _ in range(len(route))]

    for i in range(1,len(route)-1):
        A[i] = D[i-1] + inf[3][route[i]]
        D[i] = max(inf[0][route[i]],A[i])
        load[i] = load[i-1] + inf[2][route[i]]
        if D[i] > inf[1][route[i]] or load[i] > C:
            # print(D[i],inf[1][route[i]])
            return False
    return True

def get_ADWL(solution, inf, pkn):
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

def cost(solution, inf, C):
    c_dist = 0

    for i in range(len(solution)):
        if not admissible(solution[i],inf,C):
            return 1000000

    # distance of arc
    coor = inf[4]
    for s in solution:
        for i in range(len(s)-1):
            c_dist += math.sqrt((coor[s[i]][0] - coor[s[i+1]][0]) ** 2 + (coor[s[i]][1] - coor[s[i+1]][1]) ** 2)

    cost = c_dist

    return cost

def moves(solution, pkn, C):
    bsc = 10000
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
                            if not admissible(c_solution[insert_route], inf, C):
                                c_solution[insert_route].remove(n)
                                continue
                            else:
                                # insert successor node
                                for suc_pos in range(pre_pos + 1, len(solution[insert_route])+1):
                                    c_solution[insert_route].insert(suc_pos, n + pkn)

                                    if not admissible(c_solution[insert_route],inf,C):
                                        c_solution[insert_route].remove(n + pkn)
                                        continue
                                    else:
                                        # print(c_solution)
                                        # print(csc)
                                        csc = cost(c_solution, inf, C)
                                        if csc < bsc:
                                            b_solution = copy.deepcopy(c_solution)
                                            bsc = csc
                                        c_solution[insert_route].remove(n+pkn)
                                c_solution[insert_route].remove(n)
    return bsc,b_solution

def get_initial_solution(inf,pkn,veh,C):
    solution = [[] for _ in range(veh)]
    pre_flag = False
    suc_flag = False

    for i in range(veh):
        solution[i].insert(0, 0)
        solution[i].append(pkn*2+1)

    for i in range(1,pkn+1):
        tabu = []
        it = 0

        while(not pre_flag or not suc_flag):
            if it == 0 :
                route = int(random.randint(0, veh - 1))
            else:
                while(route in tabu):
                    if len(tabu) >= veh:
                        return []
                    route = int(random.randint(0,veh-1))
            tabu.append(route)
            for pre_pos in range(1,len(solution[route])):
                solution[route].insert(pre_pos,i)
                pre_flag = admissible(solution[route],inf,C)
                if pre_flag:
                    for suc_pos in range(pre_pos+1,len(solution[route])):
                        solution[route].insert(suc_pos,i+pkn)
                        suc_flag = admissible(solution[route],inf,C)
                        if suc_flag:
                            break
                        else:
                            solution[route].remove(i+pkn)
                else:
                    solution[route].remove(i)
                if pre_flag and suc_flag:
                    break
            it = 1
        pre_flag = False
        suc_flag = False
    return solution

def compare(a, b):
    k = 0
    n = 0
    f1 = False
    f2 = False
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

def tabu(inf, veh, pkn, C):
    # global tabu

    # generate initial solution
    flag = True
    while(flag):
        initial_solution = get_initial_solution(inf, pkn, veh, C)
        if initial_solution != []:
            print(initial_solution)
            flag = False

    best_solution = copy.deepcopy(initial_solution)
    best_solution_cost = cost(best_solution,inf,C)
    print(best_solution_cost)
    iteration = 0
    while(iteration < 100):
        current_solution_cost, current_solution = moves(best_solution,pkn,C)

        if current_solution_cost < best_solution_cost:
            best_solution = copy.deepcopy(current_solution)
            best_solution_cost = current_solution_cost
        iteration += 1
    return best_solution

if __name__ == "__main__":
    et = []
    lt = []
    st = []
    load = []
    coordinate = []
    inf = []

    with open('/home/yin/Desktop/pdp_testv1.txt', 'r') as f:
        data = f.readlines()
        depots = len(data)
        pkn = int((depots - 2) / 2)
    for line in data:
        inf_line = line.split()
        inf_line = list(map(int, inf_line))

        coordinate.append((inf_line[1], inf_line[2]))
        load.append(inf_line[3])
        et.append(inf_line[4])
        lt.append(inf_line[5])
        st.append(inf_line[6])

    inf = generate_inf(et, lt, load, st, coordinate, inf)
    veh = 8
    C = 20

    start = time.time()
    s = tabu(inf, veh, pkn, C)
    print(s)
    print(cost(s,inf,C))
    stop = time.time()
    print(stop-start)

    # inf = [[0, 448, 621, 534, 105, 255, 179, 475, 278, 120, 100, 912, 825, 727, 170, 357, 652, 567, 384, 99, 155, 0],
    #        [1236, 505, 702, 605, 157, 324, 254, 528, 345, 162, 163, 967, 870, 782, 225, 410, 721, 620, 429, 220, 250,
    #         1236], [0, 10, 20, 10, 10, 20, 20, 10, 10, 10, 10, -10, -20, -10, -10, -20, -20, -10, -10, -10, -10, 0],
    #        [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0],
    #        [(40, 50), (35, 69), (40, 69), (38, 70), (42, 65), (38, 68), (15, 75), (20, 85), (15, 80), (22, 75),
    #         (30, 50), (45, 68), (45, 70), (42, 68), (40, 66), (35, 66), (25, 85), (22, 85), (20, 80), (18, 75),
    #         (25, 50), (40, 50)]]
    # pkn = 10
    # veh = 5
    # C = 20
    # flag = True
    # while(flag):
    #     s = get_initial_solution(inf,pkn,veh,C)
    #     if s != []:
    #         print(s)
    #         flag = False

    # s = [[0, 2, 12, 21], [0, 10, 20, 1, 11, 21], [0, 21], [0, 6, 16, 21], [0, 4, 14, 5, 15, 21], [0, 21], [0, 9, 19, 8, 18, 7, 17, 21], [0, 3, 13, 21]]
    # # s1 = [[0, 6, 16, 21], [0, 10, 20, 8, 18, 3, 13, 21], [0, 9, 19, 1, 11, 21], [0, 4, 14, 5, 15, 7, 17, 2, 12, 21], [0, 21]]
    # # print(cost(s1,inf,C))
    # print(moves(s,pkn,C))
