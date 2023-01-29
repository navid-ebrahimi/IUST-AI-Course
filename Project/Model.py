import random
class Model:
    STEER_ACTIONS_NUM = 10 # for 10 : -5 to 5 including -5 and 5
    # (180/steer_actions_num) * X / 90
    GAS_ACTIONS_NUM = 5 # for 5 : 0 to 5 including 0 and 5
    # (1/gas_actions_num) * X
    BRAKE_ACTIONS_NUM = 5
    # (1/brake_actions_num) * X
    def __init__(self, name, epsilon):
        self.name = name
        self.epsilon = epsilon
        self.gamma = 0.9
        self.learning_rate = 0.9
        self.k = 1000
        self.memory = {}
            # memory = {
            # STATE1 : [{
            #     action1 : [q1, n1]
            #     action2 : [q2, n2]
            #     ...
            # }, best_action_until_now]
            # ...
            # }
    def f(self, action, state):
      return self.memory[state][0][action][0] + self.k / self.memory[state][0][action][1]

    def explore(self, state):
        random_steer_action = random.randint(-self.STEER_ACTIONS_NUM/2, self.STEER_ACTIONS_NUM/2 + 1)
        random_gas_action = random.randint(0, self.GAS_ACTIONS_NUM + 1)
        random_brake_action = random.randint(0, self.BRAKE_ACTIONS_NUM + 1)
        random_steer_action = (180 / self.STEER_ACTIONS_NUM) * random_steer_action / 90
        random_gas_action = 1 / self.GAS_ACTIONS_NUM * random_gas_action
        random_brake_action = 1 / self.BRAKE_ACTIONS_NUM * random_brake_action
        if state not in self.memory:
            self.memory[state] = [None, None]
            self.memory[state][0] = {}
        if (random_steer_action, random_gas_action, random_brake_action) not in self.memory[state][0]:
            self.memory[state][0][(random_steer_action, random_gas_action, random_brake_action)] = [0, 0]
            self.memory[state][1] = (random_steer_action, random_gas_action, random_brake_action)
        return random_steer_action, random_gas_action, random_brake_action

    def exploid(self, state):
        if state in self.memory:
            return self.memory[state][1]
        else:
            return self.explore(state)

    def update_best_action(self, current_state, action, next_state, reward):
        if next_state not in self.memory:
            self.memory[next_state] = [None, None]
            self.memory[next_state][0] = {}
        
        next_state_best_q = 0
        if self.memory[next_state][1] is not None:
          next_state_best_action = self.memory[next_state][1]
          next_state_best_q = self.memory[next_state][0][next_state_best_action]
        new_q = reward + self.gamma * next_state_best_q
        self.memory[current_state][0][action][0] = new_q
        self.memory[current_state][0][action][1] += 1
        if self.f(action, current_state) > self.f(self.memory[current_state][1], current_state):
            self.memory[current_state][1] = action
        
        self.normalize()
      
    def get_action(self, state):
        if random.random() < self.epsilon:
            return self.explore(state)
        else:
            return self.exploid(state)
        

    def normalize(self):
        # self.epsilon = 1 / (1 + 0.001 * self.epsilon)
        if(self.epsilon > 0.05):
            self.epsilon -= 0.001
        
        if(self.learning_rate > 0.05):
            self.learning_rate -= 0.001