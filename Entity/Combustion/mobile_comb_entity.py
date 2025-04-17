## Mobile combustion enginery
# (enginery_fueltype, fuelquant, number, CO2emissons, CH4emissions, N2Oemissions)

from Services.ProjectPhases.project_phases_service import ProjectPhasesService
from Entity.Combustion.combustion_eng_entity import CombustionEnginery


class MobileCombustion(CombustionEnginery):
    def __init__(self, phase, enginery_fueltype, quantity, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        super().__init__(phase, enginery_fueltype, quantity, n)
        self.co2_emissions = co2_emissions            #emissions of the fuel use [tonCO2/L] (float)
        self.ch4_emissions = ch4_emissions            #emissions of the fuel use [tonCH4/km] (float)
        self.ch4_cf = ch4_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)                          
        self.n2o_emissions = n2o_emissions            #emissions of the fuel use [tonN2O/km] (float)
        self.n2o_cf = n2o_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)
        
    def total_GHG_emissions(phase, quantity, n, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        total_fuel = quantity * n
        CO2_totalemissions = total_fuel * co2_emissions 
        CH4_totalemissions = total_fuel * ch4_emissions * ch4_cf
        N2O_totalemissions = total_fuel * n2o_emissions * n2o_cf
        total_emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
        
        if phase == "CONSTRUCTION":
            duration = float(ProjectPhasesService.project_duration()[0])
            return total_emissions * duration
        elif phase == "OPERATION":
            duration = float(ProjectPhasesService.project_duration()[1])
            return total_emissions * duration
    
    def to_dict(self):
        return {"phase": self.phase, "enginery_fueltype": self.enginery_fueltype, "quantity": self.quantity, \
            "n_machines": self.n, "co2_emissions": self.co2_emissions, "ch4_emissions": self.ch4_emissions, \
                "ch4_cf": self.ch4_cf, "n2o_emissions": self.n2o_emissions, "n2o_cf": self.n2o_cf}
    
    @staticmethod    
    def mobilecomb_from_dict(dict):
        return MobileCombustion(dict["phase"], dict["enginery_fueltype"], \
            dict["quantity"], dict["n_machines"], dict["co2_emissions"], dict["ch4_emissions"], dict["ch4_cf"]\
                , dict["n2o_emissions"], dict["n2o_cf"])