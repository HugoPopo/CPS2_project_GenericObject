#import paho.mqtt.client as mqtt
import sys
import json
from glob import glob
from DatasourceFactory import DatasourceFactory

config_path = "config"
if len(sys.argv) > 1:
    config_path = sys.argv[1]

factory = DatasourceFactory()
sensors = {}
    
for file in glob(config_path+"/*.json"):
    print(file)
    description = json.loads(open(file).read())
    print(description["object_type"]["value"])
    # create object with description with the factory
    sensors[description["object_name"]["value"]] = factory.createDatasource(description)
    
    

#~ description = {}
#~ config = json.loads(open("config.json").read())

#~ description["building"] = config["building"]
#~ description["room"] = config["room"]

#~ print(description["room"]["description"])


