from netmiko import ConnectHandler
#from netmiko.exceptions import (NetMikoAuthenticationException , NetMikoTimeoutException)
#from concurrent.futures import ThreadPoolExecutor
import yaml
#import time
#import threading

with open("devices.yaml") as file:
    devices = yaml.safe_load(file)
selected_devices = ["R1", "R2"]
for device_name in selected_devices:




    device_data = devices[device_name]

    connection_data = {
        "device_type": device_data["device_type"],
        "host": device_data["host"],
        "username": device_data["username"],
        "password": device_data["password"]
    }
    print("connection data password:" , connection_data["password"] is not None)
    connection = ConnectHandler(**connection_data)

    output = connection.send_command(

        "show ip interface brief"
    )
    print(device_name)
    print(output)
    connection.disconnect()
































#  devices=yaml.safe_load(file)
# selected_devices= ["R1" , 'R2']
# start_time=time.time()
# def connect_and_show (device_name):
#  connection=None
#  try:
#   device_data= devices[device_name]
#   connection_data = {
#     "device_type": device_data['device_type'] ,
#     "host": device_data['host'],
#     'username': device_data['username']
#     ,"password": device_data['password'] 
#     }
#   connection= ConnectHandler(**connection_data)
#   output = connection.send_command("show ip interface brief")
#   return {
#     "device": device_name,
#    "status": "success" ,
#      "output": output} 
#  finally:
#    if connection :
#     connection.disconnect()

# print("ALL DEVICES COMPLEATED")  
 
# end_time=time.time()
# print('total time :' , end_time-start_time)
# futures= []
# with ThreadPoolExecutor(max_workers=2) as executor:
#  for device_name in selected_devices:
#   future = executor.submit(connect_and_show,device_name)
#   futures.append(future)
# for future in futures:
#   try:
#     result= future.result()  
#     print(result['output'])
#   except NetMikoAuthenticationException:
#     print('auth faild')  
#   except NetMikoTimeoutException:
#      print("connection time out") 






#  print(device_name , "connected")
#  print(output)
#   executor.map(connect_and_show,selected_devices)
# for device_name , device_data in devices.items():
#   if (
#      device_data  ['role'] =='router' and device_data ['site'] =="cairo"
#      ):
#      selected_devices.append(device_name)
# print('selected_devices:', selected_devices)     
# successful_devices=[]
# faild_devices=[]
# for device_name in selected_devices:
#   connection=None
#   try:
#    device_data = devices[device_name]    
#    print(device_name,"cofiguration applied")

#  config_commands=['interface GigabitEthernet0/2',f'description {device_name}-UPLINK']
#  output = connection.send_config_set(config_commands)
#    verify=connection.send_command("show running-config interface GigabitEthernet0/2")
#    print("VERIFY OUTPUT:")
#    print(verify)
#    if f"description {device_name}-UPLINK " in verify:
#      print(device_name,"configure verifed")
#    else :
#      print(device_name , "configuration verification faild") 
     
   
#    print('configuration completed')
#   except NetMikoTimeoutException :
#     print(f'{device_name}connection timeout')
#   except NetMikoAuthenticationException:
#     print(f'{device_name}Authentication faild')
#   finally: 
#     if connection : connection.disconnect()
#   print("successful devices:" , successful_devices)
#   print("faild devices:" , faild_devices)  
# os.makedirs("backups", exist_ok=True)
# timestamp= datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
#    print('current directory:',os.getcwd())
#    filename=f'backups/{device_name}_{timestamp}_buckup.txt'
#    print("saving backup to:", filename)
#    with open (filename, "w") as file:
#     file.write(output)
#     print("foke exist:",os.path.exists(filename) )
#     print("fullpah:",os.path.abspath(filename))
#     print(device_name, "backup completed")
# logging.basicConfig(level=logging.INFO ,format=" - %(levelname)s - %(message)s" ,filename="automation.log")
# logging.info("script started")
# logging.info("R1 connected")


# def connect_device (device_data):
#     logging.info(f"connecting to {device_data['host']}")
#     connection_data = {
#         'device_type' : device_data ['device_type']
#      ,   'host': device_data['host']
#       ,  'username': device_data['username']
#        , 'password': device_data['password']
#     }
#     connection = ConnectHandler(**connection_data)
#     logging.info(f'connected to {device_data['host']}')
#     return connection
# def send_command(connection,command , use_textfsm=False):
#     output = connection.send_command(command , use_textfsm=use_textfsm )
#     return output 
# def get_interface(connection):
#     return send_command(connection,"show ip interface brief" , use_textfsm=True)
# def analyze_inteface (device_name,interfaces) :
#     for interface in interfaces:
#        if (interface ['status'] == "up" and interface['proto']  == "up"
#        ):
#            print(device_name,interface['interface'], "ok")
#        else:
#            print(device_name,interface['interface'],'problem')   
# for device_name in selected_devices :
#     connection=None
#     try:
#            device_data=devices[device_name]
#            connection = connect_device(device_data)
#            interfaces =send_command(connection,"show ip interface brief"  , use_textfsm=True)
#            roure =send_command(connection,"show ip route")
#            analyze_inteface(device_name,interfaces)
        
#     except NetMikoTimeoutException:
#      logging.error(f"{device_name}TIME OUT  faild")
#     except NetMikoAuthenticationException :
#         logging(f"{device_name} authintication faild")
#     finally:
#         if connection: connection.disconnect() 