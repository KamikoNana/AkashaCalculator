"""
This file contains the Entity for the Waste Treatment emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the Akacha Guidebook avaliable in the GitHub repository
"""

from enum import Enum
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class WasteType(Enum):
    """
    subclass to define the waste type as enum variable
    """
    WATER = 1
    SOLID = 2
    GAS = 3
        
class WasteTreatment:
    def __init__(self, phase, treatment, stream, quantity, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        self.phase = phase                                      #project phase (enum ProjectPhase.Phase)
        self.treatment = treatment                              #treatment type (str)
        self.stream = stream                                    #used to gategorize the stream (enum WasteTreatment.WasteType)
        self.quantity = quantity                                #quantity of treated materials per year [L/year] (float)
        self.co2_emissions = co2_emissions                      #emissions of the fuel use [tonCO2/L] (float)
        self.ch4_emissions = ch4_emissions                      #emissions of the fuel use [tonCH4/L] (float)
        self.ch4_cf = ch4_cf                                    #conversion factor of CH4 to CO2eq [adimensional] (float)                          
        self.n2o_emissions = n2o_emissions                      #emissions of the fuel use [tonN2O/L] (float)
        self.n2o_cf = n2o_cf                                    #conversion factor of CH4 to CO2eq [adimensional] (float)
    
    def total_GHG_emissions(self, duration):
        """
        Calculates the total GHG emissions for 1 element in this class
        """        
        CO2_totalemissions = self.co2_emissions 
        CH4_totalemissions = self.ch4_emissions * self.ch4_cf
        N2O_totalemissions = self.n2o_emissions * self.n2o_cf
        total_emissions = (CO2_totalemissions + CH4_totalemissions + N2O_totalemissions) * self.quantity
        
        if Phase[self.phase] == Phase.CONSTRUCTION:
            duration = float(ProjectPhasesService.project_duration()[0])
        elif Phase[self.phase] == Phase.OPERATION:
            duration = float(ProjectPhasesService.project_duration()[1])
            
        return total_emissions * duration
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """
        return {"phase": self.phase, "treatment": self.treatment, "stream": self.stream, "quantity": self.quantity, \
            "co2_emissions": self.co2_emissions, "ch4_emissions": self.ch4_emissions, \
                "ch4_cf": self.ch4_cf, "n2o_emissions": self.n2o_emissions, "n2o_cf": self.n2o_cf}
    
    @staticmethod    
    def waste_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """
        return WasteTreatment(dict["phase"], dict["treatment"], dict["stream"], \
            dict["quantity"], dict["co2_emissions"], dict["ch4_emissions"], dict["ch4_cf"]\
                , dict["n2o_emissions"], dict["n2o_cf"])
    
    