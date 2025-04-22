"""
This file contains the Entity for the Project Phases definition. 
- Defines the Entity Class;
All variables are described in the AkachaCalc Guidebook avaliable in the GitHub repository
"""

class ProjectPhases:
    def __init__(self, phase, years):
        self.phase = phase                          #name of the project phase (str)
        self.years = years                          #duration in years of the project phase (int)
    
    def to_dict(self):
        return {"phase": self.phase, "years": self.years}