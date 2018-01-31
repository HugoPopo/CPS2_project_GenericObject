# CPS2_project_GenericObject

This project aims at simulating a generic connected object solution with client interaction.
This part of the projet focuses on the object itself, simulated through a singular program running on a **Raspberry Pi**.
For more details about the project, please check the [other part](https://github.com/CPS2project). 
## Launching the program

The main file to run on the Raspberry Pi is [**roomHandler.py**](https://github.com/HugoPopo/CPS2_project_GenericObject/blob/master/roomHandler.py). It takes an optional argument, the path to the configuration files for each sensor.
By default, the path is the folder /config.
```shell
python3 roomHandler.py config/Adafruit
```
This line launches the program with the Adafruit sensor configured.

## Implement a new sensor
### create the config file
This file contains the information to set up a functional sensor:
* descriptors for each level of the MQTT topic of the object
* configuration for the sensor:
 * MQTT connection settings
 * MongoDB connection settings
 * publishing mode: either continuous or on-demand
 * possible values for not working object (latency, percentage of response, etc.)
* fields of measure (temperature, etc.)

Take a look at [**config_adafruit.json**](https://github.com/HugoPopo/CPS2_project_GenericObject/blob/master/config/config_adafruit.json) or [**config_dumb.json**](https://github.com/HugoPopo/CPS2_project_GenericObject/blob/master/config/config_dumb.json) for concrete examples.

### create the adapted class
If you want to add a new type of sensor to the solution, you have to implement a new class inheriting the class(es) of the properties you want in your sensor.
For example, if you want to set up a sensor sending temperature, you will need to inherit from [**PeriodicSensor**](https://github.com/HugoPopo/CPS2_project_GenericObject/blob/master/PeriodicSensor.py), for its publishing method is based on a publishing period in the config file.

## Test the object with MQTT messages
With an MQTT broker like Mosquitto, you can directly publish messages on the wanted topic with a certain command line input.
For example, the following line changes the publishing mode of the object:
```shell
mosquitto_pub -t "EF/1/Espace élèves/printer/MyPrinter/change" -m "config,publishing_mode,continuous"
```
For further details about possible command line inputs, please refer to the [other dedicated part of the project](https://github.com/CPS2project/Server/tree/master/dummyObject).
