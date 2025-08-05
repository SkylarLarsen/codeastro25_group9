import numpy as np

def alpha_beta_gamma(mass):
    value_grid = np.array([2.3, 0.1, 0.05], [4,0.4,0.1], [3.5, 0.7, 0.2], [1.0, 0.9, 0.3])
    if mass <=0.43:
        return value_grid[0]
    elif 0.43 < mass <= 2:
        return value_grid[1]
    elif 2 < mass <= 20:
        return value_grid[2]
    elif mass > 20:
        return value_grid[3]

    