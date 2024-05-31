import csv

data = [['Hostname', 'Vendor', 'Model', 'Location'], 
        ['sw10', 'Cisco', '3800', 'Miami'], 
        ['sw11', 'Cisco', '3650', 'Atlanta']]

with open('newdevices.csv', 'w') as f:
    devices = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in data:
        devices.writerow(row)

with open('newdevices.csv', 'r') as f:
    print(f.read())
