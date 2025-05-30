"""
This file contains the Service for the Soil Use Change emissions source. 
- Includes all calculations for the Soil Use Change class elements
All variables are described in the Akasha Guidebook avaliable in the GitHub repository
"""

import json

from Entity.SoilUseChange.soil_use_change_entity import SoilUseChange

class SoilUseChangeCalculations():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
        
    def total_emissions_soilusechange(self):
        """
        Calculates the total sum of GHG emissions for this emissions source
        - Calculates the balance between the previous soil use and the new soil use sequestration factor for all elements
        """
        total_emissions_soilusechange = 0
        emissions_soilusechange =[]
        for source, data in self.ghg_database["soil_use_change"].items():
            soil_use = SoilUseChange.soilusechange_from_dict(data)
            
            total_emissions_soilusechange = total_emissions_soilusechange + \
                soil_use.total_GHG_emissions()
            emissions_soilusechange.append([soil_use.change, \
                soil_use.total_GHG_emissions()])
        
        return [total_emissions_soilusechange, emissions_soilusechange]