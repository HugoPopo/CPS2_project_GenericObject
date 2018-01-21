from PeriodicSensor import PeriodicSensor

class DumbSensor(PeriodicSensor):
    
    def __init__(self, description):
        super().__init__(description)
        
    def getMeasure(self):
        return 12
