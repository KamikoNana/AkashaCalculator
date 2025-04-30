"""
This file contains the Service for the Project Phases definition. 
- Defines the Service Class;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

import ghg_database
from Entity.ProjectPhases.project_phases_entity import Phase

class ProjectPhasesService():
    def __init__(self):
        self 
    
    def project_duration():
        """
        Obtaines each phase duration and the project hrizon duration as a list
        """
        construction = 0
        operation = 0
        for source, data in ghg_database.project_phases.items():
            if Phase[source] == Phase.CONSTRUCTION:
                construction = data["years"]
            if Phase[source] == Phase.OPERATION:
                operation = data["years"]
        
        return [construction, operation, construction + operation]