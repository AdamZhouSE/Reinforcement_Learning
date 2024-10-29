from p1 import DIRECTIONS
import random
from p1 import POSSIBLE_ACTIONS

"""
Below is the content of test case 2 in problem 3.
We set the parameter values as default values in the class QValueTDLearning init method and define a grid_matrix below.
discount: 1
noise: 0.1
livingReward: -0.01
iterations: 20
grid:
    _    _    _    1
    _    #    _   -1
    S    _    _    _
"""
grid = [
    ['_', '_', '_', '1'],
    ['_', '#', '_', '-1'],
    ['S', '_', '_', '_']
]


class QValueTDLearning:
    def __init__(self, discount=1.0, noise=0.1, living_reward=-0.01, iterations=20):
        self.grid = grid
        self.discount = discount
        self.noise = noise
        self.living_reward = living_reward
        self.iterations = iterations
        self.q_values = {}
        # Exploration rate
        self.epsilon = 1.0
        self.epsilon_decay = 0.9
        self.epsilon_min = 0.01
        self.learning_rate = 0.1
        self.learning_rate_decay = 0.99
        self.alpha_min = 0.01

    def train(self):
        for i in range(self.iterations):
            state = self.get_start_position()
            done = False
            while not done:
                action = self.get_next_action(state)
                next_state = self.move(state, action)
                reward = self.get_reward(next_state)
                # init Q-values of the next state
                self.init_q_values(next_state)
                best_next_action = max(self.q_values[next_state], key=self.q_values[next_state].get)
                td_target = reward + self.discount * self.q_values[next_state][best_next_action]
                self.q_values[state][action] = ((1 - self.learning_rate) * self.q_values[state][action] +
                                                self.learning_rate * td_target)
                # reach a terminal state -> end
                if self.is_number(self.grid[next_state[0]][next_state[1]]):
                    done = True
                state = next_state
            # Decay epsilon and learning rate
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            self.learning_rate = max(self.learning_rate * self.learning_rate_decay, self.alpha_min)
            # TODO converge?
            # if all(abs(v) < 1e-1 for state in self.q_values for v in self.q_values[state].values()):
            #     print('break')
            #     break

    def get_next_action(self, state):
        """Epsilon-greedy policy."""
        # ensure Q-values of the current state are initialized
        self.init_q_values(state)
        # explore
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.get_possible_actions(state))
        # exploit
        else:
            # choose the action with the highest Q-value
            best_action = max(self.q_values[state], key=self.q_values[state].get)
            # introduce noise
            return random.choices(population=POSSIBLE_ACTIONS[best_action],
                                  weights=[1 - 2 * self.noise, self.noise, self.noise])[0]

    def get_possible_actions(self, state):
        """Return the possible actions from the current state."""
        row, col = state
        possible_actions = []
        for action in DIRECTIONS.keys():
            d_row, d_col = DIRECTIONS[action]
            new_row, new_col = row + d_row, col + d_col
            if (0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0])
                    and self.grid[new_row][new_col] != '#'):
                possible_actions.append(action)
        return possible_actions

    def move(self, state, action):
        """Move to the next state given the action."""
        row, col = state
        d_row, d_col = DIRECTIONS[action]
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]) and self.grid[new_row][new_col] != '#':
            return new_row, new_col
        return row, col

    def get_reward(self, next_state):
        """Return the reward of the next state."""
        row, col = next_state
        # if the cell is a number, which means exit, return the number as the reward
        if self.is_number(self.grid[row][col]):
            return float(self.grid[row][col])
        return self.living_reward

    def init_q_values(self, state):
        """Initialize the Q values for the given state."""
        if state not in self.q_values:
            # 0 for all the 4 actions
            self.q_values[state] = {action: 0.0 for action in DIRECTIONS.keys()}

    def get_start_position(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 'S':
                    return row, col

    def generate_policy(self):
        policy = [['_' for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == '#':
                    policy[row][col] = '#'
                elif self.is_number(self.grid[row][col]):
                    policy[row][col] = 'x'
                else:
                    policy[row][col] = max(self.q_values[(row, col)], key=self.q_values[(row, col)].get)
        return policy

    def run_multiple_times(self, times):
        """Run the training process multiple times."""
        for _ in range(times):
            # reset parameters
            self.q_values = {}
            self.epsilon = 1.0
            self.learning_rate = 0.1
            self.train()
            policy = self.generate_policy()
            self.print_policy(policy)

    def print_policy(self, policy):
        policy_print = ''
        for row in policy:
            # policy_print += '|' + '||'.join([f' {cell} ' for cell in row]) + '|\n'
            policy_print += ''.join(row)
        print(policy_print)

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    q = QValueTDLearning()
    q.run_multiple_times(10)
