"""
This file contains the Entity for the Fixed Combustion Machinery emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
Division between Fixed and Mobile Combustion Machinery lies in the diference of variables required. 
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.Combustion.combustion_eng_entity import CombustionEnginery
from Entity.ProjectPhases.project_phases_entity import Phase

class MobileCombustion(CombustionEnginery):
    def __init__(self, phase, enginery_fueltype, quantity, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        super().__init__(phase, enginery_fueltype, quantity, n)
        self.co2_emissions = co2_emissions                          #emissions of the fuel [tonCO2/L] (float)
        self.ch4_emissions = ch4_emissions                          #emissions of the fuel [tonCH4/km] (float)
        self.ch4_cf = ch4_cf                                        #conversion factor of CH4 to CO2eq [adimensional] (float)                          
        self.n2o_emissions = n2o_emissions                          #emissions of the fuel [tonN2O/km] (float)
        self.n2o_cf = n2o_cf                                        #conversion factor of CH4 to CO2eq [adimensional] (float)
        
    def total_GHG_emissions(phase, quantity, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        """
        Calculates the total GHG emissions for 1 element in this class
        """
        total_fuel = quantity * n
        CO2_totalemissions = total_fuel * co2_emissions 
        CH4_totalemissions = total_fuel * ch4_emissions * ch4_cf
        N2O_totalemissions = total_fuel * n2o_emissions * n2o_cf
        total_emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
        
        if Phase[phase] == Phase.CONSTRUCTION:
            duration = float(ProjectPhasesService.project_duration()[0])
            return total_emissions * duration
        elif Phase[phase] == Phase.OPERATION:
            duration = float(ProjectPhasesService.project_duration()[1])
            return total_emissions * duration
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """
        return {"phase": self.phase, "enginery_fueltype": self.enginery_fueltype, "quantity": self.quantity, \
            "n_machines": self.n, "co2_emissions": self.co2_emissions, "ch4_emissions": self.ch4_emissions, \
                "ch4_cf": self.ch4_cf, "n2o_emissions": self.n2o_emissions, "n2o_cf": self.n2o_cf}
    
    @staticmethod    
    def mobilecomb_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """
        return MobileCombustion(dict["phase"], dict["enginery_fueltype"], \
            dict["quantity"], dict["n_machines"], dict["co2_emissions"], dict["ch4_emissions"], dict["ch4_cf"]\
                , dict["n2o_emissions"], dict["n2o_cf"])