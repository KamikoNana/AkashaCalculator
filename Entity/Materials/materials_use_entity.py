"""
This file contains the Entity for the Materials Used emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""


class MaterialsUse:
    def __init__(self, phase, material, quantity, ef):
        self.phase = phase                              #project phase (enum ProjectPhase.Phase)
        self.material = material                        #name - material used (str)
        self.quantity = quantity                        #quantity of material used in total [kg] (float)
        self.ef = ef                                    #emission factor of the material production [tCO2eq/kg] (float)
    
    def total_GHG_emissions(self):
        """
        Calculates the total GHG emissions for 1 element in this class
        """        
        return self.quantity * self.ef
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """        
        return {"phase": self.phase, "material": self.material, "quantity": self.quantity, \
            "ef": self.ef}
        
    @staticmethod
    def materialsuse_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """        
        return MaterialsUse(dict["phase"], dict["material"], dict["quantity"], dict["ef"])