from os import stat


def hill_climbing(problem, state):
    ''' Returns a state as the solution of the problem '''
    all_neighbors = problem.neighbors(state)
    max = problem.value(state)
    for i in range(len(all_neighbors)):
        if (max <= problem.value(all_neighbors[i])):
            max = problem.value(all_neighbors[i])
            state = all_neighbors[i]
    return state

def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem, state)
        cnt += 1
    return state