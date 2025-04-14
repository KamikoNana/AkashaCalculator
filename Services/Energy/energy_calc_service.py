import ghg_database

from Entity.Energy.energy_entity import Energy
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class EnergyCalculations():
    def __init__(self):
        self
    
    def total_emissions_energy():
        total_emissions_energy = 0
        emissions_energy =[]
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            total_emissions_energy = total_emissions_energy +\
                Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                
            emissions_energy.append([data.source, data.type, \
                Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)])
        
        return [total_emissions_energy, emissions_energy]
            
    def phase_emissions_energy():
        construction_emissions_energy = 0
        operation_emissions_energy = 0
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                construction_emissions_energy = construction_emissions_energy + \
                    Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
            
            elif data.phase == "OPERATION":
                operation_emissions_energy = operation_emissions_energy + \
                    Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
            else:
                pass
        
        return [construction_emissions_energy, operation_emissions_energy]
    
    def GHG_emissions_saved_energy():
        energy = 0
        total_consumed = 0
        n_consumed = 0
        total_balance = 0
        balance = []
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if data.type == "CONSUMED":
                total_consumed = total_consumed + Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                n_consumed = n_consumed + 1
            consumed = total_consumed/n_consumed
        
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if data.type == "PRODUCED":
                energy = Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                total_balance = total_balance + (consumed-energy)
                balance.append([data.source, consumed-energy])
            else:
                pass
    
        return [total_balance, balance]
    
    def total_emissions_peryear_energy():
        project_duration = ProjectPhasesService.project_duration()
        
        total_emissions_peryear_construction = [0] * project_duration[0]
        total_emissions_peryear_operation = [0] * project_duration[1]
  
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
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


