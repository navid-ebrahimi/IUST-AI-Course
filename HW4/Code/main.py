from time import time
from hill_climbing import hill_climbing_random_restart
from NQueens import NQueens


if __name__ == "__main__":
    print("Running local search for N Queens Problem")
    size = eval(input(" - Please input the size of the board (4~15): "))
    print("\nhill_climbing_random_restart")
    
    problem = NQueens(size)
    times = 10
    cnt = 0
    start = time()
    for i in range(times):
        result = hill_climbing_random_restart(problem)
        if problem.goal_test(result):
            cnt += 1
    print(" - Accuracy: %2d/%d\tRunning time: %f"%(cnt, times, time()-start))
