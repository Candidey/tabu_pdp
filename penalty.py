# the penalty for capacity violations and time violations
def penalty(solution, time_table):
    """
    time_table: time_table[0] = et, time_table[1] = lt, time_table[2] = load, time_table[3] = st, st is travel time
    :param solution: routes
    :param time_table: all kinds of time like earliest time, latest time, service time
    :return: penalty
    """
    for _ in time_table:
        pick_up = len(_)/2 - 1
        pick_up = int(pick_up)

    vehicles= len(solution)

    """
    A: arrival time
    D: departure time
    W: waiting time
    """
    PEN_TW = 1
    PEN_LD = 100
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
                load[i] = time_table[2][i]
                if i > pick_up:
                    A[i] = M
                    D[i] = max(A[route[count_route]], time_table[0][i])
                    W[i] = D[i] - A[i]
                else:
                    A[i] = 0
                    D[i] = max(A[route[count_route]], time_table[0][i])
                    W[i] = D[i] - A[i]
            elif count_route == len(route) - 2:
                load[i] = load[route[count_route-1]] + time_table[2][i]
                if i <= pick_up:
                    A[i] = M
                    D[i] = max(A[route[count_route]], time_table[0][i])
                    W[i] = D[i] - A[i]
                else:
                    load[i] = load[route[count_route - 1]] + time_table[2][i]
                    A[i] = time_table[3][route[count_route - 1]] + D[route[count_route - 1]]
                    D[i] = max(A[route[count_route]], time_table[0][i])
                    W[i] = D[i] - A[i]
            else:
                load[i] = load[route[count_route-1]] + time_table[2][i]
                A[i] = time_table[3][route[count_route-1]] + D[route[count_route-1]]
                D[i] = max(A[route[count_route]], time_table[0][i])
                W[i] = D[i] - A[i]

            # travle_time[count_routes] = sum
            count_route += 1

    s_tw = 0
    s_ld = 0
    for i in range(1, pick_up*2+1):
        t = A[i] - time_table[1][i]
        s_tw = s_tw + max(0, t)
        l = load[i] - C
        s_ld = s_ld + max(0, l)

    Z = PEN_TW*s_tw + PEN_LD*s_ld

    return Z

time_table = [[0, 448, 621, 534, 15, 255, 179, 475, 278, 30, 10, 912, 825, 727, 170, 357, 652, 567, 384, 99, 65, 0], [1236, 505, 702, 605, 67, 324, 254, 528, 345, 92, 73, 967, 870, 782, 225, 410, 721, 620, 429, 148, 144, 1236], [0, 10, 20, 10, 10, 20, 20, 40, 10, 30, 10, -10, -20, -10, -10, -20, -20, -40, -10, -30, -10, 0], [0, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 0]]


if __name__ == "__main__":
    solution = [[0,4,7,14,17,21]]
    z= penalty(solution, time_table)
    print(z)
        # print(inf)