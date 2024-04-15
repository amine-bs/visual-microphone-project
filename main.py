from src.vmSoundFromVideo import vmSoundFromVideo
from src.utils import vmSaveSound, getNumFrames
import argparse
import cv2 as cv
import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual Microphone")
    parser.add_argument(
        "--video_path",
        type=str,
        help="Path to input video file"
    )
    parser.add_argument(
        "--out_path",
        type=str,
        default="output.wav",
        help="Path where output audio will be saved"
    )
    parser.add_argument(
        "--frame_rate",
        type=int,
        default=60,
        help="Frame rate on input video"
    )
    args = parser.parse_args()
    print(f"Reading video: {args.video_path}")
    cap = cv.VideoCapture(args.video_path)
    numFrames = getNumFrames(cap)
    cap = cv.VideoCapture(args.video_path)
    samplingRate, _, _, audio = vmSoundFromVideo(cap, numFramesIn=numFrames, samplingRate=args.frame_rate)
    print(f"Writing audio in: {args.out_path}")
    vmSaveSound(audio, samplingRate, args.out_path)
