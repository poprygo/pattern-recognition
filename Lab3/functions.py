import numpy as np
import matplotlib.pyplot as plt


def get_init_p_k_x(ds_size, clusters_amount):
    rand_matrix = np.random.randint(low=0, high=5000,
                                    size=(ds_size, clusters_amount))

    sum_along_row = np.repeat(rand_matrix.sum(axis=1).reshape((-1, 1)),
                              repeats=2, axis=1)

    prob_matrix = rand_matrix / sum_along_row
    return prob_matrix


def get_p_x_k(x, p):

    p = np.expand_dims(p, axis=0)
    p = np.repeat(p, repeats=x.shape[0], axis=0)
    p = p.reshape((p.shape[0], p.shape[1], -1))

    x = np.expand_dims(x, axis=1)
    x = np.repeat(x, repeats=2, axis=1)
    x = x.reshape((x.shape[0], x.shape[1], -1))

    a = np.power(p, x).prod(axis=-1)
    b = np.power(1 - p, (1 - x)).prod(axis=-1)

    return np.multiply(a, b)


def get_p_k(histo):
    """
    >>> get_p_k( np.asarray( [[0.3, 0.7],[0.45, 0.55]] ) )
    array([0.375, 0.625])
    >>> get_p_k( np.asarray( [[0.0, 1],[0.5, 0.5]] ) )
    array([0.25, 0.75])
    """
    p = histo.mean(axis=0)
    return p


def get_p_k_x(conds, apr):
    """
      >>> get_p_k_x(np.asarray( [[0.2, 0.8],[0.5, 0.5]] ), np.asarray([0.25, 0.75]))
      array([[0.07692308, 0.92307692],
             [0.25      , 0.75      ]])
      >>> get_p_k_x(np.asarray( [[0.5, 0.5],[0, 1]] ), np.asarray([0.5, 0.5]))
      array([[0.5, 0.5],
             [0. , 1. ]])
  """
    temp = conds[:, 0] * apr[0] + conds[:, 1] * apr[1]
    aps_a = (conds[:, 0] * apr[0]) / temp
    aps_b = (conds[:, 1] * apr[1]) / temp
    return np.stack((aps_a, aps_b), axis=1)


def get_prob(apr_probs, X_):

    n = X_.shape[0]
    p = np.empty((2, 28, 28))
    for i in range(0, 28):
        for j in range(0, 28):
            a1, a2, b1, b2 = 0, 0, 0, 0

            for z in range(0, n):
                a1 = a1 + X_[z, i, j] * apr_probs[z, 0]
                a2 = a2 + apr_probs[z, 0]
                b1 = b1 + X_[z, i, j] * apr_probs[z, 1]
                b2 = b2 + apr_probs[z, 1]
            p[0, i, j] = a1 / a2
            p[1, i, j] = b1 / b2
    return p


def data_preprocessing(X_):

    n = X_.shape[0]
    data = np.zeros((n, 28, 28))
    for i in range(0, n):
        temp = np.reshape(X_[i:i + 1].to_numpy(), (-1, 28))
        temp = (temp > 127).astype(np.uint8)
        data[i] = temp
    return data


def display(p_x_k):
    for i in range(p_x_k.shape[0]):
        image = p_x_k[i].reshape((28, 28))
        plt.imshow(image, cmap='gray')
        plt.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
