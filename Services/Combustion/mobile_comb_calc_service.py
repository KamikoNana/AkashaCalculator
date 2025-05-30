"""
This file contains the Service for the Mobile Combustion Machinery emissions source. 
- Includes all calculations for the Mobile Combustion Machinery class elements
Division between Fixed and Mobile Combustion Machinery lies in the diference of variables required.
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.Combustion.mobile_comb_entity import MobileCombustion
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class MobileCombustionCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
        
    def total_emissions_mobilecomb(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_mobilecomb = 0
        emissions_mobilecomb =[]
        for source, data in self.ghg_database["mobile_combustion"].items():
            mobile = MobileCombustion.mobilecomb_from_dict(data)
            
            total_emissions_mobilecomb = total_emissions_mobilecomb + \
                mobile.total_GHG_emissions(self.project_durations)
            emissions_mobilecomb.append([mobile.enginery_fueltype, mobile.n, \
                mobile.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_mobilecomb, emissions_mobilecomb]
    
    def phase_emissions_mobilecomb(self):
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_mobilecomb = 0
        operation_emissions_mobilecomb = 0
        for source, data in self.ghg_database["mobile_combustion"].items():
            mobile = mobile.mobilecomb_from_dict(data)
            
            if Phase[mobile.phase] == Phase.CONSTRUCTION:
                construction_emissions_mobilecomb = construction_emissions_mobilecomb + \
                    mobile.total_GHG_emissions(self.project_durations)
            elif Phase[mobile.phase] == Phase.OPERATION:
                operation_emissions_mobilecomb = operation_emissions_mobilecomb + \
                    mobile.total_GHG_emissions(self.project_durations)
            else:
                pass
        
        return [construction_emissions_mobilecomb, operation_emissions_mobilecomb]
    

    
    def total_emissions_peryear_mobilecomb(self):
        """
        Calculates the total commulative sum of GHG emissions for this emissions source per year of the project horizon
        """
        construction_duration = math.ceil(self.project_durations[0])
        operation_duration = math.ceil(self.project_durations[1])
        full_duration = math.ceil(self.project_durations[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
  
        for source, data in self.ghg_database["mobile_combustion"].items():
            mobile = MobileCombustion.mobilecomb_from_dict(data)
            
            if Phase[mobile.phase] == Phase.CONSTRUCTION:
                total_fuel = mobile.quantity * mobile.n
                CO2_totalemissions = total_fuel * mobile.co2_emissions 
                CH4_totalemissions = total_fuel * mobile.ch4_emissions * mobile.ch4_cf
                N2O_totalemissions = total_fuel * mobile.n2o_emissions * mobile.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                for i in range(construction_duration):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
            elif Phase[mobile.phase] == Phase.OPERATION:
                total_fuel = mobile.quantity * mobile.n
                CO2_totalemissions = total_fuel * mobile.co2_emissions 
                CH4_totalemissions = total_fuel * mobile.ch4_emissions * mobile.ch4_cf
                N2O_totalemissions = total_fuel * mobile.n2o_emissions * mobile.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                for i in range(operation_duration):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear