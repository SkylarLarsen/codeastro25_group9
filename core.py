
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad
import pandas as pd

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

# def visualize():
#   #plot results
#   return 
