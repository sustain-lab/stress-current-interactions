import numpy as np


def wind_input(wind_speed, frequency, wavenumber, phase_speed, \
               sheltering_coefficient=0.11, air_density=1.2, \
               water_density=1e3, current=0, grav=9.8):
    """Wind input source function based on Jeffreys's sheltering hypothesis."""
    wind_speed_relative = wind_speed - phase_speed - current
    s_in = sheltering_coefficient * wind_speed_relative * np.abs(wind_speed_relative)
    s_in *= air_density / water_density * 2 * np.pi * frequency * wavenumber / grav
    return s_in
