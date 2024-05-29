ip =  '192.168.0.1'
subnet = '255.255.255.252'

if subnet.endswith('.0'):
    subnet_slash_notation = '/24'
    # print(ip + subnet_slash_notation)
elif subnet.endswith('.128'):
    subnet_slash_notation = '/25'
elif subnet.endswith('.192'):
    subnet_slash_notation = '/26'
elif subnet.endswith('.224'):
    subnet_slash_notation = '/27'
elif subnet.endswith('.240'):
    subnet_slash_notation = '/28'
elif subnet.endswith('.248'):
    subnet_slash_notation = '/29'
elif subnet.endswith('.252'):
    subnet_slash_notation = '/30'
elif subnet.endswith('.255'):
    subnet_slash_notation = '/32'
else:
    print('Subnet slash notation could not be determined')

print(ip + subnet_slash_notation)

