import numpy as np
import random


def sample_pareto_random_var(x_0, gamma):
    """
    Sample one random draw from a Pareto distribution 
    with minimum value x_0 and exponent gamma.
    returns a float.
    """
    p = np.random.uniform()
    x = x_0 * (1 - p) ** (1.0 / (1 - gamma))
    return x


def dc_srgg_polar(colors, C=5.0, little_c=2.0, gamma=2.05, beta=2.5, x_0=1.0):
    """
    Make a degree-corrected soft random geometric graph 
    with the following parameters:
    colors: list of colors, one per node
    C: float, controls the maximum value of the radial coordinate of the points in space
    little_c: float, controls the probability of links forming between two edges
    gamma: the degree exponent for the Pareto distribution. >2.
    beta: the degree exponent for the connection probability. >2.
    x_0: the minimum value of a node's degree

    Returns adj, a dictionary of adjacency indicators,
    and coords, the polar coordinates of the nodes.
    """
    X = np.random.uniform(size=len(colors))
    # generate hidden variables (x_i)
    K = [sample_pareto_random_var(x_0, gamma) for c in colors]
    # generate degrees (kappa_i)

    adj = {}
    coords = {}
    for i in range(len(colors)):
        adj[colors[i]] = {}
        for j in range(i, len(colors)):
            d_i_j = np.abs(X[i] - X[j])
            # distance parameter (in hidden variables)
            p_i_j = little_c * K[i] * K[j]
            p_i_j *= (d_i_j ** beta)
            # degree correlation
            draw = np.random.uniform()
            if draw < p_i_j:
                adj[colors[i]][colors[j]] = True            
                # choosing if the edge exists
        coords[colors[i]] = (C - 3 * np.log(K[i]), 360 * X[i])
        # creating coordinates
    return adj, coords

colors = ['orange-tan', 'red', 'bright-yellow', 'royal-blue', 'turquoise', 'grey', 'lime-green', 'gold', 'brown', 'pink', 'light-tan', 'green', 'purple', 'orange']
print(dc_srgg_polar(colors, 15.0, 2.0, 2.005, 2.5, 1.0)) 
