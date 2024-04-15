import numpy as np
import cv2 as cv
from scipy.io.wavfile import write


def imresize(img, drate):
    new_shape = [int(drate * x) for x in img.shape[:2]]
    new_img = cv.resize(img, new_shape, interpolation=cv.INTER_LINEAR)
    return new_img


def im2single(img):
    new_img = img / 255
    new_img = new_img.astype(np.float32)
    return new_img


def pyrBandIndices(pind, band):
    if band > pind.shape[0] or band < 1:
        raise ValueError(f'BAND_NUM must be between 1 and number of pyramid bands ({pind.shape[0]}).')

    if pind.shape[1] != 2:
        raise ValueError('INDICES must be an Nx2 matrix indicating the size of the pyramid subbands')

    ind = 1
    for l in range(band - 1):
        ind += np.prod(pind[l, :])

    indices = np.arange(ind, ind + np.prod(pind[band - 1, :]), dtype=np.int64)

    return indices


def pyrBand(pyr, pind, band):
    indices = pyrBandIndices(pind, band)
    res = pyr[indices]
    res = res.reshape(int(pind[band - 1, 0]), int(pind[band - 1, 1]))
    return res


def vmSaveSound(x, samplingRate, save_path, gain=None):
    # VMPLAYSOUND saves the sound x, multiplied by gain
    # Normalize to 16-bit range
    y = np.int16(x / np.max(np.abs(x)) * 32767)

    if gain is not None:
        y = y * gain

    # Write to a temporary file
    write(save_path, samplingRate, y)


def getNumFrames(cap):
    numFrames = 0
    while True:
        ret, vframein = cap.read()
        if not ret:
            break
        numFrames += 1
    return numFrames - 1
