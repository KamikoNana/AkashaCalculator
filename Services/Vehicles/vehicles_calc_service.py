"""
This file contains the Service for the Vehicles emissions source. 
- Includes all calculations for the Vahicles class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math

import ghg_database

from Entity.Vehicles.vehicles_entity import Vehicles
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.Vehicles.vehicles_entity import VehiclesType

class VehiclesCalculations():
    def __init__(self):
        self
        
    def total_emissions_vehicles_all():
        """
        Calculates the total sum GHG emissions for ALL VEHICLES of this emissions source
        """
        total_emissions_vehicles = 0
        emissions_vehicles =[]
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            total_emissions_vehicles = total_emissions_vehicles + \
                Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            emissions_vehicles.append([data.vehicle, data.type, \
                Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_vehicles, emissions_vehicles]
    
    def total_emissions_vehicles_type(type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source
        """
        total_emissions_type = 0
        emissions_type =[]
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                total_emissions_type = total_emissions_type + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                emissions_type.append([data.vehicle, data.type, \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)])
        
        return [total_emissions_type, emissions_type]
    
    def phase_emissions_vehicles_all():
        """
        Calculates the total sum of GHG emissions for ALL VEHICLES of this emissions source for each project phase considered
        """
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                construction_emissions_vehicles = construction_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            elif Phase[data.phase] == Phase.OPERATION:
                operation_emissions_vehicles = operation_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.type, data.name, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
            else:
                pass
        return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def phase_emissions_vehicles_type(type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source for each project phase considered
        """
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                if Phase[data.phase] == Phase.CONSTRUCTION:
                    construction_emissions_vehicles = construction_emissions_vehicles + \
                    Vehicles.total_GHG_emissions(data.phase, data.km, data.n, \
                    data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                elif Phase[data.phase] == Phase.OPERATION:
                    operation_emissions_vehicles = operation_emissions_vehicles + \
                        Vehicles.total_GHG_emissions(data.phase, data.type, data.name, data.km, data.n, \
                        data.co2_emissions, data.ch4_emissions, data.ch4_cf, data.n2o_emissions, data.n2o_cf)
                else:
                    pass
                
            return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def total_emissions_peryear_vehicles_all():
        """
        Calculates the total commulative sum of GHG emissions for ALL VEHICLES of this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if Phase[data.phase] == Phase.CONSTRUCTION:
                total_fuel = data.km * data.n
                CO2_totalemissions = total_fuel * data.co2_emissions 
                CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(construction_duration):
                    total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
            elif Phase[data.phase] == Phase.OPERATION:
                total_fuel = data.km * data.n
                CO2_totalemissions = total_fuel * data.co2_emissions 
                CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                for i in range(operation_duration):
                    total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
            else:
                pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear
    
    def total_emissions_peryear_vehicles_type(type):
        """
        Calculates the total commulative sum of GHG emissions for EACH TYPE of this emissions source per year of the project horizon
        """
        project_duration = ProjectPhasesService.project_duration()
        construction_duration = math.ceil(project_duration[0])
        operation_duration = math.ceil(project_duration[1])
        full_duration = math.ceil(project_duration[2])
        
        total_emissions_peryear_construction = [0] * construction_duration
        total_emissions_peryear_operation = [0] * operation_duration
        
        for source, data in ghg_database.vehicles.items():
            data = Vehicles.vehicle_from_dict(data)
            
            if data.type == type:
                
                if Phase[data.phase] == Phase.CONSTRUCTION:
                    total_fuel = data.km * data.n
                    CO2_totalemissions = total_fuel * data.co2_emissions 
                    CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                    N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    for i in range(construction_duration):
                        total_emissions_peryear_construction[i] = total_emissions_peryear_construction[i] + emissions
                    
                elif Phase[data.phase] == Phase.OPERATION:
                    total_fuel = data.km * data.n
                    CO2_totalemissions = total_fuel * data.co2_emissions 
                    CH4_totalemissions = total_fuel * data.ch4_emissions * data.ch4_cf
                    N2O_totalemissions = total_fuel * data.n2o_emissions * data.n2o_cf
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    for i in range(operation_duration):
                        total_emissions_peryear_operation[i] = total_emissions_peryear_operation[i] + emissions
                else:
                    pass
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear