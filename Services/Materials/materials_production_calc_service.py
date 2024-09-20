import ghg_database

from Entity.Materials.materials_production_entity import MaterialsProduction
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class MaterialsProductionCalculations():
    def __init__(self):
        self
    
    def total_emissions_materialsprod():
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
        construction_emissions_materialsprod = 0
        operation_emissions_materialsprod = 0
        for source, data in ghg_database.materials_prod.items():
            data = MaterialsProduction.materialprod_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                construction_emissions_materialsprod = construction_emissions_materialsprod +\
                    MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)
            elif data.phase == "OPERATION":
                operation_emissions_materialsprod = operation_emissions_materialsprod +\
                    MaterialsProduction.total_GHG_emissions(data.phase, data.quantity, data.ef)
            else:
                pass
        
        return [construction_emissions_materialsprod, operation_emissions_materialsprod]
    
    
    def total_emissions_peryear_materialsprod():
        project_duration = ProjectPhasesService.project_duration()
        
        total_emissions_peryear_construction = [0] * project_duration[0]
        total_emissions_peryear_operation = [0] * project_duration[1]
  
        for source, data in ghg_database.materials_prod.items():
            data = MaterialsProduction.materialprod_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                emissions = data.quantity * data.ef
                for i in range(project_duration[0]):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
            elif data.phase == "OPERATION":
                emissions = data.quantity * data.ef
                for i in range(project_duration[1]):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, project_duration[2]):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear


