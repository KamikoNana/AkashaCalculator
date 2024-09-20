import ghg_database

from Entity.SoilUseChange.soil_use_change_entity import SoilUseChange

class SoilUseChangeCalculations():
    def __init__(self):
        self
        
    def total_emissions_soilusechange():
        total_emissions_soilusechange = 0
        emissions_soilusechange =[]
        for source, data in ghg_database.soil_use_change.items():
            data = SoilUseChange.soilusechange_from_dict(data)
            
            total_emissions_soilusechange = total_emissions_soilusechange + \
                SoilUseChange.total_GHG_emissions(data.name, data.area, \
                    data.previous_soiluse, data.prev_seqfactor, data.new_soiluse, data.new_seqfactor)
            emissions_soilusechange.append([data.name, data.type, \
                SoilUseChange.total_GHG_emissions(data.name, data.previous_soiluse, data.new_soiluse, \
                    data.previous_soiluse, data.prev_seqfactor, data.new_soiluse, data.new_seqfactor)])
        
        return [total_emissions_soilusechange, emissions_soilusechange]