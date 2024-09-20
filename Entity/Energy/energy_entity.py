#Energy
from Services.ProjectPhases.project_phases_service import ProjectPhasesService


class Energy:
    def __init__(self, phase, type, source, quantity, ef):
        self.phase = phase                          #project phase
        self.type = type                            #diferenciate between energy produced and energy consumed
        self.source = source                        #energ source
        self.quantity = quantity                    #quantity of energy used per year [MW/year] (float)
        self.ef = ef                                #emission factor [tCO2/MW] (float)
    
    def total_GHG_emissions(phase, quantity, ef):
        if phase == "CONSTRUCTION":
            return quantity * ef * ProjectPhasesService.project_duration()[0]
        elif phase == "OPERATION":
            return quantity * ef * ProjectPhasesService.project_duration()[1]
            
    def to_dict(self):
        return {"phase": self.phase, "type": self.type, "source": self.source, "quantity": self.quantity, "ef": self.ef}
    
    @staticmethod
    def energy_from_dict(dict):
        return Energy(dict["phase"], dict["type"], dict["source"], dict["quantity"], dict["ef"])