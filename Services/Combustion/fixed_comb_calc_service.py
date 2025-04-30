"""
This file contains the Service for the Fixed Combustion Enginery emissions source. 
- Includes all calculations for the Fixed Combustion Machinery class elements
Division between Fixed and Mobile Combustion Enginery lies in the diference of variables required.
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math

import ghg_database

from Entity.Combustion.fixed_comb_entity import FixedCombustion
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class FixedCombustionCalculations():
    def __init__(self):
        self
        
    def total_emissions_fixedcomb():
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_fixedcomb = 0
        emissions_fixedcomb =[]
        for source, data in ghg_database.fixed_combustion.items():
            data = FixedCombustion.fixedcomb_from_dict(data)
            
            total_emissions_fixedcomb = total_emissions_fixedcomb + \
                FixedCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, data.ef)
            emissions_fixedcomb.append([data.enginery_fueltype, data.n, \
                FixedCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, data.ef)])
        
        return [total_emissions_fixedcomb, emissions_fixedcomb]
    
    def phase_emissions_fixedcomb():
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_fixedcomb = 0
        operation_emissions_fixedcomb = 0
        for source, data in ghg_database.fixed_combustion.items():
            data = FixedCombustion.fixedcomb_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                construction_emissions_fixedcomb = construction_emissions_fixedcomb + \
                    FixedCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, data.ef)
            elif Phase[data.phase] == Phase.OPERATION:
                operation_emissions_fixedcomb = operation_emissions_fixedcomb + \
                    FixedCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, data.ef)
            else:
                pass
        
        return [construction_emissions_fixedcomb, operation_emissions_fixedcomb]
    
    def total_emissions_peryear_fixedcomb():
        """
        Calculates the total commulative sum of GHG emissions for this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
                
        for source, data in ghg_database.fixed_combustion.items():
            data = FixedCombustion.fixedcomb_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                emissions = data.quantity * data.ef
                for i in range(construction_duration):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
            elif Phase[data.phase] == Phase.OPERATION:
                emissions = data.quantity * data.ef
                for i in range(operation_duration):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear