# BFS Algorithm: https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search

from collections import deque
from numpy import matrix
from Utility import Node
from Algorithm import Algorithm

class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.root = object
        self.matrix = [[] for i in range(20)]
        for i in range(20):
            for j in range(20):
                node = Node(i,j)
                neighbors = super().get_neighbors(node)
                self.matrix[i].append(neighbors)
        self.snake = object

    def run_algorithm(self, snake):
        self.snake = snake
        init, final = self.get_initstate_and_goalstate(self.snake)
        if (len(self.path) != 0):
            try:
                self.root = self.path.pop(0)
            except: pass

        else:
            self.root = Node(init.x, init.y)
            self.path = self.Explore()
            try:
                self.path.pop(0)
                self.root = self.path.pop(0)
            except:
                self.path = self.Explore()
        return self.root

    def Explore(self):
        init, final = self.get_initstate_and_goalstate(self.snake)
        queue = [[init,[init]]]
        visited = []
        while queue:
            vertex, path = queue.pop(0)
            visited.append(vertex)
            for node in self.matrix[int(vertex.x)][int(vertex.y)]:
                if int(node.x) == int(final.x) and int(node.y) == int(final.y):
                    return path + [final]
                else:
                    if (node not in visited 
                        and super().inside_body(self.snake, node) == False
                        and super().outside_boundary(node) == False):
                            visited.append(node)
                            queue.append([node, path + [node]])
        return path