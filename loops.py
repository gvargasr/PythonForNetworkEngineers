devices = ['router1', 'router2', 'router3', 'switch1']

for device in devices:
    print(device)


device = {'device': 'router', 'model': '3800', 'os': 'IOS-XE'}

for keys in device.keys():
    print(keys)

for value in device.values():
    print(value)

for item in device.items():
    print(item)