from RealSensor import RealSensor
from PeriodicSensor import PeriodicSensor

class LightSensor(PeriodicSensor):
    
    def __init__(self, description):
        super().__init__(description)
