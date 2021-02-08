import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

df = pd.read_csv('Data/BL_W01.csv', index_col='date',
                 parse_dates=['date'])
df.tail()

df = df.loc['29/01/21':'5/02/21']
colors = plt.cm.Dark2(range(6))  # Colors of the bars

HOffset = 3.5  # Height offset from the top. Visible after 3

def init():
    ax.clear()
    nice_axes(ax)
    ax.set_ylim(.3, 6.8)

def nice_axes(ax):
    ax.set_frame_on(True)  # If the grid background is visible or not
    ax.set_facecolor('0.8')  # Grid background, 0 being black, 1 being white
    ax.tick_params(labelsize=12, length=5)  # Labelsize is how big the text is, length the line before it
    ax.grid(True, axis='x', color=(0, 0, 0, 1))  # The grid lines, R, G, B, A only works with 1 or 0
    ax.set_axisbelow(True)  # Small lines at the bottom of the X axis
    [spine.set_visible(False) for spine in ax.spines.values()]

def update(i):
    for bar in ax.containers:
        bar.remove()  # Cleans the canvas of the previous frame
    y = df_rank_expanded.iloc[i] - HOffset  # Height offset for the bars
    width = df_expanded.iloc[i]  # Width offset?
    ax.barh(y=y, width=width, color=colors, tick_label=labels, )  # Args given with the rendering of the canvas
    #date_str = df_expanded.index[i].strftime('%B %-d, %Y')
    #ax.set_title(f'Tijds data - {date_str}', fontsize='smaller')

def prepare_data(df, steps=50):
    df = df.reset_index()  # Cleans up the CSV sheet while prepping it
    df.index = df.index * steps  # Is where the steps are added
    last_idx = df.index[-1] + 1
    df_expanded = df.reindex(range(last_idx))

    df_expanded['date'] = df_expanded['date'].fillna(method='ffill')
    df_expanded = df_expanded.set_index('date')
    df_rank_expanded = df_expanded.rank(axis=1, method='first')  # Keep Axis on 1, Method sorts on who has the highest numbers
    df_expanded = df_expanded.interpolate()  # Interpolates the steps between the original data sheet
    df_rank_expanded = df_rank_expanded.interpolate()  # Interpolates the ranking and the bar position
    print(df_expanded)
    print(df_rank_expanded)
    return df_expanded, df_rank_expanded


df_expanded, df_rank_expanded = prepare_data(df)
df_expanded.head()
df_rank_expanded.head()
labels = df_expanded.columns

# Figsize dictates the size of the image / video. 13.3333 x 7.5 is 1920x1080, DPI is picture quality. Let it stay on 144
fig = plt.Figure(figsize=(13.3333, 7.5), dpi=144)
fig.patch.set_visible(0)  # Transparency for the whole background
print(fig)
ax = fig.add_subplot()
anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(df_expanded),
                     interval=100, repeat=False, blit=True)

anim.save(filename="Test.gif", writer="ffmpeg", fps=50, metadata=dict(artist="me"), bitrate=5800)

#anim.save('test.mp4', writer="ffmpeg")

#Note to self, issue found, it originates from: 30, 31 :)

#ax_array[0].set_title('Test1')
#ax_array[-1].set_title('Test2')


