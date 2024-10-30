from p1 import DIRECTIONS
import random
from p1 import POSSIBLE_ACTIONS
import copy
from p3 import calculate_value_matrix, generate_init_policy
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
        # exploration rate
        # controls the agent’s tendency to explore the environment rather than exploit its current knowledge
        # 1.0 means the agent will start by exploring entirely, taking random actions
        self.epsilon = 1.0
        # how quickly the epsilon decreases over time.
        self.epsilon_decay = 0.99
        self.epsilon_min = 0.01
        # control the rate at which Q-values are updated based on new information
        self.learning_rate = 0.1
        self.learning_rate_decay = 0.99
        self.alpha_min = 0.01
        # the maximum difference between the sum of values and the optimal sum of values
        self.max_difference = 1

    def train(self):
        """train the agent using Q-learning."""
        while True:
            state = self.get_start_position()
            done = False
            while not done:
                action = self.get_next_action(state)
                next_state = self.move(state, action)
                reward = self.get_reward(next_state)
                # init Q-values of the next state
                self.init_q_values(next_state)
                # choose the action with the highest Q-value e.g. {'state': {'N': 1.0, 'S': 2.0, 'E': 3.0, 'W': 4.0}}
                best_next_action = max(self.q_values[next_state], key=self.q_values[next_state].get)
                # calculate temporal difference learning sample
                td_target = reward + self.discount * self.q_values[next_state][best_next_action]
                # update Q-value of the current state
                self.q_values[state][action] = ((1 - self.learning_rate) * self.q_values[state][action] +
                                                self.learning_rate * td_target)
                # reach a terminal state -> stop
                if self.is_number(self.grid[next_state[0]][next_state[1]]):
                    done = True
                state = next_state
            # Decay epsilon and learning rate
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            self.learning_rate = self.learning_rate * self.learning_rate_decay
            # stop the search when the learning rate decays small enough
            if self.learning_rate < self.alpha_min:
                break

    def get_next_action(self, state):
        """use epsilon-greedy to explore"""
        # ensure Q-values of the current state are initialized
        self.init_q_values(state)
        # explore four directions randomly
        if random.uniform(0, 1) < self.epsilon:
            best_action = random.choice(list(DIRECTIONS.keys()))
        # exploit
        else:
            # choose the action with the highest Q-value
            best_action = max(self.q_values[state], key=self.q_values[state].get)
            # introduce noise
        return random.choices(population=POSSIBLE_ACTIONS[best_action],
                              weights=[1 - 2 * self.noise, self.noise, self.noise])[0]

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
        """generate the policy based on the Q-values."""
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
        cnt = 0
        for _ in range(times):
            # reset parameters
            self.q_values = {}
            self.epsilon = 1.0
            self.learning_rate = 0.1
            self.train()
            policy = self.generate_policy()
            # count the number of times the policy is optimal
            if self.validate_optimal_policy(policy):
                cnt += 1
            self.print_policy(policy)
        print('Optimal rate', cnt/times)

    def validate_optimal_policy(self, policy):
        """validate the policy generated from q-values is optimal or not."""
        value_matrix = self.policy_iteration(policy)
        value_matrix_optimal = self.value_iteration()
        sum_value = sum(sum(value for value in row if self.is_number(value)) for row in value_matrix)
        sum_value_optimal = sum(sum(value for value in row if self.is_number(value)) for row in value_matrix_optimal)
        print('sum difference', abs(sum_value - sum_value_optimal))
        if abs(sum_value - sum_value_optimal) > self.max_difference:
            return False
        return True

    def policy_iteration(self, policy):
        value_matrix = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        for i in range(self.iterations):
            value_matrix = self.calculate_value_matrix(i, policy, value_matrix)
        return value_matrix

    def calculate_value_matrix(self, cur_iteration, policy, value_matrix):
        new_value_matrix = copy.deepcopy(value_matrix)
        for row in range(len(policy)):
            for col in range(len(policy[0])):
                if policy[row][col] == 'x':
                    new_value_matrix[row][col] = float(self.grid[row][col])
                elif policy[row][col] == '#':
                    new_value_matrix[row][col] = '#'
                else:
                    new_value_matrix[row][col] = self.calculate_value(cur_iteration, policy[row][col],
                                                                      value_matrix, row, col)
        return new_value_matrix

    def calculate_value(self, cur_iteration, intended_action, value_matrix, row, col):
        if cur_iteration == 1:
            return self.living_reward
        value = 0
        possible_actions = POSSIBLE_ACTIONS[intended_action]
        for action in possible_actions:
            # the pos may not change because of wall, then add the value of the current pos
            next_row, next_col = self.move((row, col), action)
            if action == intended_action:
                value += (1 - 2 * self.noise) * (self.living_reward + self.discount * value_matrix[next_row][next_col])
            else:
                value += self.noise * (self.living_reward + self.discount * value_matrix[next_row][next_col])
        return value

    def value_iteration(self):
        policy = generate_init_policy(self.grid)
        # init the output value matrix
        value_matrix = [[0 for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        for i in range(self.iterations):
            value_matrix = calculate_value_matrix(self.grid, policy, value_matrix, i, self.discount,
                                                  self.living_reward, self.noise)
        print(policy)
        return value_matrix

    def print_policy(self, policy):
        policy_print = ''
        for row in policy:
            policy_print += '|' + '||'.join([f' {cell} ' for cell in row]) + '|\n'
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
