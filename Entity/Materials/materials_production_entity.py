"""
This file contains the Entity for the Materials Production emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class MaterialsProduction:
    def __init__(self, phase, material, process, quantity, ef):
        self.phase = phase                          #project phase
        self.material = material                    #material used (str)
        self.process = process                      #production process (str)
        self.quantity = quantity                    #quantity of material produced per year [kg/year] (float)
        self.ef = ef                                #emission factor of the material production [tCO2eq/kg] (float)
    
    def total_GHG_emissions(phase, quantity, ef):
        if phase == "CONSTRUCTION":
            duration = float(ProjectPhasesService.project_duration()[0])
            return quantity * ef * duration
        elif phase == "OPERATION":
            duration = float(ProjectPhasesService.project_duration()[1])
            return quantity * ef * duration
    
    def to_dict(self):
        return {"phase": self.phase, "material": self.material, "process": self.process, \
            "quantity": self.quantity, "ef": self.ef}
    
    @staticmethod
    def materialprod_from_dict(dict):
        return MaterialsProduction(dict["phase"], dict["material"], dict["process"], dict["quantity"], dict["ef"])