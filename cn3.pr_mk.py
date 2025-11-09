# Program: Subnetting and Finding Subnet Masks
# Equivalent to Subnet1.java

import ipaddress

def main():
    # Input from user
    ip = input("ENTER IP: ")

    # Extract first octet to determine class
    first_octet = int(ip.split('.')[0])
    mask = None

    # Determine class and assign default subnet mask
    if first_octet >= 1 and first_octet <= 126:
        ip_class = "Class A IP Address"
        mask = "255.0.0.0"
    elif first_octet >= 128 and first_octet <= 191:
        ip_class = "Class B IP Address"
        mask = "255.255.0.0"
    elif first_octet >= 192 and first_octet <= 223:
        ip_class = "Class C IP Address"
        mask = "255.255.255.0"
    elif first_octet >= 224 and first_octet <= 239:
        ip_class = "Class D IP Address (Used for Multicasting)"
        mask = "255.0.0.0"
    elif first_octet >= 240 and first_octet <= 254:
        ip_class = "Class E IP Address (Experimental Use)"
        mask = "255.0.0.0"
    else:
        print("Invalid IP Address")
        return

    print(ip_class)
    if ip_class.startswith("Class A") or ip_class.startswith("Class B") or ip_class.startswith("Class C"):
        print("SUBNET MASK:", mask)

    # Compute Network and Broadcast address
    try:
        # Convert IP and mask to network object
        network = ipaddress.IPv4Network(ip + '/' + mask, strict=False)
        print("First IP of block (Network Address):", network.network_address)
        print("Last IP of block (Broadcast Address):", network.broadcast_address)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
