"""
This file contains the Entity for the Soil Use Change emissions source. 
- Defines the Entity Class and includes the calculation of the emissons for 1 element;
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

class SoilUseChange:
    def __init__(self, change, area, previous_soiluse, prev_seqfactor, new_soiluse, new_seqfactor):
        self.change = change                                        #name for the change (str)
        self.area = area                                            #area that will suffer soil change [m2] (float)
        self.previous_soiluse = previous_soiluse                    #previous soil use (str)
        self.prev_seqfactor = prev_seqfactor                        #previous soil use CO2 sequestration factor [tCO2/year]
        self.new_soiluse = new_soiluse                              #new soil use (str)
        self.new_seqfactor = new_seqfactor                          #new soil use CO2 sequestration factor [tCO2/year]

    def total_GHG_emissions(self):
        """
        Calculates the total GHG emissions for 1 element in this class
        - If this value is POSITIVE indicated that the new soil use sequestration factor is superior and so the change is beneficial
        """        
        prev_emissions_seq = self.prev_seqfactor * self.area
        new_emissions_seq = self.new_seqfactor * self.area

        return (prev_emissions_seq - new_emissions_seq)
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """        
        return {"change": self.change, "area": self.area, "previous_soiluse": self.previous_soiluse, \
            "prev_seqfactor": self.prev_seqfactor, "new_soiluse": self.new_soiluse, \
                "new_seqfactor": self.new_seqfactor}
        
    @staticmethod
    def soilusechange_from_dict(dict):
        """
        Get the data from the dictionary for later use
        """        
        return SoilUseChange(dict["change"], dict["area"], dict["previous_soiluse"], dict["prev_seqfactor"], \
            dict["new_soiluse"], dict["new_seqfactor"])