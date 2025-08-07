import numpy as np
import matplotlib.pyplot as plt

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
        if mass < 0.43:
            alpha=2.3
            beta=0.1
            gamma=0.05
        elif 0.43 <= mass < 2:
            alpha=4
            beta=0.4
            gamma=0.1
        elif 2.0 <= mass < 20.0:
            alpha=3.5
            beta=0.7
            gamma=0.2
        elif mass >= 20:
            alpha=1.0
            beta=0.9
            gamma=0.3
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
        times = np.linspace(0, t_f, steps)
        
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

        return np.array(times), np.array(L_vals), np.array(R_vals), np.array(T_vals)

# ------ use w query -------
model = calc()




# ------ TEST w sun like star before querying -------

#from habitability_calc import calc

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

