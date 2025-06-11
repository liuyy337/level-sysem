from astropy.io import fits

hdul = fits.open('learning_time.fits', mode='update')

with fits.open('learning_time.fits', mode='update'):
    liu_data = hdul['LIU'].data
    new_data = liu_data[:-1]
    hdul['LIU'].data = new_data
    hdul.flush()

