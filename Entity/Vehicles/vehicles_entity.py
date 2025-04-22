"""
This file contains the Entity for the Vehicles emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class Vehicles:
    def __init__(self, phase, type, vehicle_fuel, km, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        self.phase = phase                          #project phase
        self.type = type                            #type of vehicle: ROAD/TRAIN/SHIP/AIR
        self.vehicle_fuel = vehicle_fuel                 #vehicle type - fuel type (str)
        self.km = km                                #km/year each vehicle makes [km/year] (float)
        self.n = n                                  #number of vehicles in total (int)
        self.co2_emissions = co2_emissions            #emissions of the fuel use [kgCO2/km] (float)
        self.ch4_emissions = ch4_emissions            #emissions of the fuel use [kgCH4/km] (float)
        self.ch4_cf = ch4_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)                          
        self.n2o_emissions = n2o_emissions            #emissions of the fuel use [kgN2O/km] (float)
        self.n2o_cf = n2o_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)

    def total_GHG_emissions(phase, km, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        total_distance = km * n
        CO2_totalemissions = total_distance * co2_emissions 
        CH4_totalemissions = total_distance * ch4_emissions * ch4_cf
        N2O_totalemissions = total_distance * n2o_emissions * n2o_cf
        total_emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
        
        if phase == "CONSTRUCTION":
            duration = float(ProjectPhasesService.project_duration()[0])
            return total_emissions * duration
        elif phase == "OPERATION":
            duration = float(ProjectPhasesService.project_duration()[1])
            return total_emissions * duration
    
    def to_dict(self):
        return {"phase": self.phase, "type": self.type, "vehicle_fuel": self.vehicle_fuel, "distance": self.km, \
            "n_vehicles": self.n, "co2_emissions": self.co2_emissions, "ch4_emissions": self.ch4_emissions, \
                "ch4_cf": self.ch4_cf, "n2o_emissions": self.n2o_emissions, "n2o_cf": self.n2o_cf}
    
    @staticmethod
    def vehicle_from_dict(dict):
        return Vehicles(dict["phase"], dict["type"], dict["vehicle_fuel"], dict["distance"], dict["n_vehicles"], \
            dict["co2_emissions"], dict["ch4_emissions"], dict["ch4_cf"], dict["n2o_emissions"], dict["n2o_cf"])