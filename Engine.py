import gym
import gym_chess
import random

env = gym.make('Chess-v0')
print(env.render())
gym_chess.Chess
env.reset()
done = False

while not done:
    action = random.choice(env.legal_moves)
    env.step(action)
    print(env.render(mode='unicode'))

env.close()
