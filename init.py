import os
from astropy.io import fits

K = 1
BASE_HOURS = float(3.0)

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

def main():
    init_fits()

if __name__ == "__main__":
    main()
