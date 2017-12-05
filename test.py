import mido
import random


def main(mid):
    # TODO: how to generate midi via different instruments
    # TODO: what if velocity in midi?

    midi = mido.midifiles.MidiFile()
    track = mido.MidiTrack()

    print(mid)
    for i, tr in enumerate(mid.tracks):
        print("=================================================")
        print('Track', i, tr.name)
        if tr.name == "Drums":
            midi.tracks.append(tr)

            for message in tr:
                print(message)

    def add(note, velocity, time):
        track.append(mido.Message('note_on', note=note,
                                  velocity=velocity,
                                  time=time, channel=9))

    # track.append(mido.Message('control_change', control=7, value=100,time=3073))
    # track.append(mido.Message('control_change', control=7, value=100))
    # track.append(mido.Message('program_change', program=115))
    # for i in range(100):
    #     note = random.randint(40, 80)
    #     velocity = random.randint(0, 127)
    #     time = random.randint(10, 1000)
    #     add(note, velocity, time)

    # midi.tracks.append(track)
    midi.save('random_song.mid')


if __name__ == "__main__":
    mid = mido.MidiFile("data/metallica/Enter_Sandman_3.mid")
    # mid = mido.MidiFile("random_song.mid")
    main(mid)
