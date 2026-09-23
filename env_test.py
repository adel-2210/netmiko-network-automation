import os

for key in os.environ:
    if "NETMIKO" in key:
        print(repr(key))