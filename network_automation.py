import yaml
import logging
import openpyxl

from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetMikoTimeoutException,
    NetMikoAuthenticationException
)

from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    filename="automation.log"
)


def load_inventory():
    with open("devices.yaml") as file:
        devices = yaml.safe_load(file)

    return devices


def select_devices(devices):
    selected_devices = []

    for device_name, device_data in devices.items():
        if (
            device_data["role"] == "router"
            and device_data["site"] == "Cairo"
        ):
            selected_devices.append(device_name)

    return selected_devices


def connect_device(device_data):
    connection_data = {
        "device_type": device_data["device_type"],
        "host": device_data["host"],
        "username": device_data["username"],
        "password": device_data["password"]
    }

    connection = ConnectHandler(**connection_data)

    return connection


def collect_interfaces(connection):
    interfaces = connection.send_command(
        "show ip interface brief",
        use_textfsm=True
    )

    return interfaces


def collect_version(connection):
    version = connection.send_command(
        "show version",
        use_textfsm=True
    )

    return version


def collect_routes(connection):
    routes = connection.send_command(
        "show ip route"
    )

    return routes


def analyze_interfaces(interfaces):
    results = []

    for interface in interfaces:

        if (
            interface["status"] == "up"
            and interface["proto"] == "up"
        ):
            status = "OK"
        else:
            status = "PROBLEM"

        results.append({
            "interface": interface["interface"],
            "ip_address": interface["ip_address"],
            "status": status
        })

    return results


def decide_action(analysis):
    actions = []

    for interface in analysis:

        if interface["status"] == "PROBLEM":
            actions.append(interface["interface"])

    return actions


def apply_configuration(connection, interface_name):
    config_commands = [
        f"interface {interface_name}",
        "description CAPSTONE-AUTOMATION"
    ]

    output = connection.send_config_set(
        config_commands
    )

    return output


def verify_configuration(connection, interface_name):
    output = connection.send_command(
        f"show running-config interface {interface_name}"
    )

    if "description CAPSTONE-AUTOMATION" in output:
        return True

    return False


def backup_configuration(connection, device_name):
    config = connection.send_command(
        "show running-config"
    )

    filename = f"backups/{device_name}_backup.txt"

    with open(filename, "w") as file:
        file.write(config)

    return filename


def create_report(results):
    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Automation Report"

    sheet.append([
        "Device",
        "Interface",
        "IP Address",
        "Status"
    ])

    for result in results:

        sheet.append([
            result["device"],
            result["interface"],
            result["ip_address"],
            result["status"]
        ])

    workbook.save("automation_report.xlsx")


def automate_device(device_name):

    connection = None

    try:
        device_data = devices[device_name]

        connection = connect_device(device_data)

        print(device_name, "connected")
        logging.info(f"{device_name} connected")

        interfaces = collect_interfaces(connection)
        version = collect_version(connection)
        routes = collect_routes(connection)

        print(device_name, "data collected")
        logging.info(f"{device_name} data collected")

        analysis = analyze_interfaces(interfaces)

        device_results = []

        for interface in analysis:
            device_results.append({
                "device": device_name,
                "interface": interface["interface"],
                "ip_address": interface["ip_address"],
                "status": interface["status"]
            })

        actions = decide_action(analysis)

        for interface_name in actions:

            apply_configuration(
                connection,
                interface_name
            )

            print(
                device_name,
                interface_name,
                "configuration applied"
            )

            verified = verify_configuration(
                connection,
                interface_name
            )

            if verified:
                print(
                    device_name,
                    interface_name,
                    "verification successful"
                )

                logging.info(
                    f"{device_name} {interface_name} "
                    "verification successful"
                )

            else:
                print(
                    device_name,
                    interface_name,
                    "verification failed"
                )

                logging.warning(
                    f"{device_name} {interface_name} "
                    "verification failed"
                )

        backup_file = backup_configuration(
            connection,
            device_name
        )

        print(
            device_name,
            "backup completed:",
            backup_file
        )

        logging.info(
            f"{device_name} backup completed"
        )

        return device_results

    except NetMikoTimeoutException:

        print(
            device_name,
            "connection timeout"
        )

        logging.error(
            f"{device_name} connection timeout"
        )

    except NetMikoAuthenticationException:

        print(
            device_name,
            "authentication failed"
        )

        logging.error(
            f"{device_name} authentication failed"
        )

    finally:

        if connection:
            connection.disconnect()


logging.info("Automation started")

devices = load_inventory()

selected_devices = select_devices(devices)

print("Selected devices:", selected_devices)

all_results = []

with ThreadPoolExecutor(max_workers=2) as executor:

    futures = []

    for device_name in selected_devices:

        future = executor.submit(
            automate_device,
            device_name
        )

        futures.append(future)

    for future in futures:

        try:
            device_results = future.result()

            if device_results:
                all_results.extend(device_results)

        except Exception as error:
            print("Unexpected error:", error)


create_report(all_results)

logging.info("Automation completed")

print("Automation completed")