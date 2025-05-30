"""
This file contains the Service for the Energy emissions source.  
- Includes all calculations for the Energy class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.Energy.energy_entity import Energy
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.Energy.energy_entity import EnergyType

class EnergyCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
    
    def total_emissions_energy(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        """
        total_emissions_energy = 0
        emissions_energy =[]
        for source, data in self.ghg_database["energy"].items():
            energy = Energy.energy_from_dict(data)
            
            total_emissions_energy = total_emissions_energy +\
                energy.total_GHG_emissions(self.project_durations)
                
            emissions_energy.append([energy.source, energy.type, \
                energy.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_energy, emissions_energy]
            
    def phase_emissions_energy(self):
        """
        Calculates the total sum of GHG emissions for this emissions source for each project phase considered
        """
        construction_emissions_energy = 0
        operation_emissions_energy = 0
        for source, data in self.ghg_database["energy"].items():
            energy = Energy.energy_from_dict(data)
            
            if Phase[energy.phase] == Phase.CONSTRUCTION:
                construction_emissions_energy = construction_emissions_energy + \
                    energy.total_GHG_emissions(self.project_durations)
            
            elif Phase[energy.phase] == Phase.OPERATION:
                operation_emissions_energy = operation_emissions_energy + \
                    energy.total_GHG_emissions(self.project_durations)
            else:
                pass
        
        return [construction_emissions_energy, operation_emissions_energy]
    
    def GHG_emissions_saved_energy(self):
        """
        Calculates the total balance of GHG emissions between the energy consumed and energy produced
        - Calculated the total balance (total consumed - total produced)
            - If this value is NEGATIVE indicates that the energy produced colmates the energy consumed emissions for the project
        - Provides outputs on the estimate optimization for each produced energy
        """
        final_energy = 0
        total_consumed = 0
        quantity_consumed = 0
        mean_consumed = 0
        n_consumed = 0
        total_produced = 0
        quantity_produced = 0
        mean_produced = 0
        n_produced = 0
        total_balance = 0
        balance = []
        quantity_balance = 0
        for source, data in self.ghg_database["energy"].items():
            energy = Energy.energy_from_dict(data)
            
            if EnergyType[energy.type] == EnergyType.CONSUMED:
                quantity_consumed = quantity_consumed + energy.quantity
                
                total_consumed = total_consumed + energy.total_GHG_emissions(self.project_durations)
                
                n_consumed = n_consumed + 1
                mean_consumed = total_consumed / n_consumed
                
            if EnergyType[energy.type] == EnergyType.PRODUCED:
                quantity_produced = quantity_produced + energy.quantity
                
                total_produced = total_produced + energy.total_GHG_emissions(self.project_durations)
                
                n_produced = n_produced + 1
                mean_produced = total_produced / n_produced
                
            else:
                pass
            
            quantity_balance = quantity_consumed - quantity_produced
            total_balance = (mean_consumed * quantity_consumed) - (mean_produced * quantity_produced)
        
        for source, data in self.ghg_database["energy"].items():
            energy = Energy.energy_from_dict(data)
            
            if EnergyType[energy.type] == EnergyType.PRODUCED:
                final_energy = energy.total_GHG_emissions(self.project_durations)
                balance.append([energy.source, mean_consumed - final_energy])
                
            else:
                pass
    
        return [total_balance, quantity_balance, balance]
    
    def total_emissions_peryear_energy(self):
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
  
        for source, data in self.ghg_database["energy"].items():
            energy = Energy.energy_from_dict(data)
            
            if Phase[energy.phase] == Phase.CONSTRUCTION:
                emissions = energy.quantity * energy.ef
                
                emissions_peryear_construction += emissions
                
            elif Phase[energy.phase] == Phase.OPERATION:
                emissions = energy.quantity * energy.ef
                
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


