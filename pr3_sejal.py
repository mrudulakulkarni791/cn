# Program: Demonstrate Subnetting and find Subnet Mask
# Author: (Your Name)
# Subject: Computer Networks Laboratory

import ipaddress

# Step 1: Take network input in CIDR format
network = input("Enter a network in CIDR format (e.g. 192.168.1.0/24): ")

# Step 2: Create an IPv4 network object
net = ipaddress.ip_network(network, strict=False)

# Step 3: Display subnetting details
print("\n--- Subnetting Details ---")
print("Network Address  :", net.network_address)
print("Subnet Mask      :", net.netmask)
print("Broadcast Address:", net.broadcast_address)
print("Total Hosts      :", net.num_addresses)
print("Usable Hosts     :", net.num_addresses - 2)
print("First Usable IP  :", list(net.hosts())[0])
print("Last Usable IP   :", list(net.hosts())[-1])
print("----------------------------")
