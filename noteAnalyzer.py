import mido
import matplotlib.pyplot as plt


def main(mid):
    dct = {}  # {note: [(time, 0/1), ...]}
    graph = {}  # { (note_on, note, time): {(next_note_, next_note, next_note_time): weight}}

    graph_time_line = 0
    time_line = 0
    for i, tr in enumerate(mid.tracks):
        print("=================================================")
        print('Track', i, tr.name)
        for message in tr:
            # print(message)
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



        # print(dct[42])
    x, y = zip(*dct[41])
    plt.plot(x, y)
    # plt.plot(dct[42][1:], [x[1] for x in dct[42][300:400]])
    plt.show()


if __name__ == '__main__':
    mid = mido.MidiFile("random_song.mid")
    main(mid)
