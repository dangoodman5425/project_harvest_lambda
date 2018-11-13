import numpy as np
from scipy.spatial.distance import cdist, euclidean


def lambda_handler(event, context):
    x = np.array(event["coordinates"])
    eps = 1e-7
    y = np.mean(x, 0)
    loop = 1
    while True:
        d = cdist(x, [y])
        nonzeros = (d != 0)[:, 0]

        d_inv = 1 / d[nonzeros]
        d_invs = np.sum(d_inv)
        w = d_inv / d_invs
        t = np.sum(w * x[nonzeros], 0)

        num_zeros = len(x) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = t
        elif num_zeros == len(x):
            return {"latitude": y[0], "longitude": y[1]}
        else:
            big_r = (t - y) * d_invs
            r = np.linalg.norm(big_r)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*t + min(1, rinv)*y

        if euclidean(y, y1) < eps:
            return {"latitude": y1[0], "longitude": y1[1]}
        loop += 1
        y = y1
