import plotly.graph_objects as go
import sys

"""
Can be used by the admin to display the usage intervals in nice graphical form
"""

def time_to_double(time):
    hour = int(time.split(":")[0])
    minute = int(time.split(":")[1]) / 60
    return hour + minute

def time_diff(start, end):
    startHour = int(start[0:2])
    startMinute = int(start[3:5])
    endHour = int(end[0:2])
    endMinute = int(end[3:5])
    hourDiff = endHour - startHour
    minuteDiff = endMinute - startMinute
    if minuteDiff < 0:
        hourDiff -= 1
        minuteDiff %= 60
    return str(hourDiff)+":"+str(minuteDiff)


if len(sys.argv) != 2:
    print("Usage: python3 plot.py <usage_interval_filename>")
    sys.exit(1)

dataset = {}
with open(sys.argv[1], 'r') as data:
    line = data.readline()
    if "Sleep" in line:
        line = data.readline()
    while line:
        words = line.split(' ')
        date = words[0]
        if date not in dataset:
            dataset[date] = []
        time = words[1]
        wakeOrSleep = words[2]
        dataset[date].append([time, wakeOrSleep])
        line = data.readline()
        if not line and "Wake" in wakeOrSleep:
            del dataset[date][-1]

    for date in dataset:
        if dataset[date][0][1] == "Sleep\n":
            dataset[date].insert(0, ["00:00:00", "Wake\n"])
        if "Wake" in dataset[date][len(dataset[date])-1][1]:
            dataset[date].append(["23:59:59",  "Sleep\n"])


fig = go.Figure(
    layout = {
        'barmode': 'stack',
        'xaxis': {'automargin': True},
        'yaxis': {'automargin': False}
    }
)

for date in dataset:
    i = 0
    y = date.split('-')
    y = y[2] + "/" + y[1] + "/" + y[0]
    while i < len(dataset[date])-1:
        fig.add_bar(x=[time_to_double(time_diff(dataset[date][i][0], dataset[date][i+1][0]))],
                    y=[y],
                    base=time_to_double(dataset[date][i][0]),
                    orientation='h',
                    showlegend=False,
                    name=y)
        i += 2

fig.show()