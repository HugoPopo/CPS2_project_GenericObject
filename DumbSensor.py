from PeriodicSensor import PeriodicSensor
from random import randint

class DumbSensor(PeriodicSensor):
    
    def __init__(self, description):
        super().__init__(description)
        self.add_field(
            field_name="dumb_measure",
            label="Dumb measure",
            description="A dumb measure for testing",
            type="Integer"
        )
        self.measure = randint(0,100)
        
    def getMeasure(self):
        return self.measure
        
    def custom_mqtt_reaction(self, topic, message):
        pass
