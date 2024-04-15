import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
from src.stee2HarmMtx import steer2HarmMtx
from src.buildSCFpyrLevs import pointOp, buildSCFpyrLevs


def rcosFn(width=None, position=None, values=None):
    # Optional args
    width = 1 if width is None else width
    position = 0 if position is None else position
    values = [0, 1] if values is None else values

    sz = 256  # arbitrary!

    X = np.pi * np.arange(-sz-1, 2) / (2*sz)
    Y = values[0] + (values[1]-values[0]) * np.cos(X)**2

    # Make sure end values are repeated, for extrapolation...
    Y[0] = Y[1]
    Y[sz+2] = Y[sz+1]

    X = position + (2*width/np.pi) * (X + np.pi/4)

    return X, Y


def buildSCFpyr(im, ht=None, order=None, twidth=None):
    # Defaults
    max_ht = int(np.floor(np.log2(min(np.shape(im)))) - 2)
    ht = max_ht if ht is None else min(ht, max_ht)
    order = 3 if order is None else min(max(order, 0), 15)
    nbands = order + 1
    twidth = 1 if twidth is None else max(twidth, 1)

    # Steering stuff
    harmonics = np.arange(0, nbands/2)*2 if nbands % 2 == 0 else np.arange(0, (nbands-1)/2)*2
    steermtx = steer2HarmMtx(harmonics, np.pi*np.arange(0, nbands)/nbands, 'even')

    # Compute ramps, etc
    dims = np.shape(im)
    ctr = np.ceil((np.array(dims)+0.5)/2)
    xramp, yramp = np.meshgrid((np.arange(1, dims[1]+1)-ctr[1])/(dims[1]/2), (np.arange(1, dims[0]+1)-ctr[0])/(dims[0]/2))
    angle = np.arctan2(yramp, xramp)
    log_rad = np.log2(np.sqrt(xramp**2 + yramp**2))
    log_rad[int(ctr[0])-1, int(ctr[1])-1] = log_rad[int(ctr[0])-1, int(ctr[1])-2]

    # Radial transition function (a raised cosine in log-frequency)
    Xrcos, Yrcos = rcosFn(twidth, (-twidth/2), [0, 1])
    Yrcos = np.sqrt(Yrcos)
    YIrcos = np.sqrt(1.0 - Yrcos**2)

    lo0mask = pointOp(log_rad, YIrcos, Xrcos[0], Xrcos[1]-Xrcos[0])
    imdft = fftshift(fft2(im))
    lo0dft = imdft * lo0mask

    pyr, pind = buildSCFpyrLevs(lo0dft, log_rad, Xrcos, Yrcos, angle, ht, nbands)

    hi0mask = pointOp(log_rad, Yrcos, Xrcos[0], Xrcos[1]-Xrcos[0])
    hi0dft = imdft * hi0mask
    hi0 = ifft2(ifftshift(hi0dft))

    pyr = np.concatenate((np.real(hi0).flatten(), pyr))
    pind = np.vstack((np.shape(hi0), pind))

    #return pyr, pind, steermtx, harmonics
    return pyr, pind
