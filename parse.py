def read_grid_mdp_problem_p1(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        seed = int(lines[0].strip().split(' ')[1])
        noise = float(lines[1].strip().split(' ')[1])
        living_reward = lines[2].strip().split(' ')[1]
        grid = []
        # the index of 'grid:' in lines
        grid_index = 3
        # read the grid
        for line in lines[grid_index + 1:]:
            grid_index += 1
            if line.startswith('grid:'):
                continue
            if line.startswith('policy:'):
                break
            # use filter to remove empty elements in the list
            grid.append(list(filter(None, line.strip().split(' '))))
        policy = []
        # read policy from the line after 'policy:'
        for line in lines[grid_index + 1:]:
            policy.append(list(filter(None, line.strip().split(' '))))
    problem = {'seed': seed, 'noise': noise, 'living_reward': living_reward, 'grid': grid, 'policy': policy}
    return problem


def read_grid_mdp_problem_p2(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        discount = float(lines[0].strip().split(' ')[1])
        noise = float(lines[1].strip().split(' ')[1])
        living_reward = float(lines[2].strip().split(' ')[1])
        iterations = int(lines[3].strip().split(' ')[1])
        grid = []
        # the index of 'grid:' in lines
        grid_index = 4
        # read the grid
        for line in lines[grid_index + 1:]:
            grid_index += 1
            if line.startswith('grid:'):
                continue
            if line.startswith('policy:'):
                break
            # use filter to remove empty elements in the list
            grid.append(list(filter(None, line.strip().split(' '))))
        policy = []
        # read policy from the line after 'policy:'
        for line in lines[grid_index + 1:]:
            policy.append(list(filter(None, line.strip().split(' '))))
    problem = {'discount': discount, 'noise': noise, 'living_reward': living_reward, 'iterations': iterations,
               'grid': grid, 'policy': policy}
    return problem


def read_grid_mdp_problem_p3(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        discount = float(lines[0].strip().split(' ')[1])
        noise = float(lines[1].strip().split(' ')[1])
        living_reward = float(lines[2].strip().split(' ')[1])
        iterations = int(lines[3].strip().split(' ')[1])
        grid = []
        # read the grid
        for line in lines[5:]:
            if line.startswith('grid:'):
                continue
            # use filter to remove empty elements in the list
            grid.append(list(filter(None, line.strip().split(' '))))
    problem = {'discount': discount, 'noise': noise, 'living_reward': living_reward, 'iterations': iterations,
               'grid': grid}
    return problem
