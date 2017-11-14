import mido
import random


def main(mid):
    # TODO: how to generate midi via different instruments
    # TODO: what if velocity in midi?


    print(mid)
    for i, track in enumerate(mid.tracks):
        print("=================================================")
        print('Track', i, track.name)
        # for message in track:
        #     print(message)

    midi = mido.midifiles.MidiFile()
    track = mido.MidiTrack()

    def add(note, velocity, time):
        track.append(mido.Message('note_on', note=note,
                                  velocity=velocity,
                                  time=time))

    for i in range(10):
        note = random.randint(20, 80)
        velocity = random.randint(0, 127)
        time = random.randint(0, 1000)
        add(note, velocity, time)

    midi.tracks.append(track)
    midi.save('random_song.mid')


if __name__ == "__main__":
    mid = mido.MidiFile("data/metallica//Nothing_Else_Matters_3.mid")
    main(mid)
