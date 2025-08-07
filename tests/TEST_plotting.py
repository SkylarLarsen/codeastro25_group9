import matplotlib.pyplot as plt
import matplotlib.axes
import pandas as pd
import numpy as np
from astropy.table import QTable
import astropy.units as u


# d_TEST = {'time': pd.Series([0, 1, 2, 3]),
#      'distance_hz_in': pd.Series([0.8, 0.8, 0.9, 1.2]),
#      'distance_hz_out': pd.Series([1, 1, 1.1, 1.5]),
#                       }

# df_TEST = pd.DataFrame(d_TEST)



a = np.array([0, 1, 2, 3], dtype=np.int32) * u.Gyr

b = [0.8, 0.8, 0.9, 1.2] * u.AU

c = [1, 1, 1.1, 1.5] * u.AU

at_TEST = QTable([a, b, c],
           names=('time', 'distance_hz_in', 'distance_hz_out'),
           meta={'name': 'hz table'})




def visualize_1(astropy_table, planet_AU):
    """Visualization_1

    Plot the evolution of the habitable zone over time.

    Args:
        astropy_table (astropy_table): Columns are time, distance_hz_in, distance_hz_out

        planet_AU (list): List of planet distances from star in AU
    
    Returns:
        fig, ax
    """

    df = astropy_table.to_pandas()

    fig, ax = plt.subplots(figsize = (12,7))
    ax.fill_between(df["time"], df["distance_hz_in"], y2= df["distance_hz_out"], color = 'green', alpha = 0.4)
    
    for i in planet_AU:
        ax.axhline(y=i, color='k', linestyle='--')

    ax.set_title("Habitable Zone over Time")
    ax.set_xlabel(f"Time ({astropy_table['time'].unit})")
    ax.set_ylabel(f"Distance from Star ({astropy_table['distance_hz_in'].unit})")

    return fig, ax


TEST_plot, TEST_ax = visualize_1(at_TEST, [0,4], [0.5,1.7], [0.7, 1.1, 1.5])
TEST_ax.set_xlim(0,3)
TEST_ax.set_ylim(0.5,1.7)
plt.show()


#------------POLAR PLOT-------------------------------------------------

'''d_TEST = {
    'pl_orbsmax': pd.Series([0.6, 1.0, 1.3, 1.8, 2.0, 2.2, 2.6]),
    'distance_hz_in': pd.Series([0.5]*7),
    'distance_hz_out': pd.Series([2.5]*7),
 }
 
d_TEST = {'pl_orbsmax': pd.Series([0, 1, 2, 3]),
      'distance_hz_in': pd.Series([0.8, 0.8, 0.9, 1.2]),
      'distance_hz_out': pd.Series([1, 1, 1.1, 1.5]),
                       }

df_TEST = pd.DataFrame(d_TEST)'''

a = np.array([0, 1, 2, 3], dtype=np.int32) * u.AU

b = [0.8, 0.8, 0.9, 1.2] * u.AU

c = [1, 1, 1.1, 1.5] * u.AU

at_TEST = QTable([a, b, c],
            names=('pl_orbsmax', 'distance_hz_in', 'distance_hz_out'),
            meta={'name': 'hz table'})



def visualize_polar(astropy_table, distance_bc, habitable_zone):

    df = astropy_table.to_pandas()
    theta = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    distance_bc = df['pl_orbsmax'] #orbit semi-major axis [AU]
    colors = distance_bc
    area = 200

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='polar')

    theta_fill = np.linspace(0, 2*np.pi, 500)
    distance_hz_in, distance_hz_out = habitable_zone
    ax.fill(theta_fill, [distance_hz_out]*len(theta_fill), color='lightgreen', alpha=0.3, zorder=0)
    ax.fill(theta_fill, [distance_hz_in]*len(theta_fill), color='white', alpha=1.0, zorder=1)

    ax.scatter(0, 0, marker='*', color='gold', s=500, label='The star', zorder=5)

    scatter = ax.scatter(theta, distance_bc, c=colors, s=area, cmap='plasma', alpha=0.75, zorder=3)

    plt.colorbar(scatter, ax=ax, label='Distance from the star (AU)')
    ax.set_title('Polar plot of the planets in the habitable zone')

    plt.show()
    
habitable_zone = (1.0,2.0) #I still have to figure out how to connect with nick's part
TEST_plot, TEST_ax = visualize_polar(at_TEST, [0, 7], habitable_zone)
TEST_ax.set_xlim(0,3)
TEST_ax.set_ylim(0.5,1.7)
plt.show()
