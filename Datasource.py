from abc import ABC, abstractmethod
from time import sleep
from paho.mqtt.client import Client
from threading import Thread
import paho.mqtt.publish as publish
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
        
        #self.fields = description["fields"]["values"]
        self.fields = { }
        
        self.base_topic = "/".join(self.base_parameters.values())
        # object config
        self.publishingMode = description["config"]["values"]["publishing_mode"]["value"]
        self.publishingInterval = description["config"]["values"]["publishing_period"]["value"]
        self.latency = description["config"]["values"]["response_latency"]["value"]
        #self.percentage_of_broadcast = description["config"]["values"]["percentage_of_broadcast"]["value"]
        
        # MQTT settings
        # Initialize the MQTT client
        self.mqtt_settings = description["config"]["values"]["mqtt_broker"]["values"]
        self.host_name = self.mqtt_settings["host_name"]["value"]
        self.host_port = self.mqtt_settings["host_port"]["value"]
        self.mqtt_user = self.mqtt_settings["user_name"]["value"]
        self.mqtt_password = self.mqtt_settings["password"]["value"]
        self.init_mqtt_client()
        
        #self.activate()
    
    def activate(self):
        # TODO create an adapted thread
        while(self.description["config"]["values"]["publishing_mode"]["value"]=="continuous"):
            print("while true")
            self.publishMeasure()
            
    @abstractmethod
    def publishMeasure(self):
        pass
        
    @abstractmethod
    def custom_mqtt_reaction(self, topic, message):
        """ Any reaction to a MQTT message other than configuration change or request.
         This behaviour depends on the object and thus should be defined in children classes.
         """
        raise NotImplementedError("Must override method custom_mqtt_reaction")

    def init_mqtt_client(self):
        """ initialize the MQTT client with the topics to subscribe to
        and the function to manage the received messages
        """
        self.mqtt_client = Client()  # create client object
        self.mqtt_client.username_pw_set(self.mqtt_user, self.mqtt_password)
        print("Connecting to the MQTT broker", self.host_name, ".")
        self.mqtt_client.connect(self.host_name, self.host_port)

        def on_message(client, userdata, msg):
            """ callback function to process mqtt messages """
            message_type = msg.topic.split("/")[-1]
            message = str(msg.payload.decode("utf-8"))
            print("\nreceived message on topic " + msg.topic + ": " + message)

            # The message should contain 3 things:
            # either <field/config>, parameter_name, new_value
            # or <field/config>, parameter_name, client_id
            if len(message.split(",")) != 3:
                print("Bad message structure")
                return 0

            # React to custom topics. Should be implemented in a concrete class depending on the behaviour to simulate.
            self.custom_mqtt_reaction(msg.topic, message)

            # The client wants to change the value of a parameter
            if message_type == "change":
                request_type, parameter_name, new_value = message.split(",")
                if request_type == "config" and parameter_name in self.get_parameters_list():
                    self.set_parameter_value(parameter_name, new_value)
                elif request_type == "field" and parameter_name in self.get_fields_list():
                    self.set_field_value(parameter_name, new_value)

            # The client requests the value of a parameter
            elif message_type == "request":
                    request_type, parameter_name, client_id = message.split(",")

                    # Fake latency
                    sleep(float(self.get_parameter_value("response_latency")) / 1000)

                    # ask for a configuration parameter
                    if request_type == "config":
                        print("request for a configuration parameter")
                        if parameter_name in self.get_parameters_list():
                            self.mqtt_client.publish(self.base_topic + "/answer/" + client_id,
                                                     self.get_parameter_value(parameter_name))
                        else:
                            self.mqtt_client.publish(self.base_topic + "/answer/" + client_id,
                                                     "no such parameter")

                    # ask for a field
                    elif request_type == "field":
                        print("request for a field")
                        if parameter_name in self.get_fields_list():
                            client.publish(self.base_topic + "/answer/" + client_id,
                                           self.get_field_value(parameter_name))
                        else:
                            self.mqtt_client.publish(self.base_topic + "/answer/" + client_id,
                                                     "no such field")

        self.mqtt_client.on_message = on_message  # bind function to callback

        building, floor, room, type, name = self.base_parameters.values()

        topics = [
            building + "/" + floor + "/" + room + "/" + type + "/" + name + "/+",
            building + "/" + floor + "/" + room + "/" + type + "/All/+",
            building + "/" + floor + "/" + room + "/All/All/+",
            building + "/" + floor + "/All/" + type + "/All/+",
            building + "/" + floor + "/All/All/All/+",
            building + "/All/All/" + type + "/All/+",
            building + "/All/All/All/All/+",
            "All/All/All/" + type + "/All/+",
            "All/All/All/All/All/+"
        ]
        for topic in topics:
            print("Subscribing to the topic " + topic)
            self.mqtt_client.subscribe(topic)

        self.mqtt_client.loop_start()  # start loop to process received messages

    def get_parameters_list(self):
        """ return the list of the configuration parameters """
        return self.description["config"]["values"].keys()

    def get_parameter_value(self, parameter_name):
        """ return the current value of a configuration parameter """
        if parameter_name in self.description["config"]["values"].keys():
            return self.description["config"]["values"][parameter_name]["value"]
        else:
            return "No such parameter"

    def set_parameter_value(self, parameter_name, new_value):
        """ change the value of a configuration parameter """
        self.description["config"]["values"][parameter_name]["value"] = new_value
        ## Update MongoDB
        #self.mongo_client.cps2_project.objects.update_one(
            #{"_id": self.mongo_id},
            #{"$set": {"config.values." + parameter_name + ".value": new_value,
                      #"last_modified.value": str(datetime.utcnow())}
            #}
        #)
        print("Switched the parameter " + parameter_name + " to " + new_value + " and updated MongoDB.")

    def get_fields_list(self):
        """ return the list of the available fields """
        return self.description["fields"]["values"].keys()

    def get_field_value(self, field_name):
        """ return the current value of a field. """
        if field_name in self.fields.keys():
            return self.fields[field_name]
        else:
            return "No such field"

    def set_field_value(self, field_name, new_value):
        """ change the value of a field """
        new_value = str(new_value)
        self.fields[field_name] = new_value
        # Send the new value to InfluxDB
        self.mqtt_client.publish(self.base_topic + "/metrics/" + field_name,
                                             self.get_field_value(field_name))
        print("Switched the field " + field_name + " to " + new_value + " and sent the new value to InfluxDB.")

    def add_field(self, field_name, label, description, type, function=None):
        """ add a field in the description of the object.
         The value of the field is either given by a function, or updated by the system. """
        new_field = {
            "label": label,
            "description": description,
            "type": type,
        }
        if function is not None:
            new_field["source"] = "function"
            self.fields[field_name] = function
        else:
            new_field["source"] = "system"
            self.fields[field_name] = "No value"
        self.description["fields"]["values"][field_name] = new_field

        # update MongoDB
        #self.mongo_client.cps2_project.objects.update_one(
            #{"_id": self.mongo_id},
            #{"$set": {"fields.values." + field_name: new_field,
                      #"last_modified.value": str(datetime.utcnow())}
             #}
        #)
        print("Added a new field called \"" + field_name + "\" and updated MongoDB.")

    def loop_forever(self):
        """ Publish and process MQTT messages forever """
        while True:
            if self.get_parameter_value("publishing_mode") == "continuous":
                self.publishMeasure()
