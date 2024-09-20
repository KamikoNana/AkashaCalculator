## Soild use change
# (area, previous_soiluse, prev_seqfactor, new_soilduse, new_seqfactor)

class SoilUseChange:
    def __init__(self, name, area, previous_soiluse, prev_seqfactor, new_soiluse, new_seqfactor):
        self.name = name                            #name of the transaction 
        self.area = area                            #area that will suffer soil change [m2] (float)
        self.previous_soiluse = previous_soiluse    #previous soil use (str)
        self.prev_seqfactor = prev_seqfactor        #previous soil use CO2 sequestration factor [tCO2/year]
        self.new_soiluse = new_soiluse              #new soil use (str)
        self.new_seqfactor = new_seqfactor          #new soil use CO2 sequestration factor [tCO2/year]

    def total_GHG_emissions(area, prev_seqfactor, new_seqfactor):
        prev_emissions_seq = prev_seqfactor * area
        new_emissions_seq = new_seqfactor * area

        return (new_emissions_seq - prev_emissions_seq)
    
    def to_dict(self):
        return {"change": self.name, "area": self.area, "previous soil use": self.previous_soiluse, \
            "previous sequestration factor": self.prev_seqfactor, "new soil use": self.new_soiluse, \
                "new sequestration factor": self.new_seqfactor}
        
    @staticmethod
    def soilusechange_from_dict(dict):
        return SoilUseChange(dict["name"], dict["area"], dict["previous_soiluse"], dict["prev_seqfactor"], \
            dict["new_soiluse"], dict["new_seqfactor"])