import numpy as np
from scipy.signal import convolve


def vmAlignAToB(Ax, Bx):
    # Aligns A to B, optionally returns offset
    acorb = convolve(Ax, Bx[::-1])
    maxval = np.max(acorb)
    maxind = np.argmax(acorb)
    shiftam = np.size(Bx, 0) - maxind
    AXout = np.roll(Ax, shiftam)
    return AXout, shiftam
