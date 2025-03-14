import sys
import codecs
import random
import re
import json

dir = "./lease_database.json"
encoding = "utf-8"

macaddress = sys.argv[1] #xx-xx-xx-xx-xx-xx
method = sys.argv[2]

MAC_ADDRESS_PATTERN = r'^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$'

predifined_ipv6_subnet = [ # 2001:db8::/64
    '2001', # 2001
    '0db8', # 0db8
    '0000', # 0000
    '0000', # 0000
    ]

predifined_ipv4_subnet = [ # 192.168.1.0/24
    '192','168','1'
]

isValid = True
if re.match(MAC_ADDRESS_PATTERN, macaddress):
    isValid = True
else:
    isValid = False

print(f"<h3>MAC Address: {macaddress}</h3>")
print(f"<h3>DHCP Version: DHCP{method}</h3>")

if isValid:

    with open(dir, mode="rt", encoding="utf-8") as f:
        lease_database = json.load(f)

        # Generate IPv6 Address (if DHCPv6 selected)
        ## Uses the EUI-64 format to generate an IPv6 address based on the MAC address
        ## Assigns the address from a predefined IPv6 subnet
        if method == "v6":
            # add "FFFE"
            macaddresslist = macaddress.split("-")
            macaddresslist.insert(3,"ff") #xx-xx-xx-ff-xx-xx-xx
            macaddresslist.insert(4,"fe") #xx-xx-xx-ff-fe-xx-xx-xx

            # Invert the 7th bit from the beginning
            firstHexOfMacStr = macaddresslist[0]
            firstHexOfMac = bytes.fromhex(firstHexOfMacStr) # to hex
            firstHexOfMacToBinary = int(firstHexOfMac.hex(), base=16) 
            reverse7bitBin = firstHexOfMacToBinary ^ 0b00000010 

            # reverse to hex and combine for Ipv6 InterfaceID
            reversed7bitFirstHex = format(reverse7bitBin,'x') 
            macaddresslist[0] = reversed7bitFirstHex 

            # conbine subnet and InterfaceID
            ipv6 = predifined_ipv6_subnet
            for idx in range(0, len(macaddresslist), 2):
                hexes = macaddresslist[idx:idx+2]
                ipv6.append(f"{hexes[0]}{hexes[1]}")

            ipv6Str = ":".join(ipv6)

            # Checks if an IP is already assigned to the given MAC address (reuse existing lease).
            leaseIpv6List = lease_database["ipv6"]
            if ipv6Str in leaseIpv6List:
                print("<div style='color:green;'>This IP has already assigned.</div>")
            else:
                leaseIpv6List.append(ipv6Str)
                print(lease_database)
                with open(dir, mode="wt", encoding="utf-8") as f:
                    json.dump(lease_database, f, ensure_ascii=False, indent=2)
            
            print("<h2>Result</h2>")
            print(f"<h3>MAC Address: {macaddress}</h3>")
            print(f"<h3>ASSIGNED ip{method}: {ipv6Str}</h3>")

            print(f"<div>lease database: {leaseIpv6List}</div>")

        else:
            # Ensures that available IPs exist in the selected subnet; otherwise, returns an error.
            leaseIpv4List = lease_database["ipv4"]

            if len(leaseIpv4List) >= 254:
                print("<h3 style='color:red;'>No IP address available for assignment</h3>")
            else:
                ipv4Str = ""
                while True:
                    ipv4 = []
                    octetOf4th = str(random.randint(1, 254))
                    for subnet in predifined_ipv4_subnet:
                        ipv4.append(subnet)
                    ipv4.append(octetOf4th)
                    ipv4Str = ".".join(ipv4)

                    if not ipv4Str in leaseIpv4List:
                        break 
                
                leaseIpv4List.append(ipv4Str)
                with open(dir, mode="wt", encoding="utf-8") as f:
                    json.dump(lease_database, f, ensure_ascii=False, indent=2)


                print("<h2>Result</h2>")
                print(f"<h3>MAC Address: {macaddress}</h3>")
                print(f"<h3>ASSIGNED ip{method}: {ipv4Str}</h3>")
                print(f"<h3>LEASE TIME: 3600 seconds</h3>")

                print(f"<div>lease database: {leaseIpv4List}</div>")

else:
    print(f"<h2 style='color:red;'>MAC address format is invalid.</h2>")
    print(f"<h3 style='color:red;'>Please type MAC address XX-XX-XX-XX-XX-XX (X is hex string)</h3>")
