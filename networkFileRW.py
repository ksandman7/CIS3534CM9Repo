#!/usr/bin/env python3
#networkFileRW.py
#Pamela Brauda
#Thursday, March 3, 2022
#Update routers and switches;
#read equipment from a file, write updates & errors to file

##---->>>> Use a try/except clause to import the JSON module



##---->>>> Create file constants for the file names; file constants can be reused
##         There are 2 files to read this program: equip_r.txt and equip_s.txt
##         There are 2 files to write in this program: updated.txt and errors.txt
      




# Constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"
ROUTER_FILE = "equip_r.txt"
SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

# Try/except to import json
try:
    import json
except ImportError:
    print("Error: Could not import JSON module.")
    exit()

# Function to get valid device
def getValidDevice(routers, switches):
    while True:
        device = input(UPDATE + QUIT).lower()
        if device in routers or device in switches:
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

# Function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    while True:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        if len(octets) == 4:
            try:
                if all(0 <= int(byte) <= 255 for byte in octets):
                    return ipAddress, invalidIPCount
            except ValueError:
                pass
        invalidIPCount += 1
        invalidIPAddresses.append(ipAddress)
        print(SORRY)

def main():
    # Read router and switch data
    try:
        with open(ROUTER_FILE, "r") as rf:
            routers = json.load(rf)
        with open(SWITCH_FILE, "r") as sf:
            switches = json.load(sf)
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ip in routers.items():
        print("\t" + router + "\t\t" + ip)
    for switch, ip in switches.items():
        print("\t" + switch + "\t\t" + ip)

    while True:
        device = getValidDevice(routers, switches)
        if device == 'x':
            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        if device in routers:
            routers[device] = ipAddress
        else:
            switches[device] = ipAddress

        updated[device] = ipAddress
        devicesUpdatedCount += 1

        print(f"{device} was updated; the new IP address is {ipAddress}")

    # Summary
    print("\nSummary:\n")
    print("Number of devices updated:", devicesUpdatedCount)

    # Write updated devices to file
    try:
        with open(UPDATED_FILE, "w") as uf:
            json.dump(updated, uf, indent=4)
        print(f"Updated equipment written to file '{UPDATED_FILE}'")
    except Exception as e:
        print(f"Failed to write updated devices: {e}")

    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write invalid IPs to file
    try:
        with open(INVALID_FILE, "w") as ef:
            json.dump(invalidIPAddresses, ef, indent=4)
        print(f"List of invalid addresses written to file '{INVALID_FILE}'")
    except Exception as e:
        print(f"Failed to write invalid IP addresses: {e}")

if __name__ == "__main__":
    main()
