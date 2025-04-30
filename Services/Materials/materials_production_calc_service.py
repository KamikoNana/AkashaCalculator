"""
This file contains the Service for the Materials Production emissions source. 
- Includes all calculations for the Materials Production class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math

import ghg_database

from Entity.Materials.materials_production_entity import MaterialsProduction
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase

class MaterialsProductionCalculations():
    def __init__(self):
        self
    
    def total_emissions_materialsprod():
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_materialsprod = 0
        emissions_materialsprod =[]
        for source, data in ghg_database.materials_prod.items():
            data = MaterialsProduction.materialprod_from_dict(data)
            
            total_emissions_materialsprod = total_emissions_materialsprod +\
                MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)
                
            emissions_materialsprod.append([data.material, data.process, \
                MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)])
        
        return [total_emissions_materialsprod, emissions_materialsprod]
    
    def phase_emissions_materialsprod():
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_materialsprod = 0
        operation_emissions_materialsprod = 0
        for source, data in ghg_database.materials_prod.items():
            data = MaterialsProduction.materialprod_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                construction_emissions_materialsprod = construction_emissions_materialsprod +\
                    MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)
            elif Phase[data.phase] == Phase.OPERATION:
                operation_emissions_materialsprod = operation_emissions_materialsprod +\
                    MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)
            else:
                pass
        
        return [construction_emissions_materialsprod, operation_emissions_materialsprod]
    
    
    def total_emissions_peryear_materialsprod():
        """
        Calculates the total commulative sum of GHG emissions for this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
  
        for source, data in ghg_database.materials_prod.items():
            data = MaterialsProduction.materialprod_from_dict(data)
            
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


