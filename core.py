
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.simbad import Simbad
import pandas as pd

def get_current_parameters(planet_name=['Kepler-22 b']):
  '''
  Returns:
  Pandas Dataframe of stellar and planet parameters

  Args:
  name_planet: list of names of planets in nasa exoplanet archive (string)
  '''
  data=[]
  for i in range(len(planet_name)):
    tab = NasaExoplanetArchive.query_criteria(table="pscomppars", where=f"pl_name='{planet_name[i]}'").to_pandas()
    if len(tab)==0:
      data.append({'pl_name':planet_name[i],           #planet name

      })
      continue
    else:
      planet_dict = tab.to_dict(orient='records')[0]
      data.append({'pl_name':planet_dict['pl_name'],           #planet name
          'hostname':planet_dict['hostname'],       #host star name
          'pl_rade': planet_dict['pl_rade'],          #planet radius [earth radius]
          'pl_masse': planet_dict['pl_masse'] ,        #planet mass [earth mass]
          'pl_ratror': planet_dict['pl_ratror'],        #Ratio of Planet to Stellar Radius
          'st_teff':planet_dict['st_teff'],          #stellar effective temperature [K]
          'st_rad':planet_dict['st_rad'],           #stellar radius [Rsun]
          'st_mass':planet_dict['st_mass'],          #stellar mass [Msun]
          'st_lum':planet_dict['st_lum'],           #Stellar Luminosity [log10(Solar)]
          'st_age' :planet_dict['st_age'],          #stellar age [Gyr]
          'pl_orbper':planet_dict['pl_orbper'],        #Orbital period [days]
          'pl_orbsmax':planet_dict['pl_orbsmax'],       #Orbit Semi-Major Axis [au]
          })
  df=pd.DataFrame(data)
      
  return df

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
