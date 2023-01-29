import gymnasium as gym
import numpy as np
from Model import Model
env = gym.make("CarRacing-v2", domain_randomize=True, render_mode="human")
episodes = 10
model = Model("model", 0.9)
for episode in range(1, episodes+1):
    state = env.reset()
    state = state[0].tolist()
    state = str(state)
    done = False
    score = 0
    while not done:
        env.render()
        action = model.get_action(state)
        n_state, reward, done,a, info = env.step(action)
        n_state = n_state.tolist()
        n_state = str(n_state)
        model.update_best_action(state, action, n_state, reward)
        score+=reward
    print('Episode:{} Score:{}'.format(episode, score))


