import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import os
from astropy.io import fits
from astropy.time import Time
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

LEVELS = {
    0:      "科员",
    10:     "副科",
    20:     "正科",
    40:     "副处",
    60:     "正处",
    90:     "副厅",
    120:    "正厅",
    160:    "副部",
    200:    "正部",
    250:    "副国",
    300:    "正国",
}

def isot_to_unix_tai(isot_str):
    return Time(isot_str, format='isot').unix_tai

def time_formatter(timestamp, pos):
    return Time(timestamp + 1749254437.0, format='unix_tai').utc.isot[:10]

def get_level(exp):
    thresholds = sorted(LEVELS.keys(), reverse=True)
    for t in thresholds:
        if exp >= t:
            return LEVELS[t]
    return "没有级别"

def plot_config(ax):
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Study Time (hours)")
    ax.set_title("Statistics of study time in Office 421")
    ax.xaxis.set_major_locator(MultipleLocator(86400))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_major_formatter(FuncFormatter(time_formatter))
    ax.legend()

with fits.open('learning_time.fits') as hdul:
    # print(hdul.info())
    zhang_data = hdul['ZHANG'].data
    liu_data = hdul['LIU'].data

zhang_time = np.array([isot_to_unix_tai(date) for date in zhang_data['date']])
zhang_time = zhang_time - zhang_time[0]
zhang_hours = zhang_data['hours']
zhang_level = get_level(zhang_data['exp'].sum())
liu_time = np.array([isot_to_unix_tai(date) for date in liu_data['date']])
liu_time = liu_time - liu_time[0]
liu_hours = liu_data['hours']
liu_level = get_level(liu_data['exp'].sum())

fig = plt.figure(figsize=(10, 6))
plt.rcParams['font.family'] = 'WenQuanYi Micro Hei'
ax = fig.add_subplot(111)

ax.plot(zhang_time, zhang_hours, color='blue', ls='-', lw='1', label=f'zhang({zhang_level}门)')
ax.plot(liu_time, liu_hours, color='red', ls='-', lw='1', label=f'liu({liu_level})')
ax.set_xlim(left=0, right=liu_time.max() + 1)
ax.set_ylim(-0.5, 10)
plot_config(ax)

plt.savefig("learning_curve.pdf", bbox_inches='tight')
