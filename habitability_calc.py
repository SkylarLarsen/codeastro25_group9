class calc:
    def alpha_beta_gamma(self, mass):
        if mass <0.43:
            alpha=2.3
            beta=0.1
            gamma=0.05
        elif 0.43<mass<2:
            alpha=4
            beta=0.4
            gamma=0.1
        elif 2<mass<20:
            alpha=3.5
            beta=0.7
            gamma=0.2
        elif mass>20:
            alpha=1.0
            beta=0.9
            gamma=0.3
        else:
            returnValueError('Invalid Mass: Not a number!!')
        return alpha, beta, gamma

    