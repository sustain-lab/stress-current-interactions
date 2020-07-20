import numpy as np

from .dispersion import wavenumber

def jonswap(frequency, wind_speed, fetch, grav_accel=9.8):
    """JONSWAP parametric frequency spectrum.
    Frequency is in Hz, wind_speed is in m/s, and fetch is in m."""
    BETA = -1.25
    GAMMA = 3.3

    alpha = 0.076 * nondimensional_fetch(wind_speed, fetch, grav_accel)**(-0.22)
    peak_frequency = jonswap_peak_frequency(wind_speed, fetch, grav_accel)
    sigma = 0.07 * np.ones((frequency.size))
    sigma[frequency > peak_frequency] = 0.09
    r = np.exp(-0.5 * ( (frequency - peak_frequency) / (sigma * peak_frequency))**2)
    omega = 2 * np.pi * frequency
    
    spectrum = 2 * np.pi * alpha * grav_accel**2 \
             / omega**5 * np.exp(BETA * (peak_frequency / frequency)**4) \
	     * GAMMA**r

    return spectrum


def jonswap_peak_frequency(wind_speed, fetch, grav_accel=9.8):
    a = 3.5
    b = 1 / 3
    return a * (grav_accel**2 / (wind_speed * fetch))**b 


def nondimensional_fetch(wind_speed, fetch, grav_accel=9.8):
    return grav_accel * fetch / wind_speed**2


def wavenumber_spectrum(frequency, frequency_spectrum, water_depth):
    """Returns the wavenumber specrum given input frequency spectrum."""
    k = wavenumber(frequency, water_depth)
    df, dk = np.diff(frequency), np.diff(k)
    Fk = np.zeros(frequency.shape)
    Fk[1:] = frequency_spectrum[1:] * df / dk
    return Fk
    
