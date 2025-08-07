import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.axes

def visualize_1(astropy_table, time_bc, distance_bc, planet_AU):
    """Visualization_1

    Plot the evolution of the habitable zone over time.

    Args:
        astropy_table (astropy_table): Columns are time, distance_hz_in, distance_hz_out
    
        time_bc (list): The lower and upper time boundary conditions for your plot. Units in Gyr
    
        distance_bc (list): The lower and upper distance-from-star boundary conditions for your plot. Units in AU
    
        planet_AU (list): List of planet distances from star in AU
    
    Returns:
        matplotlib.axes.Axes
    """

    df = astropy_table.to_pandas()

    df = df[(df.time > time_bc[0]) | (df.time < time_bc[1])] # trim x axis

    plt.fill_between(df["time"], df["distance_hz_in"], y2= df["distance_hz_out"], color = 'green', alpha = 0.4)
    
    for i in planet_AU:
        plt.axhline(y=i, color='k', linestyle='--')

    plt.ylim(distance_bc)

    plt.title("Habitable Zone over Time")
    plt.xlabel(f"Time ({astropy_table['time'].unit})")
    plt.ylabel(f"Distance from Star ({astropy_table['distance_hz_in'].unit})")

    plt.show()
    return matplotlib.axes.Axes



def visualize_polar(df, time_bc, distance_bc, habitable_zone):
    
    # Filter based on time and distance
    df = df[(df.time > time_bc[0]) & (df.time < time_bc[1])]
    df = df[(df.distance_planet_star > distance_bc[0]) & (df.distance_planet_star < distance_bc[1])]

    theta = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    r = df['distance_planet_star']
    colors = r
    area = 200

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='polar')

    theta_fill = np.linspace(0, 2*np.pi, 500)
    r_inner, r_outer = habitable_zone
    ax.fill(theta_fill, [r_outer]*len(theta_fill), color='lightgreen', alpha=0.3, zorder=0)
    ax.fill(theta_fill, [r_inner]*len(theta_fill), color='white', alpha=1.0, zorder=1)

    ax.scatter(0, 0, marker='*', color='gold', s=500, label='The star', zorder=5)

    scatter = ax.scatter(theta, r, c=colors, s=area, cmap='plasma', alpha=0.75, zorder=3)

    plt.colorbar(scatter, ax=ax, label='Distance from the star (AU)')
    ax.set_title('Polar plot of the planets in the habitable zone')

    plt.show()