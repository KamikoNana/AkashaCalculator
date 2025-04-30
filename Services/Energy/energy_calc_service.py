"""
This file contains the Service for the Energy emissions source. 
- Includes all calculations for the Energy class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math

import ghg_database

from Entity.Energy.energy_entity import Energy
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.Energy.energy_entity import EnergyType

class EnergyCalculations():
    def __init__(self):
        self
    
    def total_emissions_energy():
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
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
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_energy = 0
        operation_emissions_energy = 0
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                construction_emissions_energy = construction_emissions_energy + \
                    Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
            
            elif Phase[data.phase] == Phase.OPERATION:
                operation_emissions_energy = operation_emissions_energy + \
                    Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
            else:
                pass
        
        return [construction_emissions_energy, operation_emissions_energy]
    
    def GHG_emissions_saved_energy():
        """
        Calculates the total balance of GHG emissions between the energy consumed and energy produced
        - Calculated the total balance (total consumed - total produced)
            - If this value is NEGATIVE indicates that the energy produced colmates the energy consumed emissions for the project
        - Provides outputs on the estimate optimization for each produced energy
        """
        energy = 0
        total_consumed = 0
        mean_consumed = 0
        n_consumed = 0
        total_produced = 0
        total_balance = 0
        balance = []
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if EnergyType[data.type] == EnergyType.CONSUMED:
                total_consumed = total_consumed + Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                n_consumed = n_consumed + 1
                mean_consumed = total_consumed / n_consumed
                
            if EnergyType[data.type] == EnergyType.PRODUCED:
                total_produced = total_produced + Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                
            else:
                pass
            
            total_balance = total_consumed - total_produced
        
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
            if EnergyType[data.type] == EnergyType.PRODUCED:
                energy = Energy.total_GHG_emissions(data.phase, data.quantity, data.ef)
                balance.append([data.source, mean_consumed - energy])
                
            else:
                pass
    
        return [total_balance, balance]
    
    def total_emissions_peryear_energy():
        """
        Calculates the total commulative sum of GHG emissions for this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
  
        for source, data in ghg_database.energy.items():
            data = Energy.energy_from_dict(data)
            
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


