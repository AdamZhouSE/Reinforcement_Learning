import copy
import sys, grader, parse
import random
from decimal import Decimal

DIRECTIONS = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
}

POSSIBLE_ACTIONS = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}


def play_episode(problem):
    """
    :param problem: {'seed': seed, 'noise': noise, 'living_reward': living_reward, 'grid': grid, 'policy': policy}
    """
    seed = problem['seed']
    if seed != -1:
        random.seed(seed, version=1)
    noise = problem['noise']
    living_reward = problem['living_reward']
    grid = problem['grid']
    policy = problem['policy']

    reward = Decimal(0.0)
    start_pos = get_start_position(grid)
    row, col = start_pos
    intended_action = policy[row][col]
    experience = print_start_state(grid, start_pos)
    while intended_action != 'exit':
        next_action = get_next_action(intended_action, noise)
        cur_pos = move(grid, row, col, next_action)
        row, col = cur_pos
        reward = Decimal(reward) + Decimal(living_reward)
        experience += print_intermediate_state(grid, next_action, intended_action, start_pos, cur_pos, reward,
                                               living_reward)
        # update intended action after movement
        intended_action = policy[row][col]
    # print exit state
    reward = Decimal(reward) + Decimal(grid[row][col])
    experience += print_intermediate_state(grid, 'exit', intended_action, start_pos, (row, col), reward,
                                           grid[row][col])
    return experience


def get_start_position(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                return row, col


def get_next_action(intended_action, noise):
    return random.choices(population=POSSIBLE_ACTIONS[intended_action], weights=[1 - noise * 2, noise, noise])[0]


def move(grid, row, col, direction):
    d_row, d_col = DIRECTIONS[direction]
    new_row, new_col = row + d_row, col + d_col
    if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] != '#':
        return new_row, new_col
    # meet wall, stay in the same position
    return row, col


def print_start_state(grid, start_pos):
    start_state = 'Start state:\n'
    row, col = start_pos
    # deep copy the grid, so that the original grid will not be changed
    new_grid = copy.deepcopy(grid)
    new_grid[row][col] = 'P'
    for row in new_grid:
        for entity in row:
            # the number of blanks between entities
            blanks = max(4 - (len(entity) - 1), 1)
            start_state += f"{' ' * blanks}{entity}"
        start_state += '\n'
    start_state += 'Cumulative reward sum: 0.0\n'
    return start_state


def print_intermediate_state(grid, next_action, intended_action, start_pos, cur_pos, reward, received_reward):
    intermediate_state = '-------------------------------------------- \n'
    intermediate_state += f"Taking action: {next_action} (intended: {intended_action})\n"
    # use float(received_reward) so that integer reward will be shown as 1.0
    intermediate_state += f"Reward received: {float(received_reward)}\n"
    intermediate_state += 'New state:\n'

    new_grid = copy.deepcopy(grid)
    start_row, start_col = start_pos
    row, col = cur_pos
    # if the next action is exit, P will not be shown in the grid
    if next_action != 'exit':
        if start_pos == cur_pos:
            new_grid[start_row][start_col] = 'P'
        else:
            new_grid[row][col] = 'P'
    for row in new_grid:
        for entity in row:
            # the number of blanks between entities
            blanks = max(4 - (len(entity) - 1), 1)
            intermediate_state += f"{' ' * blanks}{entity}"
        intermediate_state += '\n'
    # remove redundant 0 in the float number reward e.g. 0.40 -> 0.4
    reward_str = str(reward)
    if '.' in reward_str:
        reward_str = reward_str.rstrip('0')
    # However, if there is no 0 after the decimal point, we need to add one 0. e.g. 1 -> 1.0
    intermediate_state += f"Cumulative reward sum: {float(reward_str)}"
    # no line break in the end
    if next_action != 'exit':
        intermediate_state += '\n'
    return intermediate_state


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    # test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
