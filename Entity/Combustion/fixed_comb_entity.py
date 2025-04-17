## Fixed combustion enginery
# (enginery_fueltype, fuelquant, number, ef)

from Entity.Combustion.combustion_eng_entity import CombustionEnginery
from Services.ProjectPhases.project_phases_service import ProjectPhasesService



class FixedCombustion(CombustionEnginery):
    def __init__(self, phase, enginery_fueltype, quantity, n, ef):
        super().__init__(phase, enginery_fueltype, quantity, n)
        self.ef = ef                                #emission factor [tCO2/L] (float)1q
        
    def total_GHG_emissions(phase, quantity, n, ef):
        total_fuel = quantity * n
        
        if phase == "CONSTRUCTION":
            duration = float(ProjectPhasesService.project_duration()[0])
            return total_fuel * ef * duration
        elif phase == "OPERATION":
            duration = float(ProjectPhasesService.project_duration()[1])
            return total_fuel * ef * duration
        
    
    def to_dict(self):
        return {"phase": self.phase, "enginery_fueltype": self.enginery_fueltype, "quantity": self.quantity, \
            "n_machines": self.n, "ef": self.ef}
    
    @staticmethod
    def fixedcomb_from_dict(dict):
        return FixedCombustion(dict["phase"], dict["enginery_fueltype"], dict["quantity"], dict["n_machines"], dict["ef"])