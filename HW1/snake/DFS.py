# DFS Algorithm: https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search

from Fruit import Fruit
from Utility import Node
from Algorithm import Algorithm
from Utility import Node

class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
        self.root = object
        self.matrix = [[] for i in range(20)]
        for i in range(20):
            for j in range(20):
                node = Node(i,j)
                neighbors = self.get_neighbors(node)
                self.matrix[i].append(neighbors)
        self.snake = object

    def run_algorithm(self, snake):
        self.snake = snake
        init, final = self.get_initstate_and_goalstate(self.snake)
        if (len(self.path) != 0):
            try:
                self.root = self.path.pop(0)
            except: pass

        if (len(self.path) == 0):
            self.root = Node(init.x, init.y)
            self.path = self.Explore()
            self.path.pop(0)
            self.root = self.path.pop(0)
        return self.root


    def Explore(self):
        init, final = self.get_initstate_and_goalstate(self.snake)
        stack = [[init, [init]]]
        visited = []
        while stack:
            (vertex, path) = stack.pop()
            if (vertex not in visited):
                if vertex.x == final.x and vertex.y == final.y:
                    return path
                visited.append(vertex)
                for node in self.matrix[int(vertex.x)][int(vertex.y)]:
                    if (node not in visited 
                        and self.inside_body(self.snake, node) == False
                        and self.outside_boundary(node) == False):
                        stack.append((node, path + [node]))