from netmiko import ConnectHandler
import yaml

with open("devices.yaml") as file:
    devices = yaml.safe_load(file)

connection = ConnectHandler(**devices["R1"])

output = connection.send_command("show ip interface brief")

print(output)

connection.disconnect()