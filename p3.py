import sys, grader, parse
import copy
from p1 import POSSIBLE_ACTIONS
from p1 import move


def value_iteration(problem):
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['living_reward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = generate_init_policy(grid)
    # init the output value matrix
    value_matrix = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    return_value = ''
    for i in range(iterations):
        value_matrix = calculate_value_matrix(grid, policy, value_matrix, i, discount, living_reward, noise)
        return_value += print_value_matrix(i, value_matrix)
        if i > 0:
            return_value += print_policy(i, policy)
    return_value = return_value.rstrip('\n')
    return return_value


def calculate_value_matrix(grid, policy, value_matrix, cur_iteration, discount, living_reward, noise):
    new_value_matrix = copy.deepcopy(value_matrix)
    if cur_iteration == 0:
        for row in range(len(policy)):
            for col in range(len(policy[0])):
                if policy[row][col] == '#':
                    new_value_matrix[row][col] = ' ##### '
    else:
        for row in range(len(policy)):
            for col in range(len(policy[0])):
                if policy[row][col] == 'x':
                    new_value_matrix[row][col] = float(grid[row][col])
                elif policy[row][col] == '#':
                    continue
                else:
                    new_value_matrix[row][col] = get_max_value(cur_iteration, grid, policy, value_matrix, row, col,
                                                               discount, living_reward, noise)
    return new_value_matrix


def get_max_value(cur_iteration, grid, policy, value_matrix, row, col, discount, living_reward, noise):
    if cur_iteration == 1:
        return living_reward
    max_value = float('-inf')
    for intended_action in POSSIBLE_ACTIONS.keys():
        value = calculate_value(grid, intended_action, value_matrix, row, col, discount, living_reward, noise)
        if value > max_value:
            max_value = value
            # update the best action in policy
            policy[row][col] = intended_action
    return max_value


def calculate_value(grid, intended_action, value_matrix, row, col, discount, living_reward, noise):
    value = 0
    possible_actions = POSSIBLE_ACTIONS[intended_action]
    for action in possible_actions:
        # the pos may not change because of wall, then add the value of the current pos
        next_row, next_col = move(grid, row, col, action)
        if action == intended_action:
            value += (1 - 2 * noise) * (living_reward + discount * value_matrix[next_row][next_col])
        else:
            value += noise * (living_reward + discount * value_matrix[next_row][next_col])
    return value


def generate_init_policy(grid):
    policy = [['' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '_' or grid[row][col] == 'S':
                # init the policy with the first action
                policy[row][col] = 'N'
            elif grid[row][col] == '#':
                policy[row][col] = '#'
            else:
                # exit
                policy[row][col] = 'x'
    return policy


def print_value_matrix(cur_iteration, value_matrix):
    return_value = f"V_k={cur_iteration}\n"
    for row in value_matrix:
        return_value += '|' + '||'.join([f'{value:7.2f}' if value != " ##### " else value for value in row]) + '|\n'
    return return_value


def print_policy(cur_interation, policy):
    return_value = f"pi_k={cur_interation}\n"
    for row in policy:
        return_value += '|' + '||'.join([f' {cell} ' for cell in row]) + '|\n'
    return return_value


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
