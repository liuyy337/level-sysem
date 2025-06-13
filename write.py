import numpy as np
import os
from astropy.io import fits
from astropy.time import Time

K = 1
BASE_HOURS = float(3.0)
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

def init_fits():
    if not os.path.exists('learning_time.fits'):
        primary_hdu = fits.PrimaryHDU()
        primary_hdu.header['K'] = K
        primary_hdu.header['BASE_HRS'] = BASE_HOURS
        primary_hdu.header['CREATED'] = Time.now().isot
        primary_hdu.header['COMMENTS'] = "Learning time of zxw and liuyy."
        empty_history = np.array([], dtype=[
             ('date', 'S26'),
             ('hours', 'f4'),
             ('exp', 'f4')
        ])
        hdul = fits.HDUList([primary_hdu,
            fits.BinTableHDU(empty_history, name='zhang'),
            fits.BinTableHDU(empty_history, name='liu')
        ])
        hdul.writeto('learning_time.fits')

def get_level(exp):
    thresholds = sorted(LEVELS.keys(), reverse=True)
    for t in thresholds:
        if exp >= t:
            return LEVELS[t]
    return "没有级别"

def parse_input_date(date_str):
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:]
    return Time(f"{year}-{month}-{day}T23:59:59.000", format='isot').isot

def update_learning_data(name, record_date, study_hours):
    exp_gain = study_hours - BASE_HOURS
    with fits.open('learning_time.fits', mode='update') as hdul:
        user_hdu = hdul[name.upper()]
        old_data = user_hdu.data
        new_record = np.array([(record_date, study_hours, exp_gain)],
            dtype=[('date', 'S26'), ('hours', 'f4'), ('exp', 'f4')])
        updated_data = np.concatenate([old_data, new_record])
        hdul[name.upper()] = fits.BinTableHDU(updated_data, name=name.upper())
        total_exp = updated_data['exp'].sum()
        current_level = get_level(total_exp)
        hdul.flush()
    return {
        'name': name,
        'date': record_date,
        'exp_gain': exp_gain,
        'total_exp': total_exp,
        'level': current_level
        }
    
def main():
    init_fits()
    
    # input name
    while True:
        name = input("name (zhang/liu): ").lower().strip()
        if name in ['zhang', 'liu']:
            break
        print(f"当前用户没有级别:{name} (仅支持zhang/liu)")

    # input date
    while True:
        date_input = input("date (YYYYMMDD): ").strip()
        if not date_input:
            record_date = Time.now().isot
            break            
        if len(date_input) == 8 and date_input.isdigit():
            try:
                record_date = parse_input_date(date_input)
                break
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print('日期格式应为"YYYYMMDD", 例如:20240511')

    # input study hours
    try:
        hours = float(input("学习时长(hours): "))
        result = update_learning_data(name, record_date, hours)
        print(f"\n{result['name']}:")
        print(f"date: {result['date']}")
        print(f"exp gain: {result['exp_gain']:.1f}")
        print(f"total exp: {result['total_exp']:.1f}")
        print(f"当前级别: {result['level']}")
    except ValueError as e:
        print(f"Input error: {e}")

if __name__ == "__main__":
    main()
