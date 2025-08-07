#Authors:
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astropy import units as u
from astropy.units import Quantity, UnitTypeError
from astropy.constants import R_earth, M_earth, R_sun, M_sun, G

import pandas as pd
import matplotlib.axes
from astropy.table import Table, vstack
import matplotlib.pyplot as plt
 


def get_current_parameters(planet_name=['Kepler-22 b']):
    """Returns a dataframe of planet and host star parameters. Parameters include planet name, host star name, planet radius [Rearth], 
    planet mass [Mearth], ratio of planet to stellar radius, stellar effective temperature [K],
   stellar radius [Rsun], stellar mass [Msun],stellar luminosity [log10(Solar)], stellar age [Gyr], orbital period [days],
   and orbit semi-major axis [AU].

   Args:
        name_planet (list): list of planet names in nasa exoplanet archive
    Returns:
        Astropy Table: Planet names and parameters for the planet and host star
    Raises:
        UnitTypeError: Raised when quantity requires conversion, but conversion cannot be completed

    
    """
    table_list=[]
    for i in range(len(planet_name)):
        tab = NasaExoplanetArchive.query_criteria(table="pscomppars", where=f"pl_name='{planet_name[i]}'")
        sub_tab=tab['pl_name','hostname','pl_rade','pl_bmasse','pl_ratror','st_teff','st_rad','st_mass','st_lum','st_age','pl_orbper','pl_orbsmax']
        if len(sub_tab)==0:
            print(f'{planet_name[i]} not found! Try again bestie :/')
            continue
        else:
            table_list.append(sub_tab)
        final_tab=vstack(table_list)
    return final_tab


def __ensure_unit(x, unit: u.Unit):
    """Helper method to ensure input units are correct.

    Args:
        x (any): Variable to check
        unit (astropy.units.Unit): Desired unit 
    Returns:
        astropy.units.Quantity: Parameter x with proper unit attached. 
    Raises:
        UnitTypeError: Raised when quantity requires conversion, but conversion cannot be completed
    """

    if x is None:
        return x
    if not isinstance(x, Quantity):
        x = x * unit
    elif x.unit != unit:
        try:
            x = x.to(unit)
        except u.UnitConversionError as uce:
            raise u.UnitTypeError(f"{x} cannot be converted to {unit}")
    return x

def __dist_from_Seff(Seff, L):
    """Helper method to convert Seff to distance (AU)"""
    #L must be in solar units
    d = (L / Seff) ** 0.5
    return d

def find_hz(st_teff, st_lum):
    """Returns the habitable zone bounds as specified by Kopparapu et al. 2014 (2014ApJ...787L..29K) for a given temperature and luminosity. 
    Both optimistic (Recent Venus-Early Mars) and conservative (runaway/maximum greenhouse) bounds are returned.
    Note:
        return table entries rg0.1, rg1, and rg5 correspond to the 0.1, 1, and 5 Earth mass runaway greenhouse values. 

    Args:
        st_teff (number or u.Quantity): Stellar effective temperature, either as a generic number or u.K
        st_lum (number or u.Quantity): Steller luminosity (expected as u.Lsun or equivalent generic number)

    Returns:
        pd.DataFrame: DataFrame containing the max/min distances (AU) from the host star matching (st_teff, st_lum) for each habitable zone scenario calculated in 2014ApJ...787L..29K
    
    """

    def KopparapuEqnFour(SeffSUN, a, b, c, d, tS):
        Seff = SeffSUN + a * tS + b * ((tS) ** 2) + c * ((tS) ** 3) + d * ((tS) ** 4)
        return Seff
    
    L = __ensure_unit(st_lum, u.Lsun)
    T_s = __ensure_unit(st_teff, u.K) - 5780 * u.K
    
    recent_venus = {'label': 'rv', 'Seff': 1.776000 , 'a': 2.136000e-04 , 'b': 2.533000e-08, 'c': -1.33200e-11, 'd': -3.09700e-15}
    runaway_greenhouse_1Mearth = {'label': 'rg1', 'Seff': 1.107, 'a': 1.332000e-04 , 'b': 1.580000e-08, 'c': -8.30800e-12, 'd': -1.93100e-15}
    maximum_greenhouse = {'label': 'mxg', 'Seff': 3.560000e-01, 'a': 6.171000e-05 , 'b': 1.698000e-09, 'c': -3.19800e-12, 'd': -5.57500e-16}
    early_mars = {'label': 'em', 'Seff': 3.200000e-01, 'a': 5.547000e-05 , 'b': 1.526000e-09, 'c': -2.87400e-12, 'd': -5.01100e-16}
    runaway_greenhouse_5Mearth = {'label': 'rg5', 'Seff': 1.188000, 'a': 1.433000e-04 , 'b': 1.707000e-08, 'c': -8.96800e-12, 'd': -2.08400e-15}
    runaway_greenhouse_01Mearth = {'label': 'rg0.1', 'Seff': 9.900000e-01, 'a': 1.209000e-04 , 'b': 1.404000e-08, 'c': -7.41800e-12, 'd': -1.71300e-15}
    
    coeff_matrix = pd.DataFrame([recent_venus, runaway_greenhouse_01Mearth, runaway_greenhouse_1Mearth, 
                                 runaway_greenhouse_5Mearth, maximum_greenhouse, early_mars])
    coeff_matrix.set_index('label', inplace=True)

    #Add column with the result of eqn. 4 in Kopparapu 2014
    for index, row in coeff_matrix.iterrows():
        #todo carry units through
        SeffBound = KopparapuEqnFour(row['Seff'], row['a'], row['b'], row['c'], row['d'], T_s.value)
        coeff_matrix.at[index,'SeffBound'] = SeffBound
        distau = __dist_from_Seff(SeffBound, L.value)
        if distau  > 0: 
           coeff_matrix.at[index,'distBound(AU)'] = distau
        else:
            raise RuntimeError("Negative distance AAAAAAAAAAAAAAAAA")

    
    return coeff_matrix