"""
This file contains the Entity for the Combustion Enginery emissions source. 
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

class CombustionEnginery:
    def __init__(self, phase, enginery_fueltype, quantity, n):
        self.phase = phase                                      #project phase (enum ProjectPhase.Phase)
        self.enginery_fueltype = enginery_fueltype              #name - enginery type (str)
        self.quantity = quantity                                #quantity of fuel used per year [L/year] (float)
        self.n = n                                              #number of machines (int)