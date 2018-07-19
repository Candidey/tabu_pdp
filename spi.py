# swapping pairs between routes
import penalty
import copy


# def spi(solution,time_table, L_status):
#     """
#     :param sultion:
#     :param time_table:
#     :return:
#     """
#     for _ in time_table:
#         pick_up = len(_)/2 -1
#
#
#     for p in range(1, pick_up+1):
#         for i in range(len(solution)):
#             if p in solution[i]:
#                 insert(p,i,solution,L_status)
#     return []
#
#
# def insert(pre_node, index_route, pick_up, L_status, solution):
#     """
#     :param pre_node: predecessor node
#     :param i: the index of route
#     :param solution: the solution
#     :return: new solution
#     """
#     # new_solution = copy.deepcopy(solution)
#     #delete pre_node and successor node from inital route
#     solution[index_route].remove(pre_node)
#     solution[index_route].remove(pre_node+pick_up)
#     # del new_solution[i]
#     #insert the pre node to other routes , satisfies both time window and capacity constraints
#     for i in len(solution):
#         if i != index_route:
#             for pos in range(1,len(solution[i])):
#                 solution[i].insert(pos,pre_node)
#                 if True:
#                     # insert successor node
#                     L_status[(pre_node, pos)] = L_status[(pre_node,)]
#                 else:
#                     # delete pre node
#
#
#
#
#
#     return new_solution


def tabu(solution):

    pass




def spi(solution,time_table):





















