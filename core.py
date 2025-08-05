
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad
import pandas as pd

def get_current_parameters(planet_name='Earth',star_name='Sun'):
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
  composite_set = NasaExoplanetArchive.query_criteria(table="pscomppars", where=f"pl_name='{planet_name}'")#where=f"disc_facility like'{planet_name}'"
  comp_df = composite_set.to_pandas()
  #comp_dict = comp_df.to_dict(orient='records')[0]
  return comp_df

  # pl = Planet(name=comp_dict['pl_name'], properties=comp_dict)

  # table = NasaExoplanetArchive.query_criteria(table=table, where=f"hostname='{star_name}' and st_teff IS NOT null")
  # try:
  #     t_dict = table.to_pandas().to_dict(orient='records')[0]
  # except IndexError:
  #     raise ValueError(f"No IPAC stellar entries found for {star_name}")
  # try:
  #     spec_type = Simbad.query_tap(f"SELECT main_id, sp_type FROM basic WHERE main_id = '{star_name}'")['sp_type'][0]
  #     t_dict['st_spectype_simbad'] = spec_type
  # except Exception as e:
  #     spec_type = None
  #     t_dict['st_spectype_simbad'] = spec_type
    # star = Star(name=star_name, properties=t_dict)
  #, t_dict

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
