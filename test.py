from netmiko import ConnectHandler
from netmiko.exceptions import(NetMikoTimeoutException,NetMikoAuthenticationException)
import yaml

with open("devices.yaml") as file:
    devices = yaml.safe_load(file)
selected_devices = []    
for device_name , device_data in devices.items():
  if (
     device_data  ['role'] =='router' and device_data ['site'] =="cairo"
     ):
     selected_devices.append(device_name)
print('selected_devices:', selected_devices)     
for device_name in selected_devices:
  device_data = devices[device_name]    
  connection_data = {
    "device_type": device_data['device_type'] ,
    "host": device_data['host'],
    'username': device_data['username']
    ,"password": device_data['password'] 
  }
  connection = None
  try:
   connection = ConnectHandler(**connection_data)
   print(f"{device_name}connected succ")
   output = connection.send_command("show ip interface brief" , use_textfsm=True )
   for interface in output:
    if (interface["status"] =='up' and interface["proto"] =='up'):
     print(device_name, interface["interface"] ,"ok")
    elif interface['status'] == "administratively down":
     print(device_name , interface['interface'],"is administratively down")
    elif interface ['status'] == "up " and interface ['proto'] == 'down' :
      print (device_name , interface["interface"] ,'proto problem')
   connection.disconnect()
  except NetMikoTimeoutException :
   print(f'{device_name}connection timeout')
  except NetMikoAuthenticationException:
   print(f'{device_name}Authentication faild')
  finally: 
    if connection : connection.disconnect()
 # if interface['status'] == "adminstratively down":
  #  print(interface['interface'],"is adminstrativelydown")
  #elif(interface["status"] =='up' and interface["proto"] =='down'):
   #  print(interface["interface"], "has a proto prob")
  #elif (interface["status"] =='up' and interface["proto"] =='up'):
     #print(interface["interface"], "ok")  

#config_commands = [
 #   "interface GigabitEthernet0/2 ","description NETMIKO-LAB"
#]
#output_4 = connection.send_config_set(config_commands)
#print(output_4)

#output_2 = connection.send_command("show version" , use_textfsm=True , read_timeout=60)

#version = output_2[0]["version"]
#expected_version= '15.9(3)M6' 
#for version in output_2:
#  if version == expected_version:
#     print ("ok")
#  else:
#     print("version mismatch")   

#print(output_2)

#output_3 = connection.send_command("show running-config | section routing ospf" , use_textfsm=True)
#print(output_3)

# output_5 = connection.send_command("show ip route" , use_textfsm=True )
# if 'Gateway of last resort is not set' in output_5 :
#   print("no default route")
# else:
#   print("default route exist")  

#print(output_5)
#excepted_network = "192.168.10.0/24"
#if excepted_network in output_5 :
#  print ('route exist')
#else:
#  print("route missing")
#output_6 = connection.send_command("show running-config")
#with open ("R1_backup.txt" , "w") as file:
# file.write(output_6)

#config =connection.send_command("show running-config interface GigabitEthernet0/2")  
#if "description NETMIKO-LAB" in config:
#  print("description ok")
#else:
#  print("description missing")  


#verify= connection.send_command("show running-config interface GigabitEthernet0/2")
#print(verify)

#prompt = connection.find_prompt()
#print(prompt)


def connect_device (device_data):
    connection_data = {
        'device_type' : device_data ['device_type']
     ,   'host': device_data['host']
      ,  'username': device_data['username']
       , 'password': device_data['password']
    }
    connection = ConnectHandler(**connection_data)
    
    return connection
def send_command(connection,command , use_textfsm=False):
    output = connection.send_command(command , use_textfsm=use_textfsm )
    return output 
def get_interface(connection):
    return send_command(connection,"show ip interface brief" , use_textfsm=True)
def analyze_inteface (device_name,interfaces) :
    for interface in interfaces:
       if (interface ['status'] == "up" and interface['proto']  == "up"
       ):
           print(device_name,interface['interface'], "ok")
       else:
           print(device_name,interface['interface'],'problem')   
for device_name in selected_devices :
    connection=None
    try:
           device_data=devices[device_name]
           connection = connect_device(device_data)
           interfaces =send_command(connection,"show ip interface brief"  , use_textfsm=True)
           roure =send_command(connection,"show ip route")
           analyze_inteface(device_name,interfaces)
        
    except NetMikoTimeoutException:
     print(device_name,"TIME OUT  faild")
    except NetMikoAuthenticationException :
        print(device_name, "authintication faild")
    finally:
        if connection: connection.disconnect()    
