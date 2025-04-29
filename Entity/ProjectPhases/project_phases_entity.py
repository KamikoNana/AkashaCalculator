"""
This file contains the Entity for the Project Phases definition. 
- Defines the Entity Class;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

from enum import Enum
 
class Phase(Enum):
    """
    subclass to define the various project phases as enum variables
    """
    CONSTRUCTION = 1
    OPERATION = 2
        
class ProjectPhases:
    def __init__(self, phase, years):
        self.phase = phase                          #project phase (enum ProjectPhases.Phase)
        self.years = years                          #duration in years of the project phase (int)
    
    def to_dict(self):
        """
        Transforms data from original format in excel input file to dictionary format
        """
        return {"phase": self.phase, "years": self.years}
    
