import json

subnet = "192.168.1"
data = {"ips": [f"{subnet}.{i}" for i in range(1, 255)]}

json_data = json.dumps(data, indent=2)
print(json_data)

