import json
import logging
import os
import requests
import sys

# the following is the default for PPBA but change as needed
host_and_port = "localhost:32000"
# buffer indicates how many degrees the air temp will be (in C) below dew point before triggering camera dew heater 
buffer_temperature = 2


# Determine the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create a logs directory if it doesn't exist in the script directory
logs_dir = os.path.join(script_dir, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(logs_dir, 'nina-camera-dew-heater.log'),
    filemode='a'
)

def start_server(host_and_port):
    url = f'http://{host_and_port}/Server/Start'
    response = requests.put(url)
    response_data = json.loads(response.text)
    if (response_data['code'] != 200):
        logging.error("Error detected. Exiting the application.")
        sys.exit(1)  # Exit the application with status code 1 indicating an error
    
    return


def get_connected_devices(host_and_port):
    url = f'http://{host_and_port}/Server/DeviceManager/Connected'
    response = requests.get(url)
    response_data = json.loads(response.text)    
    if (response_data['code'] != 200):
        logging.error("Error detected. Exiting the application.")
        sys.exit(1)  # Exit the application with status code 1 indicating an error

    unique_keys = {device['uniqueKey'] for device in response_data['data'] if device.get('name') == "PPBAdvance"}
  
    return unique_keys


def get_current_environment(host_and_port, driver_unique_key):
    url = f'http://{host_and_port}/Driver/PPBAdvance/Report/Environment?DriverUniqueKey={driver_unique_key}'
    response = requests.get(url)
    response_data = json.loads(response.text)    
    if (response_data['code'] != 200):
        logging.error("Error detected. Exiting the application.")
        sys.exit(1)  # Exit the application with status code 1 indicating an error

    report = response_data['data']['message']
    return report['temperature'], report['humidity'], report['dewPoint']

if __name__ == "__main__":

    start_server(host_and_port)
    unique_keys = get_connected_devices(host_and_port)
    
    enable_heater = False
    env_readout = ""
    for index, key in enumerate(unique_keys):
        env = get_current_environment(host_and_port, key)
        temperature = env[0]
        humidity = env[1]
        dew_point = env[2]
        # if multiple devices are supported, enable heater if any of those devices indicates temp is close to dew point
        enable_heater = enable_heater or (temperature <= dew_point + buffer_temperature)
        env_readout += f"PPBA {index}: temp {temperature} °C, humidity {humidity} %, dew pt {dew_point} °C"
        
    env_readout = f"temp {temperature}°C, humidity {humidity}%, dew pt {dew_point}°C"
    if (enable_heater):
        logging.info(f"Dew is imminent [{env_readout}]")
        sys.exit(-1)
    else:
        logging.info(f"Dew is not imminent [{env_readout}]")
        sys.exit(0)
