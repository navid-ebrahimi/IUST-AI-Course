import gymnasium as gym
import numpy as np
from QLearningImproved import Model
import cv2
import math
import json
import csv
from TemplateMatching import TemplateMatching
from LineDetection import LineDetection
import matplotlib.pyplot as plt

def draw_3D_chart(chart_data_time, chart_data_reward, chart_data_action):
  # creating the dataset
  chart_data_reward = chart_data_reward[77:]
  chart_data_action = chart_data_action[77:]
  chart_data_time = chart_data_time[77:]
  actions = []
  for action in chart_data_action:
    nums = []
    for num in action:
      num = round(num, 2)
      nums.append(num)
    actions.append((nums[0], nums[1], nums[2]))
  
  chart_data_action = actions
  chart_data_epsilon = [0.5] * len(chart_data_reward)
  barWidth = 0.25
  fig = plt.subplots(figsize =(12, 8))
  barWidth = 0.25
  br1 = np.arange(len(chart_data_reward))
  br2 = [x + barWidth for x in br1]
  br3 = [x + barWidth for x in br2]
  plt.bar(br1, chart_data_reward, color ='r', width = barWidth,
        edgecolor ='grey', label ='reward')
  plt.bar(br2, chart_data_epsilon, color ='g', width = barWidth,
        edgecolor ='grey', label ='epsilon')
  plt.xlabel('Actions', fontweight ='bold', fontsize = 15)
  plt.ylabel('Properties', fontweight ='bold', fontsize = 15)
  plt.xticks([r + barWidth for r in range(len(chart_data_reward))],
          chart_data_action)
  
  plt.legend()
  plt.show()
  # data = {'C':20, 'C++':15, 'Java':30,
  #         'Python':35}
  # courses = list(data.keys())
  # values = list(data.values())
    
  # fig = plt.figure(figsize = (10, 5))
  
  # # creating the bar plot
  # plt.bar(courses, values, color ='maroon',
  #         width = 0.4)
  
  # plt.xlabel("Courses offered")
  # plt.ylabel("No. of students enrolled")
  # plt.title("Students enrolled in different courses")
  # plt.show()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(chart_data_time, chart_data_reward,
    #            chart_data_action, c='r', marker='o')
    # ax.set_xlabel('Time')
    # ax.set_ylabel('Reward')
    # ax.set_zlabel('Action')
    # plt.show()
    # # save it in a image file
    # ax.figure.savefig('ImprovedQLearning_chart.png')

def shift_car_locations(car_locations, car_loc):
    for i in range(1, len(car_locations)-1):
        car_locations[i] = car_locations[i+1]
    car_locations[4] = car_loc
    return car_locations

def extract_tuple_from_string(string):
    string = string[1:]
    tup = tuple(map(float, string.split(', ')))
    return tup

def get_database():
  memory = {}
  with open('database.csv', 'r') as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        if row[0] == 'state':
            continue
        state = row[0]
        action = row[1]
        state = state[1:-1]
        state = state.split('), ')
        tup1 = extract_tuple_from_string(state[0])
        tup2 = extract_tuple_from_string(state[1])
        tup3 = extract_tuple_from_string(state[2][:-1])
        state = (tup1, tup2, tup3)
        action = action[1:-1]
        action = action.split(', ')
        action = tuple(map(float, action))
        Q = float(row[2])
        N = int(row[3])
        best_action = row[4]
        if state not in memory:
            memory[state] = [{}, None]
        memory[state][0][action] = [Q, N]
        if best_action == '':
            best_action = None
        else:
            best_action = best_action[1:-1]
            best_action = best_action.split(', ')
            best_action = tuple(map(float, best_action))
        memory[state][1] = best_action
  return memory

def write_to_database(model):
  with open('database.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['state', 'action', 'Q', 'N', 'best_action'])
    for state in model.memory:
      for action in model.memory[state][0]:
        writer.writerow([state, action, model.memory[state][0][action][0], model.memory[state][0][action][1], model.memory[state][1]])


env = gym.make("CarRacing-v2", render_mode="human")
car = cv2.imread('assets/car.png')
turn_left = cv2.imread('assets/turn_left.png')
turn_right = cv2.imread('assets/turn_right.png')
temp_match = TemplateMatching()
line_detect = LineDetection(50,150,1,np.pi/180,15,50,20)
episodes = 10
model = Model("model", 0.5)
mem = get_database()
if len(mem) != 0:
    model.memory = mem

model.ROAD_RGB =[100,100,100]
model.ENV_RGB = [100,202,100]


for episode in range(1, episodes+1):
    state = env.reset()
    current_state = state[0]
    done = False
    score = 0
    for i in range(0, 100):
        n_state, reward, done,a, info = env.step(env.action_space.sample())
        current_state = n_state
    frame1 = n_state[0:84, 0:96]
    x0, y0 = temp_match.template_loc(frame1, car, "car")
    car_locations = []
    for i in range(5):
        # finding average velocity
        x,y = temp_match.template_loc(frame1, car, "car")
        n_state, reward, done,a, info = env.step(env.action_space.sample())
        current_state = n_state
        car_locations.append((x,y))
        frame1 = n_state[0:84, 0:96]
    average_velocity = math.sqrt((x-x0)**2 + (y-y0)**2) / 5
    frame = current_state[0:84, 0:96]
    j = 0
    chart_data_time = []
    chart_data_reward = []
    chart_data_action = []
    while not done:
        env.render()
        chart_data_time.append(j)
        j += 1
        car_loc = temp_match.template_loc(frame, car, "car")
        left_loc = temp_match.template_loc(frame, turn_left, "turn_left")
        right_loc = temp_match.template_loc(frame, turn_right, "turn_right")
        lines_loc = line_detect.detect_lines(frame)
        curr_data = [car_loc, lines_loc, left_loc, right_loc, average_velocity]
        action, discrete = model.get_action(state, curr_data)
        chart_data_action.append(action)
        n_state, reward, done,a, info = env.step(action)
        chart_data_reward.append(reward)
        frame = n_state[0:84, 0:96]
        car_loc = temp_match.template_loc(frame, car, "car")
        lines_loc = line_detect.detect_lines(frame)
        left_loc = temp_match.template_loc(frame, turn_left, "turn_left")
        right_loc = temp_match.template_loc(frame, turn_right, "turn_right")
        car_locations = shift_car_locations(car_locations, car_loc)
        average_velocity = math.sqrt((car_locations[4][0]-car_locations[0][0])**2 + (car_locations[4][1]-car_locations[0][1])**2) / 5
        next_data = [car_loc, lines_loc, left_loc, right_loc, average_velocity]
        model.update_best_action(current_state, discrete, n_state, reward, curr_data, next_data)
        score+=reward
        current_state = n_state
        # write_to_database(model)
        # if j > 85:
        #   done = True
    # if episode == 1:
    #   draw_3D_chart(chart_data_time, chart_data_reward, chart_data_action)
    print('Episode:{} Score:{}'.format(episode, score))

