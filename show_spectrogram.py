import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import argparse


def spectogram(audio_path):
    # Load the .wav file
    y, sr = librosa.load(audio_path)

    # Compute the STFT
    D = librosa.stft(y)

    # Convert the STFT into a spectrogram
    spectrogram = librosa.amplitude_to_db(abs(D), ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spectrogram")
    parser.add_argument(
        "--audio_path",
        type=str,
        help="Path to input audio file"
    )
    args = parser.parse_args()
    spectogram(args.audio_path)
