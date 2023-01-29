import random
import math
class Model:
    STEER_ACTIONS_NUM = 10 # for 10 : -5 to 5 including -5 and 5
    # (180/steer_actions_num) * X / 90
    GAS_ACTIONS_NUM = 5 # for 5 : 0 to 5 including 0 and 5
    # (1/gas_actions_num) * X
    BRAKE_ACTIONS_NUM = 5
    # (1/brake_actions_num) * X
    MAX_VELOCITY = 20
    ROAD_WIDTH = 10
    ROAD_RGB = [0, 0, 0]
    ENV_RGB = [0, 0, 0]
    def __init__(self, name, epsilon):
        self.name = name
        self.epsilon = epsilon
        self.gamma = 0.9
        self.learning_rate = 0.9
        self.k = 1000
        positions = [(-1.0,0.0),(0.0,0.5),(0.5,1.0)]
        curves = [(-1.0,-0.2),(-0.2,0.2),(0.2,1.0)]
        velocities = [(-1.0,0.0),(0.0,0.5),(0.5,1.0)]
        self.states = []
        for pos in positions:
          for curve in curves:
            for vel in velocities:
              self.states.append((pos,curve,vel))
        self.memory = {}
            # memory = {
            # STATE1 : [{
            #     action1 : [q1, n1]
            #     action2 : [q2, n2]
            #     ...
            # }, best_action_until_now]
            # ...
            # }
        for state in self.states:
          self.memory[state] = [{}, None]
    def f(self, action, state):
      return self.memory[state][0][action][0] + self.k / self.memory[state][0][action][1]

    def specify_state(self, data):
        car_loc, lines_loc, left_loc, right_loc, avg_v = data
        a1,b1,c1,a2,b2,c2 = 0,0,0,0,0,0
        if lines_loc is not None:
          if len(lines_loc) > 2:
            a1,b1,c1 = self.get_line_equation(lines_loc[0])
            a2,b2,c2 = self.get_line_equation(lines_loc[1])
        try:
          dis1 = abs(a1*car_loc[0]+b1*car_loc[1]+c1)/math.sqrt(a1**2+b1**2)
          dis2 = abs(a2*car_loc[0]+b2*car_loc[1]+c2)/math.sqrt(a2**2+b2**2)
        except:
          dis1, dis2 = 0,0
        if dis1 + dis2 < self.ROAD_WIDTH:
          # pos_f [-1,1]
          pos_f = 1 - abs(dis1-dis2)/self.ROAD_WIDTH
        else:
          dis_out = min(dis1,dis2)
          pos_f = -(dis_out)/self.ROAD_WIDTH
          if pos_f < -1:
            pos_f = -1
        # curve_f [-1,1]
        # TODO: get the slope of the road
        curve_f = 1
        if self.is_turn_left(car_loc, left_loc) or self.is_turn_right(car_loc, right_loc):
          curve_f = pos_f
        # mapping average velocity to [-1,1]
        # velocity_f [0,1]
        velocity_f = avg_v/self.MAX_VELOCITY
        for cat in self.states:
          if pos_f >= cat[0][0] and pos_f < cat[0][1] and curve_f >= cat[1][0] and curve_f < cat[1][1] and velocity_f >= cat[2][0] and velocity_f < cat[2][1]:
            return cat
        return self.states[0]
    def explore(self, state, data):
        random_steer_action = random.randint(-self.STEER_ACTIONS_NUM/2, self.STEER_ACTIONS_NUM/2 + 1)
        random_gas_action = random.randint(0, self.GAS_ACTIONS_NUM + 1)
        random_brake_action = random.randint(0, self.BRAKE_ACTIONS_NUM + 1)
        random_steer_action1 = (180 / self.STEER_ACTIONS_NUM) * random_steer_action / 90
        random_gas_action1 = 1 / self.GAS_ACTIONS_NUM * random_gas_action
        random_brake_action1 = 1 / self.BRAKE_ACTIONS_NUM * random_brake_action
        feature_state = self.specify_state(data)
        if (random_steer_action, random_gas_action, random_brake_action) not in self.memory[feature_state][0]:
            self.memory[feature_state][0][(random_steer_action, random_gas_action, random_brake_action)] = [0, 0]
            self.memory[feature_state][1] = (random_steer_action, random_gas_action, random_brake_action)
        return (random_steer_action1, random_gas_action1, random_brake_action1), (random_steer_action, random_gas_action, random_brake_action)

    def exploid(self, state, data):
        feature_state = self.specify_state(data)
        if self.memory[feature_state][1] is None:
            return self.explore(state, data)
        best = self.memory[feature_state][1]
        random_steer_action = (180 / self.STEER_ACTIONS_NUM) * best[0] / 90
        random_gas_action = 1 / self.GAS_ACTIONS_NUM * best[1]
        random_brake_action = 1 / self.BRAKE_ACTIONS_NUM * best[2]
        return (random_steer_action, random_gas_action, random_brake_action), best
    def update_best_action(self, current_state, action, next_state, reward, curr_data, next_data):
        next_state_best_q = 0
        feature_next_state = self.specify_state(next_data)
        feature_current_state = self.specify_state(curr_data)
        if self.memory[feature_next_state][1] is not None:
          next_state_best_action = self.memory[feature_next_state][1]
          next_state_best_q = self.memory[feature_next_state][0][next_state_best_action][0]
        new_q = reward + self.gamma * next_state_best_q
        self.memory[feature_current_state][0][action][0] = new_q
        self.memory[feature_current_state][0][action][1] += 1
        if self.f(action, feature_current_state) > self.f(self.memory[feature_current_state][1], feature_current_state):
            self.memory[feature_current_state][1] = action
        
        self.normalize()
      
    def get_action(self, state, data):
        if random.random() < self.epsilon:
            return self.explore(state, data)
        else:
            return self.exploid(state, data)
    
    def get_line_equation(self, line):
      x1, y1, x2, y2 = line[0]
      b = 1
      a = (y2 - y1) / (x1 - x2)
      c = -y1 - a * x1
      return a, b, c

    def is_turn_left(self, car_loc, left_loc):
      x1, y1 = car_loc
      x2, y2 = left_loc
      if abs(x1 - x2) < 0.1 and abs(y1 - y2) < 0.1:
        return True
      return False

    def is_turn_right(self, car_loc, right_loc):
      x1, y1 = car_loc
      x2, y2 = right_loc
      if abs(x1 - x2) < 0.1 and abs(y1 - y2) < 0.1:
        return True
      return False

    def normalize(self):
        # self.epsilon = 1 / (1 + 0.001 * self.epsilon)
        if(self.epsilon > 0.05):
            self.epsilon -= 0.001
        
        if(self.learning_rate > 0.05):
            self.learning_rate -= 0.001