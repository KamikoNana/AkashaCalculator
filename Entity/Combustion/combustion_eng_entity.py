## Combustion enginery 
# (phase, enginery, fueltype, quantity, number)


class CombustionEnginery:
    def __init__(self, phase, enginery_fueltype, quantity, n):
        self.phase = phase                          #project phase
        self.enginery_fueltype = enginery_fueltype                    #enginery type (str)
        self.quantity = quantity                    #quantity of fuel used per year [L/year] (float)
        self.n = n                        #number of machines (int)