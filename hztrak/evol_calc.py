import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import matplotlib.pyplot as plt
from hztrak.core import get_current_parameters
from astropy.table import Table
from astropy import units as u
from astropy.constants import L_sun
from core import find_hz

'''
def get_queried_star_from_user():
    planet_names = input("Enter exoplanet name (e.g. Kepler-22 b): ")

    for planet in planet_names:
        df = get_current_parameters([planet.strip()])
    
    if len(df) == 0:
        raise ValueError(f"No data found for planet '{planet_names}'")

    row = df[0]
'''

def get_queried_star_from_user():
    planet_names = input("Enter exoplanet name (e.g. Kepler-22 b): ")

    df = get_current_parameters([planet_names.strip()])
    
    if len(df) == 0:
        raise ValueError(f"No data found for planet '{planet_names}'")


    queried_star = {
        'pl_name': df.loc[0,'pl_name'],
        'st_mass': df.loc[0,'st_mass'],                      # same mass
        'st_rad': df.loc[0,'st_rad'],                        # quantity (Rsun)
        'st_teff': df.loc[0,'st_teff'],                      # quantity (Kelvin)
        'st_lum': 10 ** df.loc[0,'st_lum'],                  # converts log(L/Lsun) → Lsun
        'st_age': df.loc[0,'st_age']                         # quantity (Gyr)
    }

    return queried_star


def alpha_beta_gamma(mass):
    ''' Alpha Beta Gamma Params

    Calculates the parameters alpha, beta, and gamma to be used in evolution functions
    depending on the mass of the queried star 

    Args:
        mass (int): mass of selected star for stellar evolution
    
    Returns: 
        int: alpha, beta, gamma
    '''
    if mass < 0.43:
        alpha = 2.3
        beta = 0.1
        gamma = 0.05
    elif 0.43 <= mass < 2:
        alpha = 4
        beta = 0.4
        gamma = 0.1
    elif 2.0 <= mass < 20.0:
        alpha = 3.5
        beta = 0.7
        gamma = 0.2
    elif mass >= 20:
        alpha = 1.0
        beta = 0.9
        gamma = 0.3
    else:
        raise ValueError('Invalid Mass: Not a number!!')
    
    return alpha, beta, gamma

def luminosity_evolve(L_0, beta, t_f, t, alpha):
    ''' 
    Evolve Luminosity

    Evolves the luminosity to future time t_f

    Args:
        L_0 (int): initial luminosity
        beta (int): L evolution parameter
        t_f (int): end time user wishes to evolve to
        t (int): time variable
        alpha: mass ratio parameter
    
    Returns:
        int: final luminosity at timestep of t_f
    '''

    L_f = L_0 * (1 + beta * (t / t_f) ** alpha)
    return L_f

def radius_evolve(R_0, gamma, t_f, t, alpha):
    ''' 
    Evolve Radius

    Evolves the radius to future time t_f

    Args:
        R_0 (int): initial radius
        gamma (int): R evolution parameter
        t_f (int): end time user wishes to evolve to
        t (int): time variable
        alpha: mass ratio parameter
    
    Returns:
        int: final radius at timestep of t_f
    '''

    R_f = R_0 * (1 + gamma * (t / t_f) ** alpha)
    return R_f

def temp_evolve(T_0, L_f, L_0, R_f, R_0):
    ''' 
    Evolve Temperature

    Evolves the temperature to future time t_f

    Args:
        T_0 (int): initial temperature
        L_f (int):  final luminosity
        L_0 (int): inital luminosity
        R_f (int): final radius
        R_0 (int): initial radius
    
    Returns:
        int: final temperature at timestep of t_f
    '''
    T_f = T_0 * (L_f / L_0)**(1/4) * (R_f / R_0)**(-1/2)
    return T_f

def evolve_star(L_0, R_0, T_0, mass, t_f=1e10, steps=10):
    """
    Evolve star 

    Evolve the star's L, R, and T over time and return numpy arrays.

    Args:
        L_0 (int): inital luminosity
        R_0 (int): initial radius
        T_0 (int): initial temperature
        mass (int): mass of selected star for stellar evolution
        t_f (int): end time user wishes to evolve to
        steps (int): number of intervals in t_f

    Returns:
        arrays for time, luminosity, radius, and temp

    """
    alpha, beta, gamma = alpha_beta_gamma(mass)
    times = np.linspace(0, t_f, steps)  # times has same unit as t_f
    
    L_vals = []
    R_vals = []
    T_vals = []

    for t in times:
        L_t = luminosity_evolve(L_0, beta, t_f, t, alpha)
        R_t = radius_evolve(R_0, gamma, t_f, t, alpha)
        T_t = temp_evolve(T_0, L_t, L_0, R_t, R_0)

        L_vals.append(L_t)
        R_vals.append(R_t)
        T_vals.append(T_t)

    #return np.array(times), np.array(L_vals), np.array(R_vals), np.array(T_vals)

    # Build and return astropy table
    table = Table(
        [times, L_vals, R_vals, T_vals],
        names=('time_yr', 'luminosity_Lsun', 'radius_Rsun', 'temperature_K')
    )
    return table


# ------ USE w query -------
#if __name__ == "__main__":

#model = calc()

star = get_queried_star_from_user()

# use 'results' for astropy table of the floats
results = evolve_star(
L_0=star['st_lum'],
R_0=star['st_rad'],
T_0=star['st_teff'],
mass=star['st_mass'],
t_f=star['st_age'],
steps=10
)

for row in results:
    print(f"t = {row['time_yr']:.1f} Gyr | L = {row['luminosity_Lsun']:.3f} L☉ | "
        f"R = {row['radius_Rsun']:.3f} R☉ | T = {row['temperature_K']:.1f} K")

#print(results)  #astropy table print formatted

frames = {} #Keys are the time stamp, the values are the hz bounds

for row in results:
    t = row['time_yr']
    t_eff = row['temperature_K']
    st_lum = row['luminosity_Lsun']

    hz_found = find_hz(st_lum=st_lum, st_teff=t_eff)
    
    frames[t] = hz_found


print(frames)

#Skylar call your method here








