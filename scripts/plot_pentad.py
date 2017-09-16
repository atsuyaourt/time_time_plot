import numpy as np
import pandas as pd

import matplotlib.pyplot as plt 
from matplotlib.ticker import MultipleLocator

INPUT_CSV = 'input/Baguio_pentad.csv'
OUT_DIR = 'img/'
CMAP = plt.get_cmap('winter') # see https://matplotlib.org/examples/color/colormaps_reference.html
LEVELS = np.linspace(40, 280, 7)


def plot_format(ax):
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(which='both', direction='in')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))


def tt_plot(df, **kwargs):
    # reshape the data
    _df = df.pivot(df.columns[0], df.columns[1], df.columns[2])

    # prepare the data for plotting
    X = _df.columns.values
    Y = _df.index.values
    Z = _df.values
    x , y = np.meshgrid(X, Y)

    # plot
    fig, ax  = plt.subplots()
    cs = ax.contourf(x, y, Z, **kwargs)
    fig.colorbar(cs, ax=ax, shrink=0.4)

    # format the plot
    plot_format(ax)

    return (fig, ax)

# Load the date
df = pd.read_csv(INPUT_CSV)

### Example 1: Plot the whole data ###
plot_opts = {
    'levels': LEVELS,
    'cmap': CMAP
}
fig, ax = tt_plot(df, **plot_opts)
ax.set_xlabel('Pentad')
fig.tight_layout()
# save the plot
plt.savefig(OUT_DIR + 'plot_pentad.png')

### Example 2: Plot a portion of the data using 'xlim' ###
plot_opts = {
    'levels': LEVELS,
    'cmap': CMAP
}
fig, ax = tt_plot(df, **plot_opts)
ax.set_xlabel('Pentad')
ax.set_xlim(25, 65)
fig.tight_layout()
# save the plot
plt.savefig(OUT_DIR + 'plot_pentad_clipped.png')
