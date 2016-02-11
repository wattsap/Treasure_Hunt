#!/usr/bin/python

import collections
import random
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def contains(self, item):
        return not self.is_empty() and item in list(zip(*self.elements))[1]

def dfs(grid):

    # do the search
    result = dfs_iterative(grid)
    result2 = bfs_iterative(grid)
    result3 = ucs_iterative(grid)


    print ("Depth First Search")
    # print expanded nodes
    print (len(result['visited']))
    for pos in result['visited']:
        print (str(pos[0]) + ' ' + str(pos[1]))

    print ("Breath First Search")
    print (len(result2['visited']))
    for pos in result2['visited']:
        print (str(pos[0]) + ' ' + str(pos[1]))

    print ("Uniform Cost Search")
    path = reconstruct_path(finish_state, result3)
    print (len(path)-1)  # distance is -1
    for pos in path:
        print (str(pos[0]) + ' ' + str(pos[1]))


    # print path
    #path = reconstruct_path(finish_state, result['came_from'])
    #print (len(path)-1)  # distance is -1
    #for pos in path:
        #print (str(pos[0]) + ' ' + str(pos[1]))


# ---------------------------------------------------------------------------
# Depth First Search
#
# * take element from the fringe
# * if it's the goal -> success
# * otherwise add all of it's neighbours that have not yet been
#     looked at to the fringe
#
# Store the path by recording where we came from.
#   See: http://www.redblobgames.com/pathfinding/a-star/introduction.html
#   Alternative: store not only nodes but also their parents in visited
# ---------------------------------------------------------------------------

def dfs_iterative(grid):
    global finish_state
    fringe = collections.deque()  # nodes under consideration
    came_from = {}  # our closed set & node parent information
    visited = []  # only needed for hackerrank - print expanded nodes at end

    # start state
    start = (11, 11)
    fringe.append(start)
    came_from[start] = None

    while len(fringe) > 0:
        current = fringe.pop()  # depth first
        visited.append(current)

        if is_goal(current, grid):  # done?
            finish_state = current
            print (finish_state)
            return {'visited': visited, 'came_from': came_from}

        # expand all possible moves from current
        neighbours = get_neighbours(current, grid)
        for next in neighbours:

            # don't expand (or explore) nodes twice
            if next not in came_from and next not in fringe:
                came_from[next] = current
                fringe.append(next)

def bfs_iterative(grid):
    global finish_state
    fringe = collections.deque()  # nodes under consideration
    came_from = {}  # our closed set & node parent information
    visited = []  # only needed for hackerrank - print expanded nodes at end

    # start state
    start = (11, 11)
    fringe.append(start)
    came_from[start] = None

    while len(fringe) > 0:
        current = fringe.popleft()
        visited.append(current)

        if is_goal(current, grid):  # done?
            finish_state = current
            print (finish_state)
            return {'visited': visited, 'came_from': came_from}

        # expand all possible moves from current
        neighbours = get_neighbours(current, grid)
        for next in neighbours:

            # don't expand (or explore) nodes twice
            if next not in came_from and next not in fringe:
                came_from[next] = current
                fringe.append(next)

def ucs_iterative(grid):
    global finish_state
    fringe = PriorityQueue()   # nodes under consideration
    came_from = {}  # our closed set & node parent information
    cost_so_far = {} # only needed for hackerrank - print expanded nodes at end

    # start state
    start = (11, 11)
    fringe.put(start, 0)
    cost_so_far[start] = 0
    came_from[start] = None

    while not fringe.is_empty() > 0:
        current = fringe.get()


        if is_goal(current, grid):  # done?
            finish_state = current
            return came_from

        # expand all possible moves from current
        neighbours = get_neighbours(current, grid)
        for next in neighbours:

            new_cost = cost_so_far[current] + cost_of_move(next, grid)

            # don't expand (or explore) nodes twice
            if (next not in came_from and not fringe.contains(next)) or (new_cost < cost_so_far[next]):
                came_from[next] = current
                cost_so_far[next] = new_cost
                fringe.put(next, new_cost)

def cost_of_move(pos, grid):
    return 0 if is_goal(pos, grid) else 1


# gets all neighbours for a position on the grid, only returns valid moves
def get_neighbours(pos, grid):
    (x, y) = pos
    step = grid[pos[0]][pos[1]]
    neighbours = [(x-step, y  ),  # up
                  (x,   y-step),  # left
                  (x,   y+step),  # right
                  (x+step, y  )]  # down
    neighbours = filter(lambda x: is_passable(x, grid), neighbours)
    return neighbours


def is_passable(pos, grid):
    x,y = pos[0],pos[1]
    return (x >= 0 and x < 21) and (y >= 0 and y < 21)


def is_goal(pos, grid):
    x,y = pos[0],pos[1]
    return (x == 0 and y == 0) or (x == 0 and y == 20) or (x == 20 and y == 0) or ( x == 20 and y == 20)


def is_start(pos, grid):
    x,y = pos[0],pos[1]
    return x == 11 and y == 11


# build path from start to goal
def reconstruct_path(goal, came_from):
    current = goal
    path = [current]
    while not is_start(current, grid):
        print (current)
        current = came_from[current]
        path.append(current)
    return path[::-1]  # reverse




# PREDEFINED TEMPLATE CODE -----------------------------------------
start_state = (11,11)
finish_state = (0,0)
grid = [[random.randint(1,9) for x in range(21)] for x in range(21)]


dfs(grid)