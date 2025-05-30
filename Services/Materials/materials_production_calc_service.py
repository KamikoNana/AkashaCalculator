"""
This file contains the Service for the Materials Production emissions source. 
- Includes all calculations for the Materials Production class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.Materials.materials_production_entity import MaterialsProduction
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class MaterialsProductionCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
    
    def total_emissions_materialsprod(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_materialsprod = 0
        emissions_materialsprod =[]
        for source, data in self.ghg_database["materials_prod"].items():
            product = MaterialsProduction.materialprod_from_dict(data)
            
            total_emissions_materialsprod = total_emissions_materialsprod +\
                product.total_GHG_emissions(self.project_durations)
                
            emissions_materialsprod.append([data.material, data.process, \
                product.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_materialsprod, emissions_materialsprod]
    
    def phase_emissions_materialsprod(self):
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_materialsprod = 0
        operation_emissions_materialsprod = 0
        for source, data in self.ghg_database["materials_prod"].items():
            product = MaterialsProduction.materialprod_from_dict(data)
            
            if Phase[product.phase] == Phase.CONSTRUCTION:
                construction_emissions_materialsprod = construction_emissions_materialsprod +\
                    product.total_GHG_emissions(self.project_durations)
            elif Phase[product.phase] == Phase.OPERATION:
                operation_emissions_materialsprod = operation_emissions_materialsprod +\
                    product.total_GHG_emissions(self.project_durations)
            else:
                pass
        
        return [construction_emissions_materialsprod, operation_emissions_materialsprod]
    
    
    def total_emissions_peryear_materialsprod(self):
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
  
        for source, data in self.ghg_database["materials_prod"].items():
            product = MaterialsProduction.materialprod_from_dict(data)
            
            if Phase[product.phase] == Phase.CONSTRUCTION:
                emissions = product.quantity * product.ef
                
                emissions_peryear_construction += emissions
                
            elif Phase[product.phase] == Phase.OPERATION:
                emissions = product.quantity * product.ef
                
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


