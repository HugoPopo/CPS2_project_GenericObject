from Datasource import Datasource
import time

class PeriodicSensor(Datasource):
    
    def __init__(self, description):
        super().__init__(description)
        self.publishingPeriod = description["config"]["values"]["publishing_period"]["value"]
        
    def publishMeasure(self):
        measure = self.getMeasure()
        print(self.topic," ",measure)
        #TODO mqtt publish
        time.sleep(self.publishingInterval+self.latency)
