import numpy as np
from sklearn.neural_network import BernoulliRBM
from midiextractor import midiToNoteStateMatrix, noteStateMatrixToMidi
import os

timestamp = 20  # 15
default_bound = 156
number_of_songs_generated = 1


def create_batch_from_folder(folder, song=False):
    batch = []

    if song:
        statematrix = midiToNoteStateMatrix(folder)
        for i in range(statematrix.shape[0] // timestamp):
            batch.append(statematrix[i: i + timestamp].flatten())
        return np.asarray(batch)

    files = os.listdir(folder)

    for file in files[:10]:
        statematrix = midiToNoteStateMatrix(folder + "/" + file)
        print(file, statematrix.shape)

        for i in range(statematrix.shape[0] / timestamp):
            batch.append(statematrix[i: i + timestamp].flatten())
    return np.asarray(batch)


def train_RBM(statematrix):
    print("Matrix for RBM shape", statematrix.shape)
    model = BernoulliRBM(n_components=1000)
    model.fit(statematrix)

    generated_images = np.random.randint(2, size=(number_of_songs_generated, timestamp * default_bound))
    for i in range(1000):  # 100
        generated_images = model.gibbs(generated_images)

    generated_images = generated_images.astype(int)

    generated_images = np.reshape(generated_images, (number_of_songs_generated, timestamp, default_bound))
    print(generated_images.shape)

    noteStateMatrixToMidi(generated_images[0])


if __name__ == "__main__":
    song = True
    statematrix = create_batch_from_folder("MetallicaEnterSandmanDrums.mid", song)
        # statematrix = create_batch_from_folder("../data/metallica")
    train_RBM(statematrix)
