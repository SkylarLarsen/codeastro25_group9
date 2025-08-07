# ------ TEST w sun like star before querying -------
import numpy as np
import matplotlib.pyplot as plt
from hztrak.evol_calc import calc

# instantiate the class
model = calc()

# user-defined initial conditions for a Sun-like star
M_star = 1.0         # Solar masses
L_0 = 1.0            # Solar luminosity (L_sun)
T_0 = 5772.0         # Solar effective temperature (K)
R_0 = 1.0            # Solar radius (R_sun)
t_f = 1e9           # Approximate MS lifetime (yrs)
steps = 10

times, L_arr, R_arr, T_arr = model.evolve_star(L_0, R_0, T_0, M_star, t_f, steps)

for i in range(steps):
    print(f"t = {times[i]/1e9:.1f} Gyr | L = {L_arr[i]:.3f} L_sun | R = {R_arr[i]:.3f} R_sun | T = {T_arr[i]:.1f} K")

'''
# Convert time to Gyr for readability
times_gyr = times / 1e9

# Plot all on the same graph
plt.figure(figsize=(10, 6))
plt.plot(times_gyr, L_arr, label='Luminosity (L/L☉)', marker='o')
plt.plot(times_gyr, R_arr, label='Radius (R/R☉)', marker='s')
plt.plot(times_gyr, T_arr / 5772.0, label='Temperature (T/T☉)', marker='^')  # Normalize T to T☉

plt.xlabel('Time (Gyr)')
plt.ylabel('Normalized Quantity')
plt.title('Stellar Evolution Over Time (Solar Mass Star)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''

