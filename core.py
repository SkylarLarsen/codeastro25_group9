
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad

from astropy import units as u
from astropy.units import Quantity, UnitTypeError
from astropy.constants import R_earth, M_earth, R_sun, M_sun, G

import pandas as pd
import matplotlib.pyplot as plt


def get_current_parameters(planet_name='Kepler-22 b'):
  '''
  Returns:
  Dictionary of stellar parameters. Keys in dictionary include:
  Planet Mass [Msun]
  T_eff of star [K]
  Luminosity of Star [Lsun]
  Radius of star [Rsun]

  Args:
  name_planet: name of planet in nasa exoplanet archive (string)
  name_star: name of star in Simbad (string)
  '''
  tab = NasaExoplanetArchive.query_criteria(table="pscomppars", where=f"pl_name='{planet_name}'").to_pandas()
  dict = tab.to_dict(orient='records')[0]
  #star_dict = star_tab.to_dict(orient='records')[0]
  return dict

# def evolve_stellar_parameters(stellar_parameters: dict, current_age, target_age) -> dict:

#   return aged_stellar_parameters


# def find_habitable_zone(st_teff, st_lum, pl_mass):

#   inner = 0
#   outer = 0
  
#   bounds = [inner, outer]
#   return bounds

def visualize(df, time_bc, distance_bc, planet_AU):
    """
    Inputs
    ------

    df : dataframe
        Columns are time, distance_hz_in, distance_hz_out
    
    time_bc : list
        The lower and upper time boundary conditions for your plot. Units in Gyr
    
    distance_bc : list
        The lower and upper distance-from-star boundary conditions for your plot. Units in AU
    
    planet_AU : list
        List of planet distances from star in AU
    
    Returns
    -------
    plots how habitable zone changes over time
    """

    df = df[(df.time > time_bc[0]) | (df.time < time_bc[1])] # trim x axis

    plt.fill_between(df["time"], df["distance_hz_in"], y2= df["distance_hz_out"], color = 'green', alpha = 0.4)
    
    for i in planet_AU:
        plt.axhline(y=i, color='k', linestyle='--')

    plt.ylim(distance_bc)

    plt.title("Habitable Zone over Time")
    plt.xlabel("Time (Gyr)")
    plt.ylabel("Distance from Star (AU)")

    plt.show()


def ensure_unit(x, unit: u.Unit):
    """Helper method to ensure input units are correct
    :param x: Variable to check
    :param unit: Desired unit (astropy.unit)
    :returns x: Parameter x with proper unit attached. 
    :raises UnitTypeError: UnitTypeError raised when quantity requires conversion, but conversion cannot be completed
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