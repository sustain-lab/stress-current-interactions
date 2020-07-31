import numpy as np


def phase_speed(frequency, wavenumber):
    """Returns the phase speed of a wave
    given input frequency and wavenumber."""
    return 2 * np.pi * frequency / wavenumber


def group_speed(frequency, wavenumber, water_depth, water_density=1e3, \
                surface_tension=0.074, grav=9.8):
    """Returns the group speed of a wave given input frequency, 
    wavenumber, and water depth."""
    cp = phase_speed(frequency, wavenumber)
    kd = wavenumber * water_depth
    sigma_k2 = surface_tension * wavenumber**2
    return cp * (0.5 + kd / np.sinh(kd) + sigma_k2 / (water_density * grav * sigma_k2))


def mean_squared_slope(wavenumber_spectrum, wavenumber, dk):
    return np.sum(wavenumber_spectrum * wavenumber**2 * dk)


def significant_wave_height(wavenumber_spectrum, dk):
    return 4 * np.sqrt(np.sum(wavenumber_spectrum * dk))


def mean_wave_period(wavenumber_spectrum, frequency):
    return np.sum(wavenumber_spectrum) / np.sum(wavenumber_spectrum * frequency)


def dominant_wave_period(wavenumber_spectrum, frequency):
    return np.sum(wavenumber_spectrum**4) / np.sum(wavenumber_spectrum**4 * frequency)
