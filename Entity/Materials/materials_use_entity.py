## Materials used 
# (material, quantity, prod_ef, use_ef)
from Services.ProjectPhases.project_phases_service import ProjectPhasesService


class MaterialsUse:
    def __init__(self, phase, material, quantity, ef):
        self.phase = phase                          #project phase
        self.material = material                    #material used (str)
        self.quantity = quantity                    #quantity of material used in total [kg] (float)
        self.ef = ef                      #emission factor of the material production [tCO2eq/kg] (float)
    
    def total_GHG_emissions(phase, material, quantity, ef):
        if phase == "CONSTRUCTION":
            return quantity * ef * ProjectPhasesService.project_duration()[0]
        elif phase == "OPERATION":
            return quantity * ef * ProjectPhasesService.project_duration()[1]
    
    def to_dict(self):
        return {"phase": self.phase, "material": self.material, "quantity": self.quantity, \
            "ef": self.ef}
        
    @staticmethod
    def materialsuse_from_dict(dict):
        return MaterialsUse(dict["phase"], dict["material"], dict["quantity"], dict["ef"])