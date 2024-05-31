import csv

# with open('device.csv', 'r') as file:
#     devices = csv.reader(file)
#     header = next(devices)
#     print(f'Headers: {header}')
#     for row in devices:
#         print(row)

with open('device.csv', 'r') as f:
    devices = csv.DictReader(f)
    for row in devices:
        print(row)
        print(row['Hostname'], row['Model'])
        print('-------------------------------------------------------------')