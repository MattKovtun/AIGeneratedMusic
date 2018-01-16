import os
import mido
import random
import numpy as np


def main(folder):
    files = os.listdir(folder)
    for file in files:

        mid = mido.MidiFile(folder + "/" + file)
        print(folder + "/" + file, mid.length)


if __name__ == '__main__':
    folder = "../data/metallica"
    main(folder)
