## Materials production
# (material, process, quantity, ef)
from Services.ProjectPhases.project_phases_service import ProjectPhasesService


class MaterialsProduction:
    def __init__(self, phase, material, process, quantity, ef):
        self.phase = phase                          #project phase
        self.material = material                    #material used (str)
        self.process = process                      #production process (str)
        self.quantity = quantity                    #quantity of material produced per year [kg/year] (float)
        self.ef = ef                                #emission factor of the material production [tCO2eq/kg] (float)
    
    def total_GHG_emissions(phase, quantity, ef):
        if phase == "CONSTRUCTION":
            return quantity * ef * ProjectPhasesService.project_duration()[0]
        elif phase == "OPERATION":
            return quantity * ef * ProjectPhasesService.project_duration()[1]
    
    def to_dict(self):
        return {"phase": self.phase, "material": self.material, "process": self.process, \
            "quantity": self.quantity, "ef": self.ef}
    
    @staticmethod
    def materialprod_from_dict(dict):
        return MaterialsProduction(dict["phase"], dict["material"], dict["process"], dict["quantity"], dict["ef"])