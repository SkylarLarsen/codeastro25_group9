import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import matplotlib.pyplot as plt
from hztrak.core import get_current_parameters
from astropy.table import Table
from astropy import units as u
from astropy.constants import L_sun


def get_queried_star_from_user():
    planet_name = input("Enter exoplanet name (e.g. Kepler-22 b): ")
    df = get_current_parameters([planet_name.strip()])
    
    if len(df) == 0:
        raise ValueError(f"No data found for planet '{planet_name}'")

    row = df[0]

    queried_star = {
        'pl_name': row['pl_name'],
        'st_mass': row['st_mass'],                      # same mass
        'st_rad': row['st_rad'],                        # quantity (Rsun)
        'st_teff': row['st_teff'],                      # quantity (Kelvin)
        'st_lum': 10 ** row['st_lum'] * L_sun.unit,     # converts log(L/Lsun) → Lsun
        'st_age': row['st_age']                         # quantity (Gyr)
    }

    return queried_star

class calc:
    def alpha_beta_gamma(self, mass):
        ''' Alpha Beta Gamma Params

        Calculates the parameters alpha, beta, and gamma to be used in evolution functions
        depending on the mass of the queried star 

        Args:
            mass (int): mass of selected star for stellar evolution
        
        Returns: 
            int: alpha, beta, gamma
        '''
        if mass < 0.43 * u.Msun:
            alpha = 2.3
            beta = 0.1
            gamma = 0.05
        elif 0.43 * u.Msun <= mass < 2 * u.Msun:
            alpha = 4
            beta = 0.4
            gamma = 0.1
        elif 2.0 * u.Msun <= mass < 20.0 * u.Msun:
            alpha = 3.5
            beta = 0.7
            gamma = 0.2
        elif mass >= 20 * u.Msun:
            alpha = 1.0
            beta = 0.9
            gamma = 0.3
        else:
            raise ValueError('Invalid Mass: Not a number!!')
        
        return alpha, beta, gamma
    
    def luminosity_evolve(self, L_0, beta, t_f, t, alpha):
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
    
    def radius_evolve(self, R_0, gamma, t_f, t, alpha):
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
    
    def temp_evolve(self, T_0, L_f, L_0, R_f, R_0):
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
    
    def evolve_star(self, L_0, R_0, T_0, mass, t_f=1e10, steps=10):
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
        alpha, beta, gamma = self.alpha_beta_gamma(mass)
        times = np.linspace(0, t_f.value, steps) * t_f.unit  # times has same unit as t_f
        
        L_vals = []
        R_vals = []
        T_vals = []

        for t in times:
            L_t = self.luminosity_evolve(L_0, beta, t_f, t, alpha)
            R_t = self.radius_evolve(R_0, gamma, t_f, t, alpha)
            T_t = self.temp_evolve(T_0, L_t, L_0, R_t, R_0)

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
if __name__ == "__main__":

    model = calc()

    star = get_queried_star_from_user()

    # use 'results' for astropy table of the floats
    results = model.evolve_star(
        L_0=star['st_lum'],
        R_0=star['st_rad'],
        T_0=star['st_teff'],
        mass=star['st_mass'],
        t_f=star['st_age'] * 1e9,  # Gyr → yr
        steps=10
    )

    for row in results:
        print(f"t = {row['time_yr']/1e9:.1f} Gyr | L = {row['luminosity_Lsun']:.3f} L☉ | "
            f"R = {row['radius_Rsun']:.3f} R☉ | T = {row['temperature_K']:.1f} K")

    #print(results)  #Prints the full Astropy table nicely formatted




