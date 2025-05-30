"""
This file contains the Service for the Vehicles emissions source. 
- Includes all calculations for the Vahicles class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import math
import json

from Entity.Vehicles.vehicles_entity import Vehicles
from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.ProjectPhases.project_phases_entity import Phase
from Entity.Vehicles.vehicles_entity import VehiclesType

class VehiclesCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        self.project_durations = ProjectPhasesService(self.ghg_database).project_duration()
        
    def total_emissions_vehicles_all(self):
        """
        Calculates the total sum GHG emissions for ALL VEHICLES of this emissions source
        """
        total_emissions_vehicles = 0
        emissions_vehicles =[]
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            total_emissions_vehicles = total_emissions_vehicles + \
                vehicle.total_GHG_emissions(self.project_durations)
            emissions_vehicles.append([vehicle.vehicle, vehicle.type, \
                vehicle.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_vehicles, emissions_vehicles]
    
    def total_emissions_vehicles_type(self, type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source
        """
        total_emissions_type = 0
        emissions_type =[]
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            if vehicle.type == type:
                total_emissions_type = total_emissions_type + \
                    vehicle.total_GHG_emissions(self.project_durations)
                emissions_type.append([vehicle.vehicle, vehicle.type, \
                    vehicle.total_GHG_emissions(self.project_durations)])
        
        return [total_emissions_type, emissions_type]
    
    def phase_emissions_vehicles_all(self):
        """
        Calculates the total sum of GHG emissions for ALL VEHICLES of this emissions source for each project phase considered
        """
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            if Phase[vehicle.phase] == Phase.CONSTRUCTION:
                construction_emissions_vehicles = construction_emissions_vehicles + \
                    vehicle.total_GHG_emissions(self.project_durations)
            elif Phase[vehicle.phase] == Phase.OPERATION:
                operation_emissions_vehicles = operation_emissions_vehicles + \
                    vehicle.total_GHG_emissions(self.project_durations)
            else:
                pass
        return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def phase_emissions_vehicles_type(self, type):
        """
        Calculates the total sum of GHG emissions for EACH TYPE of this emissions source for each project phase considered
        """
        construction_emissions_vehicles = 0
        operation_emissions_vehicles = 0
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            if vehicle.type == type:
                if Phase[vehicle.phase] == Phase.CONSTRUCTION:
                    construction_emissions_vehicles = construction_emissions_vehicles + \
                    vehicle.total_GHG_emissions(self.project_durations)
                elif Phase[vehicle.phase] == Phase.OPERATION:
                    operation_emissions_vehicles = operation_emissions_vehicles + \
                        vehicle.total_GHG_emissions(self.project_durations)
                else:
                    pass
                
            return [construction_emissions_vehicles, operation_emissions_vehicles]
    
    def total_emissions_peryear_vehicles_all(self):
        """
        Calculates the total commulative sum of GHG emissions for ALL VEHICLES of this emissions source per year of the project horizon
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
        
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            if Phase[vehicle.phase] == Phase.CONSTRUCTION:
                total_distance = vehicle.km * vehicle.n
                CO2_totalemissions = vehicle.co2_emissions * total_distance
                CH4_totalemissions = vehicle.ch4_emissions * vehicle.ch4_cf * total_distance
                N2O_totalemissions = vehicle.n2o_emissions * vehicle.n2o_cf * total_distance
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                emissions_peryear_construction += emissions
                    
            elif Phase[vehicle.phase] == Phase.OPERATION:
                total_distance = vehicle.km * vehicle.n
                CO2_totalemissions = vehicle.co2_emissions * total_distance
                CH4_totalemissions = vehicle.ch4_emissions * vehicle.ch4_cf * total_distance
                N2O_totalemissions = vehicle.n2o_emissions * vehicle.n2o_cf * total_distance
                emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                
                emissions_peryear_operation += emissions
                
            else:
                pass
            
        for i in range (construction_duration):
            total_emissions_peryear_construction[i] = emissions_peryear_construction
        for i in range (operation_duration):
            total_emissions_peryear_operation[i] = emissions_peryear_operation
        
        if rem_construction != 0:
            total_emissions_peryear_construction[-1] = (rem_construction * emissions_peryear_construction) + ( (1-rem_construction) * emissions_peryear_operation)
        if rem_operation != 0:
            total_emissions_peryear_operation[-1] = (rem_operation * emissions_peryear_operation) 
        if (rem_construction + rem_operation) > 1:
            total_emissions_peryear_operation[-1] = ((rem_construction + rem_operation) - 1) * emissions_peryear_operation 
        
        total_emissions_peryear = total_emissions_peryear_construction + total_emissions_peryear_operation
        
        for i in range(1, full_duration):
            total_emissions_peryear[i] = total_emissions_peryear[i] + total_emissions_peryear[i-1]
        
        return total_emissions_peryear
    
    def total_emissions_peryear_vehicles_type(self, type):
        """
        Calculates the total commulative sum of GHG emissions for EACH TYPE of this emissions source per year of the project horizon
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
        
        for source, data in self.ghg_database["vehicles"].items():
            vehicle = Vehicles.vehicle_from_dict(data)
            
            if vehicle.type == type:
                
                if Phase[vehicle.phase] == Phase.CONSTRUCTION:
                    total_distance = vehicle.km * vehicle.n
                    CO2_totalemissions = vehicle.co2_emissions * total_distance
                    CH4_totalemissions = vehicle.ch4_emissions * vehicle.ch4_cf * total_distance
                    N2O_totalemissions = vehicle.n2o_emissions * vehicle.n2o_cf * total_distance
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
                    emissions_peryear_construction += emissions
                    
                elif Phase[vehicle.phase] == Phase.OPERATION:
                    total_distance = vehicle.km * vehicle.n
                    CO2_totalemissions = vehicle.co2_emissions * total_distance
                    CH4_totalemissions = vehicle.ch4_emissions * vehicle.ch4_cf * total_distance
                    N2O_totalemissions = vehicle.n2o_emissions * vehicle.n2o_cf * total_distance
                    emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
                    
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