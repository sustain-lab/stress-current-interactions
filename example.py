import numpy as np
from stress_current_interactions.diagnostics import phase_speed, form_drag
from stress_current_interactions.dispersion import wavenumber
from stress_current_interactions.source_functions import wind_input
from stress_current_interactions.spectral_shapes import jonswap

wind_speed = 10
fetch = 1e4
water_depth = 1e3
rhow = 1e3
grav_accel = 9.8

def stress_distribution(wind_speed, fetch, current):
    f = np.logspace(-1, 1, 100)
    k = wavenumber(f, water_depth)
    dk = np.zeros(k.shape)
    dk[1:] = np.diff(k)
    F = jonswap(f, wind_speed, fetch)
    Fk = wavenumber_spectrum(f, F, water_depth)
    Cp = phase_speed(f, k) 
    Sin = wind_input(wind_speed, f, k, Cp, current=current)
    return rhow * grav_accel * Sin / Cp * Fk


f = np.logspace(-1, 1, 100)
k = wavenumber(f, water_depth)
dk = np.zeros(k.shape)
dk[1:] = np.diff(k)

tau = stress_distribution(wind_speed, fetch, 0)
