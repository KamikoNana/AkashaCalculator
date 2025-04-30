"""
This file contains the Service for the Waste Treatment emissions source. 
- Includes all calculations for the Waste Treatment class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math

import ghg_database

from Entity.WasteTreatm.waste_treatm_entity import WasteTreatment
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.WasteTreatm.waste_treatm_entity import WasteType

class WasteTreatmentCalculations():
    def __init__(self):
        self
        
    def total_emissions_waste_all():
        """
        Calculates the total sum GHG emissions for ALL WASTE of this emissions source
        """
        total_emissions_waste = 0
        emissions_waste =[]
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            total_emissions_waste = total_emissions_waste + \
                WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            emissions_waste.append([data.treatment, data.stream, \
                WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_waste, emissions_waste]
    
    def total_emissions_waste_type(type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source
        """
        total_emissions_waste = 0
        emissions_waste =[]
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            if data.stream == type:
                
                total_emissions_waste = total_emissions_waste + \
                WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                emissions_waste.append([data.treatment, data.stream, \
                WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_waste, emissions_waste]
    
    def phase_emissions_waste_all():
        """
        Calculates the total sum of GHG emissions for ALL WASTE of this emissions source for each project phase considered
        """
        construction_emissions_waste = 0
        operation_emissions_waste = 0
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                construction_emissions_waste = construction_emissions_waste +\
                    WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            elif Phase[data.phase] == Phase.OPERATION:
                operation_emissions_waste = operation_emissions_waste + \
                    WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            else:
                pass
            
        return [construction_emissions_waste, operation_emissions_waste]
    
    def phase_emissions_waste_type(type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source for each project phase considered
        """
        construction_emissions_waste = 0
        operation_emissions_waste = 0
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            if data.type == type:
                
                if data.phase == Phase.CONSTRUCTION:
                    construction_emissions_waste = construction_emissions_waste +\
                    WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                elif data.phase == Phase.OPERATION:
                    operation_emissions_waste = operation_emissions_waste + \
                    WasteTreatment.total_GHG_emissions(data.phase, data.quantity, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                else:
                    pass
                
        return [construction_emissions_waste, operation_emissions_waste]
    
    def total_emissions_peryear_waste_all():
        """
        Calculates the total commulative sum of GHG emissions for ALL WASTE of this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                CO2_totalemissions = data.quantity * data.co2_emissions 
                CH4_totalemissions = data.quantity * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = data.quantity * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(construction_duration):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
            elif Phase[data.phase] == Phase.OPERATION:
                CO2_totalemissions = data.quantity * data.co2_emissions 
                CH4_totalemissions = data.quantity * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = data.quantity * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(operation_duration):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear
    
    def total_emissions_peryear_waste_type(type):
        """
        Calculates the total commulative sum of GHG emissions for EACH TYPE of this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in ghg_database.waste_treatm.items():
            data = WasteTreatment.waste_from_dict(data)
            
            if data.stream == type:
                
                if Phase[data.phase] == Phase.CONSTRUCTION:
                    CO2_totalemissions = data.quantity * data.co2_emissions 
                    CH4_totalemissions = data.quantity * data.ch4_emissions * data.ch4_cf
                    N2O_totalemissions = data.quantity * data.n2o_emissions * data.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                    for i in range(construction_duration):
                        total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
                elif Phase[data.phase] == Phase.OPERATION:
                    CO2_totalemissions = data.quantity * data.co2_emissions 
                    CH4_totalemissions = data.quantity * data.ch4_emissions * data.ch4_cf
                    N2O_totalemissions = data.quantity * data.n2o_emissions * data.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    for i in range(operation_duration):
                        total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
                
                else:
                    pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear