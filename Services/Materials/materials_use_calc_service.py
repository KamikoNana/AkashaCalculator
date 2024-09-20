import ghg_database

from Entity.Materials.materials_use_entity import MaterialsUse
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class MaterialsUseCalculations():
    def __init__(self):
        self
        
    def total_emissions_materialsuse():
        total_emissions_materialsuse = 0
        emissions_materialsuse =[]
        for source, data in ghg_database.materials_use.items():
            data = MaterialsUse.materialsuse_from_dict(data)
            
            total_emissions_materialsuse = total_emissions_materialsuse + \
                MaterialsUse.total_GHG_emissions(data.phase, data.material, data.quantity, data.ef)
            emissions_materialsuse.append([data.material, \
                MaterialsUse.total_GHG_emissions(data.phase, data.material, \
                data.quantity, data.ef)])
        
        return [total_emissions_materialsuse, emissions_materialsuse]
    
    def phase_emissions_materialsuse():
        construction_emissions_materialsuse = 0
        operation_emissions_materialsuse = 0
        for source, data in ghg_database.materials_use.items():
            data = MaterialsUse.materialsuse_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                construction_emissions_materialsuse = construction_emissions_materialsuse + \
                    MaterialsUse.total_GHG_emissions(data.phase, data.material, data.quantity, data.ef)
                    
            elif data.phase == "OPERATION":
                operation_emissions_materialsuse = operation_emissions_materialsuse + \
                    MaterialsUse.total_GHG_emissions(data.phase, data.material, data.quantity, data.ef)
            else:
                pass
        
        return [construction_emissions_materialsuse, operation_emissions_materialsuse]