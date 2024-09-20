## Waste treatment
# (treatment, quantity, CO2emissons, CH4emissions, N2Oemissions)
from Services.ProjectPhases.project_phases_service import ProjectPhasesService

class WasteTreatment:
    def __init__(self, phase, treatment, stream, quantity, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        self.phase = phase                          #project phase
        self.treatment = treatment                  #treatment type (str)
        self.stream = stream                        #used to gategorize the stream: SOIL/WATER/GAS
        self.quantity = quantity                    #quantity of treated materials per year [L/year] (float)
        self.co2_emissions = co2_emissions            #emissions of the fuel use [kgCO2/L] (float)
        self.ch4_emissions = ch4_emissions            #emissions of the fuel use [kgCH4/km] (float)
        self.ch4_cf = ch4_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)                          
        self.n2o_emissions = n2o_emissions            #emissions of the fuel use [kgN2O/km] (float)
        self.n2o_cf = n2o_cf                        #conversion factor of CH4 to CO2eq [adimensional] (float)
    
    def total_GHG_emissions(phase, quantity, co2_emissions, ch4_emissions, ch4_cf, n2o_emissions, n2o_cf):
        CO2_totalemissions = quantity * co2_emissions 
        CH4_totalemissions = quantity * ch4_emissions * ch4_cf
        N2O_totalemissions = quantity * n2o_emissions * n2o_cf
        total_emissions = CO2_totalemissions + CH4_totalemissions + N2O_totalemissions
        
        if phase == "CONSTRUCTION":
            return total_emissions * ProjectPhasesService.project_duration()[0]
        elif phase == "OPERATION":
            return total_emissions * ProjectPhasesService.project_duration()[1]
    
    def to_dict(self):
        return {"phase": self.phase, "treatment": self.treatment, "stream": self.stream, "quantity": self.quantity, \
            "co2_emissions": self.co2_emissions, "ch4_emissions": self.ch4_emissions, \
                "ch4_cf": self.ch4_cf, "n2o_emissions": self.n2o_emissions, "n2o_cf": self.n2o_cf}
    
    @staticmethod    
    def waste_from_dict(dict):
        return WasteTreatment(dict["phase"], dict["treatment"], dict["stream"], \
            dict["quantity"], dict["co2_emissions"], dict["ch4_emissions"], dict["ch4_cf"]\
                , dict["n2o_emissions"], dict["n2o_cf"])