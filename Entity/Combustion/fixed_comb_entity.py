"""
This file contains the Entity for the Fixed Combustion Machinery emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
Division between Fixed and Mobile Combustion Machinery lies in the diference of variables required.
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

from Entity.Combustion.combustion_eng_entity import CombustionEnginery
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class FixedCombustion(CombustionEnginery):
    def __init__(self, phase, enginery_fueltype, quantity, n, ef):
        super().__init__(phase, enginery_fueltype, quantity, n)
        self.ef = ef                                                #emission factor [tCO2/L] (float)
        
    def total_GHG_emissions(phase, quantity, n, ef):
        """
        Calculates the total GHG emissions for 1 element in this class
        """
        total_fuel = quantity * n
        
        if Phase[phase] == Phase.CONSTRUCTION:
            duration = float(ProjectPhasesService.project_duration()[0])
            return total_fuel * ef * duration
        elif Phase[phase] == Phase.OPERATION:
            duration = float(ProjectPhasesService.project_duration()[1])
            return total_fuel * ef * duration
        
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """
        return {"phase": self.phase, "enginery_fueltype": self.enginery_fueltype, "quantity": self.quantity, \
            "n_machines": self.n, "ef": self.ef}
    
    @staticmethod
    def fixedcomb_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """
        return FixedCombustion(dict["phase"], dict["enginery_fueltype"], dict["quantity"], dict["n_machines"], dict["ef"])