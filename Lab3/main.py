from functions import (
    data_preprocessing,
    get_init_p_k_x,
    get_p_k,
    get_prob,
    get_p_x_k,
    get_p_k_x,
    display
)
import pandas as pd
import numpy as np
import mnist


if __name__ == '__main__':

    X = mnist.train_images().reshape(60000, -1)
    y = mnist.train_labels()

    mnist_df = np.concatenate([y.reshape(-1, 1), X], axis=1)

    wanted_set = {4, 3}
    selected = np.vectorize(wanted_set.__contains__)

    df = mnist_df[selected(mnist_df[:, 0])]
    y, X = pd.DataFrame(df[:, 0]), pd.DataFrame(df[:, 1:])

    n = X.shape[0]

    X = data_preprocessing(X)

    p = np.empty((n, 2))
    p_k_x = get_init_p_k_x(n, 2)

    for i in range(5):

        p_k = get_p_k(p_k_x)
        p = get_prob(p_k_x, X)
        p_x_k = get_p_x_k(X, p)

        p_k_x = 1 - get_p_k_x(p_x_k, p_k)

    display(p)
