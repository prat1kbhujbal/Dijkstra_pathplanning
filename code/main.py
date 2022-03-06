import argparse
import numpy as pb
from obstacle_plot import *
from dijkstra import *


def solvable(start_node, goal_node, map):
    '''Check if goal/start node on obstacle'''
    if map[start_node[0],
           start_node[1]] == 1 or map[goal_node[0],
                                      goal_node[1]] == 1:
        print("Start Node/Goal Node is inside the obstacle!! Please provide valid nodes.")
        return False
    return True


def main():
    '''Main Function'''
    Parser = argparse.ArgumentParser()
    Parser.add_argument(
        '--start', nargs='+', type=int, default=[100, 215],
        help='start node. Default: [100,215]')
    Parser.add_argument(
        '--goal', nargs='+', type=int, default=[100, 180],
        help='goal node. Default: [100,180]')
    Parser.add_argument(
        "--animate_explr",
        default=False,
        choices=('True', 'False'),
        help="Shows visualization while exploring. Default: False.")
    Parser.add_argument(
        "--visualize",
        default=True,
        choices=('True', 'False'),
        help="Shows visualization after goal reached. Default: True.")

    Args = Parser.parse_args()
    start_node = Args.start
    goal_node = Args.goal
    # Map Grid
    map_grid = [400, 250]
    explr_animation = str(Args.animate_explr)
    show_animation = str(Args.visualize)
    map = pb.zeros((map_grid[0], map_grid[1]), pb.uint8)
    plot_grid(start_node, goal_node, map_grid)
    map = obstacle(map)
    if solvable(start_node, goal_node, map):
        dijkstra(start_node, goal_node, map, explr_animation, show_animation)


if __name__ == "__main__":
    main()
