from random import randrange
from pip import main


class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if (state[i] == state[j] or abs(state[j] - state[i]) == abs(i - j)):
                    return False
        
        return True

    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        val = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if (state[i] == state[j]):
                    val+=1
                if (abs(state[j] - state[i]) == abs(i - j)):
                    val+=1
        return self.N * self.N - val

    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        all_neighbors = []
        for i in range(self.N):
            for j in range(self.N):
                if (state[i] != j):
                    neighbor = list(state)
                    neighbor[i] = j
                    neighbor = tuple(neighbor)
                    all_neighbors.append(neighbor)

        return all_neighbors