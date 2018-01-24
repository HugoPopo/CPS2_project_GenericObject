#import paho.mqtt.client as mqtt
import sys
import json
from glob import glob
from DatasourceFactory import DatasourceFactory
from threading import Thread

config_path = "config"
if len(sys.argv) > 1:
    config_path = sys.argv[1]

factory = DatasourceFactory()
sensors = {}
    
for file in glob(config_path+"/*.json"):
    print(file)
    description = json.loads(open(file).read())
    print(description["object_type"]["value"])
    # create object with description in the factory
    sensor = factory.createDatasource(description)
    sensors[description["object_name"]["value"]] = sensor
    #TODO run the loop in a thread
    sensor.loop_forever()
    

#~ description = {}
#~ config = json.loads(open("config.json").read())

#~ description["building"] = config["building"]
#~ description["room"] = config["room"]

#~ print(description["room"]["description"])


