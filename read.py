import matplotlib.pyplot as plt
import numpy as np
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

def unix_tai_to_iso(timestamp):
    return Time(timestamp, format='unix_tai').utc.isot

def time_formatter(t):
    return Time(t, format='unix_tai').utc.iso[:10]
    # return Time(t, format='unix_tai').utc.iso[11:16]

def get_level(exp):
    thresholds = sorted(LEVELS.keys(), reverse=True)
    for t in thresholds:
        if exp >= t:
            return LEVELS[t]
    return "没有级别"

with fits.open('learning_time.fits') as hdul:
    print(hdul.info())
    zhang_data = hdul['ZHANG'].data
    liu_data = hdul['LIU'].data

zhang_level = get_level(zhang_data['exp'].sum())
liu_level = get_level(liu_data['exp'].sum())
print("张徐蔚的级别：", zhang_level)
print("刘洋毓的级别：", liu_level)

print(liu_data)

