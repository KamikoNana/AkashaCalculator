"""
This file contains the Service for the Fixed Combustion Enginery emissions source. 
- Includes all calculations for the Fixed Combustion Machinery class elements
Division between Fixed and Mobile Combustion Enginery lies in the diference of variables required.
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.Combustion.fixed_comb_entity import FixedCombustion
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase


class FixedCombustionCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
        
    def total_emissions_fixedcomb(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_fixedcomb = 0
        emissions_fixedcomb =[]
        for source, data in self.ghg_database["fixed_combustion"].items():
            fixed = FixedCombustion.fixedcomb_from_dict(data)
            
            total_emissions_fixedcomb = total_emissions_fixedcomb + \
                fixed.total_GHG_emissions(self.project_durations)
            emissions_fixedcomb.append([fixed.enginery_fueltype, fixed.n, \
                fixed.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_fixedcomb, emissions_fixedcomb]
    
    def phase_emissions_fixedcomb(self):
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_fixedcomb = 0
        operation_emissions_fixedcomb = 0
        for source, data in self.ghg_database["fixed_combustion"].items():
            fixed = FixedCombustion.fixedcomb_from_dict(data)
            
            if Phase[fixed.phase] == Phase.CONSTRUCTION:
                construction_emissions_fixedcomb = construction_emissions_fixedcomb + \
                    fixed.total_GHG_emissions(self.project_durations)
            elif Phase[fixed.phase] == Phase.OPERATION:
                operation_emissions_fixedcomb = operation_emissions_fixedcomb + \
                    fixed.total_GHG_emissions(self.project_durations)
            else:
                pass
        
        return [construction_emissions_fixedcomb, operation_emissions_fixedcomb]
    
    def total_emissions_peryear_fixedcomb(self):
        """
        Calculates the total commulative sum of GHG emissions for this emissions source per year of the project horizon
        """
        construction_duration = math.ceil(self.project_durations[0])
        operation_duration = math.ceil(self.project_durations[1])
        full_duration = math.ceil(self.project_durations[2])
        
        rem_construction = self.project_durations[0] % 1
        rem_operation = self.project_durations[1] % 1
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        emissions_peryear_construction = 0
        emissions_peryear_operation = 0
                
        for source, data in self.ghg_database["fixed_combustion"].items():
            fixed = FixedCombustion.fixedcomb_from_dict(data)
            
            if Phase[fixed.phase] == Phase.CONSTRUCTION:
                emissions = fixed.quantity * fixed.ef
                
                emissions_peryear_construction += emissions
                
            elif Phase[fixed.phase] == Phase.OPERATION:
                emissions = fixed.quantity * fixed.ef
                
                emissions_peryear_operation += emissions
                
            else:
                pass
        
        for i in range (construction_duration):
            total_emissions_peryear_construction[i] = emissions_peryear_construction
        for i in range (operation_duration):
            total_emissions_peryear_operation[i] = emissions_peryear_operation
        
        if rem_construction != 0:
            total_emissions_peryear_construction[-1] = (rem_construction * emissions_peryear_construction) + ( (1-rem_construction) * emissions_peryear_operation)
            total_emissions_peryear_operation[-1] = (rem_construction * emissions_peryear_operation)
        if rem_operation != 0:
            total_emissions_peryear_operation[-1] = (rem_operation * emissions_peryear_operation) + (rem_construction * emissions_peryear_operation)
        if (rem_construction + rem_operation) > 1:
            total_emissions_peryear_operation[-1] = ((rem_construction + rem_operation) - 1) * emissions_peryear_operation 
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear