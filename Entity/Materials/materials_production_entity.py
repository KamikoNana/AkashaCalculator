"""
This file contains the Entity for the Materials Production emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class MaterialsProduction:
    def __init__(self, phase, material, process, quantity, ef):
        self.phase = phase                                      #project phase (enum ProjectPhase.Phase)
        self.material = material                                #material produced (str)
        self.process = process                                  #production process (str)
        self.quantity = quantity                                #quantity of material produced per year [kg/year] (float)
        self.ef = ef                                            #emission factor of the material production [tCO2eq/kg] (float)
    
    def total_GHG_emissions(phase, quantity, ef):
        """
        Calculates the total GHG emissions for 1 element in this class
        """        
        if Phase[phase] == Phase.CONSTRUCTION:
            duration = float(ProjectPhasesService.project_duration()[0])
            return quantity * ef * duration
        elif Phase[phase] == Phase.OPERATION:
            duration = float(ProjectPhasesService.project_duration()[1])
            return quantity * ef * duration
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """        
        return {"phase": self.phase, "material": self.material, "process": self.process, \
            "quantity": self.quantity, "ef": self.ef}
    
    @staticmethod
    def materialprod_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """        
        return MaterialsProduction(dict["phase"], dict["material"], dict["process"], dict["quantity"], dict["ef"])