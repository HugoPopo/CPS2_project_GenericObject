from Datasource import Datasource
from LightSensor import LightSensor
from RemoteDatasource import RemoteDatasource
from AdafruitSensor import AdafruitSensor
from DumbSensor import DumbSensor

class DatasourceFactory(object):
    
    __datasourceBuilder = {
        "light sensor": LightSensor,
        #"motion sensor": MotionSensor,
        "remote": RemoteDatasource,
        "dumb": DumbSensor,
        "Adafruit temperature sensor": AdafruitSensor
    }
    
    def __init__(self):
        pass
        
    def createDatasource(self,description):
        object_type = description["object_type"]["value"]
        return DatasourceFactory.__datasourceBuilder[object_type](description)
        
