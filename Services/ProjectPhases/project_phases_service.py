import ghg_database

class ProjectPhasesService():
    def __init__(self):
        self
    
    def project_duration():
        construction = 0
        operation = 0
        for source, data in ghg_database.project_phases.items():
            if source == "CONSTRUCTION":
                construction = data["years"]
            if source == "OPERATION":
                operation = data["years"]
        
        return [construction, operation, construction + operation]