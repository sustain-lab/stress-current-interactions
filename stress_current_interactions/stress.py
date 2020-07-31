import numpy as np

VISCOSITY_AIR = 1.56e-5
VISCOSITY_WATER = 0.9E-6
VON_KARMAN = 0.4


def drag_coefficient(ustar: float, U: float) -> float:
    """Returns the drag coefficient given input 
    friction velocity ustar and wind speed U."""
    return (ustar / U)**2


def drag_coefficient_LP1981(U10: float) -> float:
    """Returns the drag coefficient given wind speed at 10-m height
    based on Large and Pond (1981)."""
    return 1.2e-3 if U10 <= 11 else (0.49 + 0.065 * U10) * 1e-3


def friction_velocity_smooth(Uz: float, z: float, 
    viscosity_air: float=VISCOSITY_AIR, num_iterations: int=10) -> float:
    """Returns the friction velocity given input wind speed 
    and height, assuming smooth law of the wall."""
    ALPHA = 0.132
    z0 = 1e-3
    for n in range(20):
        ustar = VON_KARMAN * Uz / np.log(z / z0)
        z0 = ALPHA * viscosity_air / ustar
    return ustar


def wind_speed_at_reference_height(Uz: float, z: float, ustar: float, 
    zref: float) -> float:
    """Scales input wind speed Uz at height z to reference 
    height zref given friction velocity ustar."""
    return Uz + ustar / VON_KARMAN * np.log(zref / z)


def average_wind_speed_in_log_layer(Uz: float, z: float, ustar: float,
    zref: np.ndarray) -> np.ndarray:
    """Returns the average wind speed between the surface and zref,
    given input wind speed Uz at height z and friction velocity ustar."""
    U = wind_speed_at_reference_height(Uz, z, ustar, zref)
    return np.cumsum(U) / np.arange(1, U.size + 1, 1)


def form_drag(source_input, wavenumber_spectrum, phase_speed, wavenumber,
    water_density=1e3, grav=9.8):
    """Returns form drag as integral of the wind input function Sin
    over the wavenumber spectrum."""
    dk = np.zeros(wavenumber.shape)
    dk[1:] = np.diff(wavenumber)
    return water_density * grav * np.sum(source_input * wavenumber_spectrum * dk / phase_speed)

