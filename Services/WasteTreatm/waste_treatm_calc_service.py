"""
This file contains the Service for the Waste Treatment emissions source. 
- Includes all calculations for the Waste Treatment class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.WasteTreatm.waste_treatm_entity import WasteTreatment
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.WasteTreatm.waste_treatm_entity import WasteType

class WasteTreatmentCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
        
    def total_emissions_waste_all(self):
        """
        Calculates the total sum GHG emissions for ALL WASTE of this emissions source
        """
        total_emissions_waste = 0
        emissions_waste =[]
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            total_emissions_waste = total_emissions_waste + \
                waste.total_GHG_emissions(self.project_durations)
            emissions_waste.append([waste.treatment, waste.stream, \
                waste.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_waste, emissions_waste]
    
    def total_emissions_waste_type(self, type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source
        """
        total_emissions_waste = 0
        emissions_waste =[]
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            if waste.stream == type:
                
                total_emissions_waste = total_emissions_waste + \
                waste.total_GHG_emissions(self.project_durations)
                emissions_waste.append([waste.treatment, waste.stream, \
                waste.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_waste, emissions_waste]
    
    def phase_emissions_waste_all(self):
        """
        Calculates the total sum of GHG emissions for ALL WASTE of this emissions source for each project phase considered
        """
        construction_emissions_waste = 0
        operation_emissions_waste = 0
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            if Phase[waste.phase] == Phase.CONSTRUCTION:
                construction_emissions_waste = construction_emissions_waste +\
                    waste.total_GHG_emissions(self.project_durations)
            elif Phase[waste.phase] == Phase.OPERATION:
                operation_emissions_waste = operation_emissions_waste + \
                    waste.total_GHG_emissions(self.project_durations)
            else:
                pass
            
        return [construction_emissions_waste, operation_emissions_waste]
    
    def phase_emissions_waste_type(self, type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source for each project phase considered
        """
        construction_emissions_waste = 0
        operation_emissions_waste = 0
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            if waste.type == type:
                
                if waste.phase == Phase.CONSTRUCTION:
                    construction_emissions_waste = construction_emissions_waste +\
                    waste.total_GHG_emissions(self.project_durations)
                elif waste.phase == Phase.OPERATION:
                    operation_emissions_waste = operation_emissions_waste + \
                    waste.total_GHG_emissions(self.project_durations)
                else:
                    pass
                
        return [construction_emissions_waste, operation_emissions_waste]
    
    def total_emissions_peryear_waste_all(self):
        """
        Calculates the total commulative sum of GHG emissions for ALL WASTE of this emissions source per year of the project horizon
        """
        construction_duration = math.ceil(self.project_durations[0])
        operation_duration = math.ceil(self.project_durations[1])
        full_duration = math.ceil(self.project_durations[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            if Phase[waste.phase] == Phase.CONSTRUCTION:
                CO2_totalemissions = waste.quantity * waste.co2_emissions 
                CH4_totalemissions = waste.quantity * waste.ch4_emissions * waste.ch4_cf
                N2O_totalemissions = waste.quantity * waste.n2o_emissions * waste.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(construction_duration):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
            elif Phase[waste.phase] == Phase.OPERATION:
                CO2_totalemissions = waste.quantity * waste.co2_emissions 
                CH4_totalemissions = waste.quantity * waste.ch4_emissions * waste.ch4_cf
                N2O_totalemissions = waste.quantity * waste.n2o_emissions * waste.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(operation_duration):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear
    
    def total_emissions_peryear_waste_type(self, type):
        """
        Calculates the total commulative sum of GHG emissions for EACH TYPE of this emissions source per year of the project horizon
        """
        construction_duration = math.ceil(self.project_durations[0])
        operation_duration = math.ceil(self.project_durations[1])
        full_duration = math.ceil(self.project_durations[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in self.ghg_database["waste_treatm"].items():
            waste = WasteTreatment.waste_from_dict(data)
            
            if waste.stream == type:
                
                if Phase[waste.phase] == Phase.CONSTRUCTION:
                    CO2_totalemissions = waste.quantity * waste.co2_emissions 
                    CH4_totalemissions = waste.quantity * waste.ch4_emissions * waste.ch4_cf
                    N2O_totalemissions = waste.quantity * waste.n2o_emissions * waste.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                    for i in range(construction_duration):
                        total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
                elif Phase[waste.phase] == Phase.OPERATION:
                    CO2_totalemissions = waste.quantity * waste.co2_emissions 
                    CH4_totalemissions = waste.quantity * waste.ch4_emissions * waste.ch4_cf
                    N2O_totalemissions = waste.quantity * waste.n2o_emissions * waste.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    for i in range(operation_duration):
                        total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
                
                else:
                    pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear