class calc:
    def alpha_value(self, mass):
        if mass <0.43:
            alpha=2.3
        elif 0.43<mass<2:
            alpha=4
        elif 2<mass<20:
            alpha=3.5
        elif mass>20:
            alpha=1.0
        else:
            returnValueError('InValid Mass: Not a number!!')
        return alpha

    def 