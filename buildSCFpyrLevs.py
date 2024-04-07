import numpy as np
from scipy.special import factorial
from scipy.fftpack import ifft2, ifftshift
from scipy.interpolate import interp1d


def pointOp(im, lut, origin, increment):
    X = origin + increment * np.arange(0, np.size(lut))
    Y = lut.flatten()

    interp_func = interp1d(X, Y, kind='linear', fill_value='extrapolate')
    res = interp_func(im.flatten())
    res = np.reshape(res, np.shape(im))

    return res


def buildSCFpyrLevs(lodft, log_rad, Xrcos, Yrcos, angle, ht, nbands):
    if ht <= 0:
        lo0 = ifft2(ifftshift(lodft))
        pyr = np.real(lo0.flatten())
        pind = np.shape(lo0)
    else:
        bands = np.zeros((np.prod(np.shape(lodft)), nbands))
        bind = np.zeros((nbands, 2))

        Xrcos = Xrcos - np.log2(2)  # shift origin of lut by 1 octave.

        lutsize = 1024
        Xcosn = np.pi * np.arange(-(2 * lutsize + 1), lutsize + 2) / lutsize  # [-2*pi:pi]
        order = nbands - 1
        const = (2 ** (2 * order)) * (factorial(order) ** 2) / (nbands * factorial(2 * order))

        alfa = np.mod(np.pi + Xcosn, 2 * np.pi) - np.pi
        Ycosn = 2 * np.sqrt(const) * (np.cos(Xcosn) ** order) * (np.abs(alfa) < np.pi / 2)

        himask = pointOp(log_rad, Yrcos, Xrcos[0], Xrcos[1] - Xrcos[0])

        for b in range(nbands):
            anglemask = pointOp(angle, Ycosn, Xcosn[0] + np.pi * (b - 1) / nbands, Xcosn[1] - Xcosn[0])
            banddft = ((-1j) ** (nbands - 1)) * lodft * anglemask * himask
            band = ifft2(ifftshift(banddft))

            bands[:, b] = band.flatten()
            bind[b, :] = np.shape(band)

        dims = np.array(np.shape(lodft))
        ctr = np.ceil((dims + 0.5) / 2)
        lodims = np.ceil((dims - 0.5) / 2)
        loctr = np.ceil((lodims + 0.5) / 2)
        lostart = ctr - loctr + 1
        loend = lostart + lodims - 1

        log_rad = log_rad[int(lostart[0]):int(loend[0]), int(lostart[1]):int(loend[1])]
        angle = angle[int(lostart[0]):int(loend[0]), int(lostart[1]):int(loend[1])]
        lodft = lodft[int(lostart[0]):int(loend[0]), int(lostart[1]):int(loend[1])]
        YIrcos = np.abs(np.sqrt(1.0 - Yrcos ** 2))
        lomask = pointOp(log_rad, YIrcos, Xrcos[0], Xrcos[1] - Xrcos[0])

        lodft = lomask * lodft

        npyr, nind = buildSCFpyrLevs(lodft, log_rad, Xrcos, Yrcos, angle, ht - 1, nbands)

        pyr = np.concatenate((bands.flatten(), npyr))
        pind = np.vstack((bind, nind))

    return pyr, pind