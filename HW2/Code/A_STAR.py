from pydoc import visiblename
from Algorithm import Algorithm
from Utility import Node
from queue import PriorityQueue

class A_STAR(Algorithm):
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

        elif (len(self.path) == 0):
            for i in range(20):
                for j in range(20):
                    self.grid[i][j].f = 1000000
                    self.grid[i][j].g = 0
                    self.grid[i][j].h = 0
            self.root = Node(init.x, init.y)
            node = self.Explore()
            self.get_path(node)
            self.root = self.path.pop(0)
        return self.root

    def Explore(self):
        PQueue = []
        init, final = self.get_initstate_and_goalstate(self.snake)
        visited = []
        PQueue.append((0,init))
        while(len(PQueue)!= 0):
            PQueue.sort(key=lambda x:x[0])
            curr_node = PQueue.pop(0)
            curr_node = curr_node[1]
            if curr_node.x == final.x and curr_node.y == final.y:
                return curr_node
            visited.append(curr_node)
            neighbors = self.get_neighbors(curr_node)
            for neighbor in neighbors:
                if (
                        self.inside_body(self.snake, neighbor) == False
                        and self.outside_boundary(neighbor) == False
                        and curr_node.g + neighbor.h + 1 < neighbor.f
                    ):
                        neighbor.parent = curr_node
                        neighbor.h = self.manhattan_distance(neighbor,final)
                        neighbor.g = curr_node.g + 1
                        neighbor.f = neighbor.h + neighbor.g
                        if (neighbor not in PQueue):
                            PQueue.append((neighbor.f, neighbor))