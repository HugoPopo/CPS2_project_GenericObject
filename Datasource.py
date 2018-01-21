from abc import ABC, abstractmethod
import json

class Datasource(ABC):
    
    def __init__(self, description):
        self.description = description
        
        # Base parameters such as the location and the type of the object
        self.base_parameters = {
            "building": self.description["building"]["value"],
            "floor": self.description["floor"]["value"],
            "room": self.description["room"]["value"],
            "object_type": self.description["object_type"]["value"],
            "object_name": self.description["object_name"]["value"]
        }
        
        
        self.topic = "/".join(self.base_parameters)
        # object config
        self.publishingMode = description["config"]["values"]["publishing_mode"]["value"]
        self.publishingInterval = description["config"]["values"]["publishing_period"]["value"]
        self.latency = description["config"]["values"]["response_latency"]["value"]
        #self.percentage_of_broadcast = description["config"]["values"]["percentage_of_broadcast"]["value"]
        
        # MQTT settings
        #self.mqtt = 
        
        self.activate()
    
    
    
    def activate(self):
        # TODO create an adapted thread
        while(self.publishingMode=="continuous"):
            print("while true")
            self.publishMeasure()
            
    @abstractmethod
    def publishMeasure(self):
        pass
        
    @abstractmethod
    def getMeasure(self):
        pass
        
    #getters & setters
    def getLatency(self):
        return self.latency
        
    def getPublishingMode(self):
        return self.publishingMode
        
    def setPublishingMode(self, mode):
        if mode in self.description["config"]["publishing_mode"]["possible_values"]:
            self.publishingMode = mode
