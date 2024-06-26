import numpy as np
from tqdm import tqdm
from copy import deepcopy

from src.utils import imresize, im2single, pyrBand
from src.vmAlignAtoB import vmAlignAToB
from scipy.signal import butter, lfilter
from src.buildSCFpyr import buildSCFpyr


def vmSoundFromVideo(
        vHandle,
        nScalesin=1,
        nOrientationsin=2,
        numFramesIn=50,
        dSampleFactor=0.1,
        samplingRate=60
):
    if samplingRate < 0:
        samplingRate = vHandle.FrameRate

    ret, colorFrame = vHandle.read(0)
    if dSampleFactor != 1:
        colorFrame = imresize(colorFrame, dSampleFactor)
    fullFrame = im2single(np.mean(colorFrame, axis=2))
    refFrame = deepcopy(fullFrame)
    h, w = refFrame.shape

    nF = numFramesIn
    pyrRef, pind = buildSCFpyr(refFrame, nScalesin, nOrientationsin)

    for j in range(0, nScalesin):
        for k in range(nOrientationsin):
            bandIdx = 1 + (nOrientationsin * j) + k + 1

    totalsigs = nScalesin * nOrientationsin
    signalffs = np.zeros((nScalesin, nOrientationsin, nF))
    ampsigs = np.zeros((nScalesin, nOrientationsin, nF))
    pb = tqdm(desc="Processing", total=nF)

    for q in range(nF):
        ret, vframein = vHandle.read(q)
        if (dSampleFactor == 1):
            fullFrame = im2single(np.mean(vframein, axis=2))
        else:
            fullFrame = im2single(np.mean(imresize(vframein, dSampleFactor), axis=2))

        im = fullFrame
        pyr, _ = buildSCFpyr(im, nScalesin, nOrientationsin)
        pyrAmp = abs(pyr)
        angle = np.pi + np.angle(pyr) - np.angle(pyrRef)
        pyrDeltaPhase = (angle % (2 * np.pi)) - np.pi

        for j in range(nScalesin):
            bandIdx = 1 + j * nOrientationsin + 1
            curH = pind[bandIdx, 0]
            curW = pind[bandIdx, 1]
            for k in range(nOrientationsin):
                bandIdx = 1 + j * nOrientationsin + k + 1
                amp = pyrBand(pyrAmp, pind, bandIdx)
                phase = pyrBand(pyrDeltaPhase, pind, bandIdx)

                phasew = phase * (abs(amp) ** 2)  # * and ** must be pointwise
                sumamp = np.sum(np.abs(amp))
                ampsigs[j, k, q] = sumamp

                signalffs[j, k, q] = np.mean(phasew) / sumamp
        pb.update(1)

    sigOut = np.zeros((nF,))
    for q in range(nScalesin):
        for p in range(nOrientationsin):
            sigaligned, shiftam = vmAlignAToB(signalffs[q, p], signalffs[0, 0])
            sigOut = sigOut + sigaligned
            # shiftam

    averageNoAlignment = np.mean(np.reshape(signalffs, (nScalesin*nOrientationsin, nF)), axis=0)

    highpassfc = 0.05
    b, a = butter(3, highpassfc, 'high')
    x = lfilter(b, a, sigOut)
    x[:10] = np.mean(x)

    maxsx = np.max(x)
    minsx = np.min(x)

    if maxsx != 1 or minsx != -1:
        r = maxsx - minsx
        x = 2 * x / r
        newmx = np.max(x)
        offset = newmx - 1
        x = x - offset

    return samplingRate, sigOut, averageNoAlignment, x
