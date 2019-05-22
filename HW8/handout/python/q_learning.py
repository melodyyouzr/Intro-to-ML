from environment import MountainCar
import numpy as np
from numpy import random
import sys
import matplotlib.pyplot as plt


def QValue(a, weight, bias, state):
    suml = 0
    column = weight[:, a]
    for k, v in state.items():
        suml += column[k] * v
    suml += bias
    return suml


# In[221]:


def epsilon_find(e, weight, bias, state):
    qvalue = []
    if random.random() < e:
        a = random.choice(action)
    else:
        for i in range(3):
            v = QValue(i, weight, bias, state)
            qvalue.append(v)
        a = qvalue.index(max(qvalue))
    return a


# In[222]:


def update(e, learning_rate, gamma, weight, episode, max_iteration, bias):
    total_returns = []
    list = [0] * 25
    ave = []
    for i in range(episode):
        state = car.transform(car.state)
        total_r = 0
        step_count = 0
        done = False
        while (done == False):
            a = epsilon_find(e, weight, bias, state)

            next_state, reward, done = car.step(a)

            curr_q = QValue(a, weight, bias, state)

            total_r += reward

            qvalue = []
            for i in action:
                v = QValue(i, weight, bias, next_state)
                qvalue.append(v)
            max_q = max(qvalue)

            constant = learning_rate * (curr_q - (reward + gamma * max_q))

            for k, v in state.items():
                weight[k][a] = weight[k][a] - constant * v

            bias = bias - constant

            state = next_state

            step_count += 1
            if step_count == max_iteration:
                break

        total_returns.append(total_r)
        list.pop(0)
        list.append(total_r)
        k = sum(list) / 25
        ave.append(k)
        car.reset()

    return weight, bias, total_returns, ave


# In[223]:


if __name__ == "__main__":
    car = MountainCar(sys.argv[1])
    weight_out = sys.argv[2]
    returns_out = sys.argv[3]
    episode = int(sys.argv[4])
    max_iteration = int(sys.argv[5])
    epsilon = float(sys.argv[6])
    gamma = float(sys.argv[7])
    learning_rate = float(sys.argv[8])

    init_weight = np.zeros([car.state_space, 3], dtype=float)
    init_bias = 0
    action = [0, 1, 2]
    w, b, r, a = update(epsilon, learning_rate, gamma, init_weight, episode, max_iteration, init_bias)

    write_w = ""
    for i in range(len(w)):
        for j in range(len(w[i])):
            write_w += str(w[i][j]) + '\n'

    weight_file = open(weight_out, 'w')
    weight_file.write(str(b) + '\n')
    weight_file.write(write_w)

    write_r = ""
    for i in range(len(r)):
        write_r += str(r[i]) + '\n'

    reward_file = open(returns_out, 'w')
    reward_file.write(write_r)

    axis_x = np.linspace(1, 400, 400)
    plt.title("Total Rewards and rolling mean of Tile Features")  # give plot a title
    plt.xlabel("Episodes")  # make axis labels
    plt.ylabel("Rewards")

    plt.plot(axis_x, r, color='blue', label='total rewards per episode')
    plt.plot(axis_x, a, color='red', label='rolling mean')
    plt.legend()
    plt.savefig("Q2.png")
    plt.show()



