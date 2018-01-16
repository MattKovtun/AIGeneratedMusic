import mido
import matplotlib.pyplot as plt
import random
import numpy as np


def greedy_get_note(note, graph):
    mx = -1
    epsilon = .85
    next_note = -1
    for key in graph[note]:
        if mx < graph[note][key]:
            mx = graph[note][key]
            next_note = key

    if np.random.uniform(0, 1) > epsilon:

        a = set(graph[note].keys())
        if len(a) == 1:
            return next_note
        a.remove(next_note)
        next_note = random.sample(a, 1)[0]

        print("swapping")
    return next_note


def smart_note_pick(note,graph):
    pos_next_notes = list(graph[note].keys())
    note_ps = np.asarray([graph[note][i] for i in pos_next_notes])
    note_ps_normed = note_ps / np.sum(note_ps)
    # print(note_ps_normed)
    # print(",,", np.random.choice(len(pos_next_notes), note_ps_normed))
    return pos_next_notes[int(np.random.choice(len(pos_next_notes), p=note_ps_normed))]


    # print("====")
    # print(pos_next_notes)
    # print(pos_next_notes)
    # print(note_ps)




def main(mid):
    # TODO: write in classes
    # TODO: separate methods
    dct = {}  # {note: [(time, 0/1), ...]}
    graph = {}  # { (note_on, note, time): {(next_note_, next_note, next_note_time): weight}}

    time_line = 0
    for i, tr in enumerate(mid.tracks):
        print("=================================================")
        print('Track', i, tr.name)
        for message in tr:
            attrs = vars(message)
            if 'time' in attrs:
                time_line += attrs['time']
            else:
                continue
            if 'note' in attrs:
                dct[attrs['note']] = dct.get(attrs['note'], []) + [(time_line, 0 if attrs['type'] == 'note_off' else 1)]

        for i in range(len(tr) - 1):
            cur_node = vars(tr[i])
            next_node = vars(tr[i + 1])

            if not (cur_node['type'].startswith('note') and next_node['type'].startswith('note')):
                continue

            # cur_node_data = (0 if cur_node['type'] == 'note_off' else 1, cur_node['note'], cur_node['time'])
            # next_node_data = (0 if next_node['type'] == 'note_off' else 1, next_node['note'], next_node['time'])
            cur_node_data = tuple((k, cur_node[k]) for k in sorted(cur_node.keys()))
            next_node_data = tuple((k, next_node[k]) for k in sorted(next_node.keys()))
            if cur_node_data in graph:
                if next_node_data in graph[cur_node_data]:
                    graph[cur_node_data][next_node_data] += 1
                else:
                    graph[cur_node_data][next_node_data] = 1
            else:
                graph[cur_node_data] = {next_node_data: 1}
        print(graph)
        print(len(graph.keys()))
        starting_note = random.choice(list(graph.keys()))
        # print(starting_note)
        # next_note = greedy_get_note(starting_note, graph)
        # print(graph[starting_note][next_note])

        midi = mido.midifiles.MidiFile()
        track = mido.MidiTrack()

        for n in range(150):
            # print(starting_note)
            # print(smart_note_pick(starting_note, graph))
            track.append(
                mido.Message(channel=starting_note[0][1], note=starting_note[1][1], time=starting_note[2][1],
                             type=starting_note[3][1], velocity=starting_note[4][1]))

            starting_note = greedy_get_note(starting_note, graph)
            # starting_note = smart_note_pick(starting_note, graph)
        midi.tracks.append(track)

        midi.save('generated_song_3.mid')

        # print(dct[42])
        # x, y = zip(*dct[41])
        # plt.plot(x, y)
        # # plt.plot(dct[42][1:], [x[1] for x in dct[42][300:400]])
        # plt.show()


if __name__ == '__main__':
    mid = mido.MidiFile("MetallicaEnterSandmanDrums.mid")
    main(mid)
