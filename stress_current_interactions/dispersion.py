import numpy as np


def wavenumber(frequency, water_depth, grav=9.8, surface_tension=0.074, \
               water_density=1e3, num_iterations=100):
    """Solves the dispersion relationship for wavenumber
    using a Newton-Raphson iteration method."""
    frequency_nondim = 2 * np.pi * np.sqrt(water_depth / grav) * frequency
    k = frequency_nondim**2
    surface_tension_nondim = surface_tension / (grav * water_density * water_depth**2)
    count = 0
    while count < num_iterations:
        t = np.tanh(k)
        dk = - (frequency_nondim**2 - k * t * (1 + surface_tension_nondim * k**2)) \
           / (3 * surface_tension_nondim * k**2 * t + t + k * (1 + surface_tension_nondim * k**2) * (1 - t**2))
        k -= dk
        count += 1
    return k / water_depth

