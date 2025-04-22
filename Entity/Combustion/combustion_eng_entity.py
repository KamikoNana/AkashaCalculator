"""
This file contains the Entity for the Combustion Enginery emissions source. 
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

class CombustionEnginery:
    def __init__(self, phase, enginery_fueltype, quantity, n):
        self.phase = phase                                      #project phase (str)
        self.enginery_fueltype = enginery_fueltype              #enginery type (str)
        self.quantity = quantity                                #quantity of fuel used per year [L/year] (float)
        self.n = n                                              #number of machines (int)