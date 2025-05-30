"""
This file contains the Entity for the Energy emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

from enum import Enum
from Entity.ProjectPhases.project_phases_entity import Phase

class EnergyType(Enum):
    """
    subclass to define the energy type as enum variable
    """
    CONSUMED = 1
    PRODUCED = 2

class Energy:
    def __init__(self, phase, type, source, quantity, ef):
        self.phase = phase                                  #project phase (enum ProjectPhase.Phase)
        self.type = type                                    #energy category (enum Energy.EnergyType)
        self.source = source                                #name - energy source (str)
        self.quantity = quantity                            #quantity of energy used per year [MW/year] (float)
        self.ef = ef                                        #emission factor [tCO2/MW] (float)
    
    def total_GHG_emissions(self, durations):
        """
        Calculates the total GHG emissions for 1 element in this class
        """

        if Phase[self.phase] == Phase.CONSTRUCTION:
            duration = float(durations[0])
        elif Phase[self.phase] == Phase.OPERATION:
            duration = float(durations[1])
            
        return self.quantity * self.ef * duration
            
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """
        return {"phase": self.phase, "type": self.type, "source": self.source, "quantity": self.quantity, "ef": self.ef}
    
    @staticmethod
    def energy_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """
        return Energy(dict["phase"], dict["type"], dict["source"], dict["quantity"], dict["ef"])
    
    