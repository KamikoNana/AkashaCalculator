import ghg_database

from Entity.Vehicles.vehicles_entity import Vehicles
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class VehiclesCalculations():
    def __init__(self):
        self
        
    def total_emissions_vehicles_all():
        total_emissions_vehicles = 0
        emissions_vehicles =[]
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            total_emissions_vehicles = total_emissions_vehicles + \
                Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            emissions_vehicles.append([data.vehicle_fuel, data.type, \
                Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_vehicles, emissions_vehicles]
    
    def total_emissions_vehicles_type(type):
        total_emissions_type = 0
        emissions_type =[]
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                total_emissions_type = total_emissions_type + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                emissions_type.append([data.vehicle_fuel, data.type, \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_type, emissions_type]
    
    def phase_emissions_vehicles_all():
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                construction_emissions_vehicles = construction_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            elif data.phase == "OPERATION":
                operation_emissions_vehicles = operation_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.type, data.name, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            else:
                pass
        return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def phase_emissions_vehicles_type(type):
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                if data.phase == "CONSTRUCTION":
                    construction_emissions_vehicles = construction_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                elif data.phase == "OPERATION":
                    operation_emissions_vehicles = operation_emissions_vehicles + \
                        Vehicles.total_GHG_emissions(data.phase, data.type, data.name, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                else:
                    pass
                
            return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def total_emissions_peryear_vehicles_all():
        project_duration = ProjectPhasesService.project_duration()
        
        total_emissions_peryear_construction = [0] * project_duration[0]
        total_emissions_peryear_operation = [0] * project_duration[1]
        
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.phase == "CONSTRUCTION":
                total_fuel = data.km * data.n
                CO2_totalemissions = total_fuel * data.co2_emissions 
                CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(project_duration[0]):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
            elif data.phase == "OPERATION":
                total_fuel = data.km * data.n
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
    
    def total_emissions_peryear_vehicles_type(type):
        project_duration = ProjectPhasesService.project_duration()
        
        total_emissions_peryear_construction = [0] * project_duration[0]
        total_emissions_peryear_operation = [0] * project_duration[1]
        
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                
                if data.phase == "CONSTRUCTION":
                    total_fuel = data.km * data.n
                    CO2_totalemissions = total_fuel * data.co2_emissions 
                    CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                    N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    for i in range(project_duration[0]):
                        total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
                elif data.phase == "OPERATION":
                    total_fuel = data.km * data.n
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