class calc:
    def alpha_beta_gamma(self, mass):
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

    def luminosity_evolve(self, L_0, beta, t_f, t):
        L_t = L_0 * (1 + beta * (t / t_f))
        return L_t
    
    def radius_evolve(self, R_0, gamma, t_f, t):
        R_t = R_0 * (1 + gamma * (t / t_f))
        return R_t
    
    def temp_evolve(self, T_0, L_t, L_0, R_t, R_0):
        T_t = T_0 * (L_t / L_0)**(1/4) * (R_t / R_0)**(-1/2)
        return T_t
    
