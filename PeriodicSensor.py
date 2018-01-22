from Datasource import Datasource
import time

class PeriodicSensor(Datasource):
    
    def __init__(self, description):
        super().__init__(description)
        
    def publishMeasure(self):
        for field_name in self.get_fields_list():
            self.set_field_value(field_name, self.getMeasure())
            self.mqtt_client.publish(self.base_topic + "/metrics/" + field_name,
                                     self.get_field_value(field_name))
        time.sleep(float(self.get_parameter_value("publishing_period")) / 1000)
