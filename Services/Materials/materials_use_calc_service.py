"""
This file contains the Service for the Materials Use emissions source. 
- Includes all calculations for the Materials Use class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import json

from Entity.Materials.materials_use_entity import MaterialsUse
from Entity.ProjectPhases.project_phases_entity import Phase

class MaterialsUseCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        
    def total_emissions_materialsuse(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_materialsuse = 0
        emissions_materialsuse =[]
        for source, data in self.ghg_database["materials_use"].items():
            use = MaterialsUse.materialsuse_from_dict(data)
            
            total_emissions_materialsuse = total_emissions_materialsuse + \
                use.total_GHG_emissions()
            emissions_materialsuse.append([use.material, \
                use.total_GHG_emissions()])
        
        return [total_emissions_materialsuse, emissions_materialsuse]
    
    def phase_emissions_materialsuse(self):
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_materialsuse = 0
        operation_emissions_materialsuse = 0
        for source, data in self.ghg_database["materials_use"].items():
            use = MaterialsUse.materialsuse_from_dict(data)
            
            if Phase[use.phase] == Phase.CONSTRUCTION:
                construction_emissions_materialsuse = construction_emissions_materialsuse + \
                    MaterialsUse.total_GHG_emissions(use.phase, use.material, use.quantity, use.ef)
                    
            elif Phase[use.phase] == Phase.OPERATION:
                operation_emissions_materialsuse = operation_emissions_materialsuse + \
                    MaterialsUse.total_GHG_emissions(use.phase, use.material, use.quantity, use.ef)
            else:
                pass
        
        return [construction_emissions_materialsuse, operation_emissions_materialsuse]