import numpy as np
import pandas as pd

import matplotlib.pyplot as plt 
from matplotlib.ticker import MultipleLocator, FixedLocator, FuncFormatter
from matplotlib.dates import DayLocator, date2num, num2date

INPUT_CSV = 'input/Baguio.csv'
CMAP = plt.cm.RdBu
# LEVELS = np.arange(-1200, 1201, 400)
LEVELS = np.arange(-25, 26, 5)

# Option to remove outliers, change to False to turn off
ROBUST = True


def CustomDateLocator(d):
    ''' Custom Date Locator '''
    d = pd.Series(d)
    c = d[d.dt.day.apply(lambda x: x in [1, 10, 20])].values
    c = [date2num(_d) for _d in pd.to_datetime(c)]
    return FixedLocator(c)


def CustomDateFormatter(x, pos=None):
    ''' Custom Date Formatting '''
    x = num2date(x)
    if x.day == 1:
        label = '{}/{}'.format(x.month, x.day)
    else:
        label = x.strftime('%d')
    return label


def reject_outliers(sr, iq_range=0.5):
    ''' Implementation of IQR and MAD
    source: https://stackoverflow.com/a/39424972
    '''
    pcnt = (1 - iq_range) / 2
    qlow, median, qhigh = sr.dropna().quantile([pcnt, 0.50, 1-pcnt])
    iqr = qhigh - qlow
    return sr[ (sr - median).abs() <= iqr]


def tt_plot(df):

    # prepare the data for plotting
    X = df.columns.values
    Y = df.index.values
    Z = df.values
    x , y = np.meshgrid(X, Y)

    # plot
    fig, ax  = plt.subplots()
    cs = ax.contourf(x, y, Z, levels=LEVELS, cmap=CMAP)
    fig.colorbar(cs, ax=ax, shrink=0.4)

    # format the plot
    ax.xaxis.set_ticks_position('both')
    ax.yaxis.set_ticks_position('both')
    ax.tick_params(which='both', direction='in')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.xaxis.set_major_locator(CustomDateLocator(X))
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(CustomDateFormatter))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    fig.tight_layout()

    return (fig, ax)

# Load the date
df = pd.read_csv(INPUT_CSV)
# add a day column
df['DD'] = df.groupby(['YY', 'MM']).cumcount() + 1
# create a date column
# year is arbitrary. we just need the month and day
df['DATE'] = pd.to_datetime(dict(year=2000, month=df['MM'], day=df['DD'])) 

if ROBUST:
    df['RR'] = reject_outliers(df['RR'])

# reshape the data
df2 = df.pivot('YY', 'DATE', 'RR')

fig, ax = tt_plot(df2)

# show the plot
# plt.show()

# save the plot
plt.savefig('plot.png')
