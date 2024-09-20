import ghg_database

from Entity.Combustion.mobile_comb_entity import MobileCombustion
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class MobileCombustionCalculations():
    def __init__(self):
        self
        
    def total_emissions_mobilecomb():
        total_emissions_mobilecomb = 0
        emissions_mobilecomb =[]
        for source, data in ghg_database.mobile_combustion.items():
            data = MobileCombustion.mobilecomb_from_dict(data)
            
            total_emissions_mobilecomb = total_emissions_mobilecomb + \
                MobileCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            emissions_mobilecomb.append([data.enginery_fueltype, data.n, \
                MobileCombustion.total_GHG_emissions(data.phase, data.quantity, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_mobilecomb, emissions_mobilecomb]
    
    def phase_emissions_mobilecomb():
        construction_emissions_mobilecomb = 0
        operation_emissions_mobilecomb = 0
        for source, data in ghg_database.mobile_combustion.items():
            data = MobileCombustion.mobilecomb_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                construction_emissions_mobilecomb = construction_emissions_mobilecomb + \
                    MobileCombustion.total_GHG_emissions(data.phase, data.quantity,\
                    data.n, data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            elif data.phase == "OPERATION":
                operation_emissions_mobilecomb = operation_emissions_mobilecomb + \
                    MobileCombustion.total_GHG_emissions(data.phase, data.quantity,\
                    data.n, data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            else:
                pass
        
        return [construction_emissions_mobilecomb, operation_emissions_mobilecomb]
    

    
    def total_emissions_peryear_mobilecomb():
        project_duration = ProjectPhasesService.project_duration()
        
        total_emissions_peryear_construction = [0] * project_duration[0]
        total_emissions_peryear_operation = [0] * project_duration[1]
  
        for source, data in ghg_database.mobile_combustion.items():
            data = MobileCombustion.mobilecomb_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                total_fuel = data.quantity * data.n
                CO2_totalemissions = total_fuel * data.co2_emissions 
                CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                for i in range(project_duration[0]):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
            elif data.phase == "OPERATION":
                total_fuel = data.quantity * data.n
                CO2_totalemissions = total_fuel * data.co2_emissions 
                CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                for i in range(project_duration[1]):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, project_duration[2]):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear