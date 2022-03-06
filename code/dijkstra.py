import numpy as pb
import matplotlib.pyplot as plt
from queue import PriorityQueue


class Dijkstra:
    '''Class for Dijkstra'''

    def __init__(self, position, cost, parent):
        self.position = position
        self.cost = cost
        self.parent = parent


def verify_node(node):
    '''Check for borders with clearance of 5 mm'''
    px = node[0]
    py = node[1]

    if px < 5:
        return False
    if py < 5:
        return False
    if px >= 395:
        return False
    if py >= 245:
        return False
    return True


def actions(px, py):
    '''Explore paths'''
    actions = [
        (px, py + 1),
        (px + 1, py),
        (px - 1, py),
        (px, py - 1),
        (px + 1, py + 1),
        (px - 1, py - 1),
        (px - 1, py + 1),
        (px + 1, py - 1)]
    return actions


def planning(node, map):
    '''Returns explored paths and corresponding costs'''
    px = node.position[0]
    py = node.position[1]
    action = actions(px, py)
    explore = []

    for i, path in enumerate(action):
        if verify_node(path):
            if map[path[0]][path[1]] == 0:
                if i > 3:
                    cost = pb.sqrt(2)
                else:
                    cost = 1
                explore.append([path, cost])
    return explore


def dijkstra(start, goal, map, expl_animation, show_animation):
    '''dijkstra algorithm'''
    distance = {}
    pque = PriorityQueue()
    visited_nodes = []
    node_object = {}
    distance[str(start)] = 0
    visited_nodes.append(str(start))
    start_node = Dijkstra(start, 0, None)
    goal_node = Dijkstra(goal, 0, None)
    node_object[str(start_node.position)] = start_node
    pque.put([start_node.cost, start_node.position])
    eplr_x = []
    eplr_y = []
    while not pque.empty():
        current_node = pque.get()
        node = node_object[str(current_node[1])]
        if current_node[1][0] == goal_node.position[0] and current_node[1][1] == goal_node.position[1]:
            print("Goal Reached !!")

            goal_node.position = goal
            goal_node.cost = current_node[0]
            goal_node.parent = node
            node_object[str(goal)] = goal_node
            break
        for i, cost in planning(node, map):
            if str(i) in visited_nodes:
                cost = cost + distance[str(node.position)]
                if cost < distance[str(i)]:
                    distance[str(i)] = cost
                    node_object[str(i)].parent = node
            else:
                visited_nodes.append(str(i))
                eplr_x.append(i[0])
                eplr_y.append(i[1])
                if expl_animation == str(
                        True) and show_animation == str(False):
                    plt.plot(i[0], i[1], ".b")
                    plt.pause(0.00000000000000000001)
                cost = cost + distance[str(node.position)]
                distance[str(i)] = cost
                new_node = Dijkstra(
                    i, cost, node_object[str(node.position)])
                node_object[str(i)] = new_node
                pque.put([cost, new_node.position])
    if show_animation == str(True):
        print("Showing Exploration")
        for i in range(len(eplr_x)):
            plt.plot(eplr_x[i], eplr_y[i], ".b")
            plt.pause(0.00000000000000000001)
    goal_node = node_object[str(goal)]
    parent_node = goal_node.parent

    path_x = []
    path_y = []
    while parent_node:
        path_x.append(parent_node.position[0])
        path_y.append(parent_node.position[1])
        parent_node = parent_node.parent
        plt.plot(path_x, path_y, "-r", markersize=2)
        plt.pause(0.00001)
    plt.show()
