"""
This file contains the Service for the Project Phases definition. 
- Defines the Service Class;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

import json

from Entity.ProjectPhases.project_phases_entity import Phase

class ProjectPhasesService():
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.ghg_database = json.load(f)
    
    def __init__(self, ghg_database):
        self.ghg_database = ghg_database
    
    def project_duration(self):
        """
        Obtaines each phase duration and the project hrizon duration as a list
        """
        construction = 0
        operation = 0
        for source, data in self.ghg_database["project_phases"].items():
            if Phase[source] == Phase.CONSTRUCTION:
                construction = data["years"]
            if Phase[source] == Phase.OPERATION:
                operation = data["years"]
        
        return [construction, operation, construction + operation]