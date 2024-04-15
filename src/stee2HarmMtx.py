import numpy as np


def steer2HarmMtx(harmonics, angles=None, evenorodd='even'):
    # Make HARMONICS a row vector
    harmonics = np.array(harmonics).flatten()

    numh = 2 * harmonics.size - any(harmonics == 0)

    if angles is None:
        angles = np.pi * np.arange(numh) / numh
    else:
        angles = np.array(angles).flatten()

    if isinstance(evenorodd, str):
        if evenorodd == 'even':
            evenorodd = 0
        elif evenorodd == 'odd':
            evenorodd = 1
        else:
            raise ValueError('EVEN_OR_ODD should be the string EVEN or ODD')

    # numh = 2 * len(harmonics) - (0 in harmonics)
    imtx = np.zeros((len(angles), numh))
    col = 0

    for h in harmonics:
        args = h * angles
        if h == 0:
            imtx[:, col] = np.ones(len(angles))
            col += 1
        elif evenorodd:
            imtx[:, col] = np.sin(args)
            imtx[:, col + 1] = -np.cos(args)
            col += 2
        else:
            imtx[:, col] = np.cos(args)
            imtx[:, col + 1] = np.sin(args)
            col += 2

    r = np.linalg.matrix_rank(imtx)
    if r != numh and r != len(angles):
        print('WARNING: matrix is not full rank', file=sys.stderr)

    mtx = np.linalg.pinv(imtx)

    return mtx
