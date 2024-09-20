## Project phases
# (phase, years)


class ProjectPhases:
    def __init__(self, phase, years):
        self.phase = phase                          #name of the project phase (str)
        self.years = years                          #duration in years of the project phase (int)
    
    def to_dict(self):
        return {"phase": self.phase, "years": self.years}