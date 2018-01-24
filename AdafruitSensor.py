from PeriodicSensor import PeriodicSensor
import Adafruit_BMP.BMP085 as BMP085


class AdafruitSensor(PeriodicSensor):
    def __init__(self, description):
        super().__init__(description)
        self.sensor = BMP085.BMP085()
        self.add_field(
            field_name="temperature",
            label="Temperature",
            description="A temperature of the room",
            type="Float"
        )
       
       
    def getMeasure(self):
        return self.sensor.read_temperature()
    
    def custom_mqtt_reaction(self, topic, message):
        pass
