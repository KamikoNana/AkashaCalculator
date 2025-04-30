"""
This file contains the Service for the Soil Use Change emissions source. 
- Includes all calculations for the Soil Use Change class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import ghg_database

from Entity.SoilUseChange.soil_use_change_entity import SoilUseChange

class SoilUseChangeCalculations():
    def __init__(self):
        self
        
    def total_emissions_soilusechange():
        """
        Calculates the total sum of GHG emissions for this emissions source
        - Calculates the balance between the previous soil use and the new soil use sequestration factor for all elements
        """
        total_emissions_soilusechange = 0
        emissions_soilusechange =[]
        for source, data in ghg_database.soil_use.items():
            data = SoilUseChange.soilusechange_from_dict(data)
            
            total_emissions_soilusechange = total_emissions_soilusechange + \
                SoilUseChange.total_GHG_emissions(data.area, \
                    data.prev_seqfactor, data.new_seqfactor)
            emissions_soilusechange.append([data.change, \
                SoilUseChange.total_GHG_emissions(data.area, \
                    data.prev_seqfactor, data.new_seqfactor)])
        
        return [total_emissions_soilusechange, emissions_soilusechange]