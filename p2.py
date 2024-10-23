import copy
import sys, grader, parse
from p1 import POSSIBLE_ACTIONS
from p1 import move


def policy_evaluation(problem):
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['living_reward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']
    # init the output value matrix
    value_matrix = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    return_value = ''
    for i in range(iterations):
        value_matrix = calculate_value_matrix(grid, policy, value_matrix, i, discount, living_reward, noise)
        return_value += print_value_matrix(i, value_matrix)
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
                if policy[row][col] == 'exit':
                    new_value_matrix[row][col] = float(grid[row][col])
                elif policy[row][col] == '#':
                    continue
                else:
                    new_value_matrix[row][col] = calculate_value(cur_iteration, grid, policy, value_matrix, row, col,
                                                                 discount,
                                                                 living_reward,
                                                                 noise)
    return new_value_matrix


def calculate_value(cur_iteration, grid, policy, value_matrix, row, col, discount, living_reward, noise):
    if cur_iteration == 1:
        return living_reward
    value = 0
    intended_action = policy[row][col]
    possible_actions = POSSIBLE_ACTIONS[intended_action]
    for action in possible_actions:
        # the pos may not change because of wall, then add the value of the current pos
        next_row, next_col = move(grid, row, col, action)
        if action == intended_action:
            value += (1 - 2 * noise) * (living_reward + discount * value_matrix[next_row][next_col])
        else:
            value += noise * (living_reward + discount * value_matrix[next_row][next_col])
    return value


def print_value_matrix(cur_iteration, value_matrix):
    return_value = f"V^pi_k={cur_iteration}\n"
    for row in value_matrix:
        return_value += '|' + '||'.join([f'{value:7.2f}' if value != " ##### " else value for value in row]) + '|\n'
    return return_value


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)
