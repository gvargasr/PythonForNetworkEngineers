import yaml

with open('first.yml', 'r') as file:
    data = yaml.safe_load(file)
user = data['users']['user2']
print(data)
print(type(data))
print(user['name'])
for role in user['roles']:
    print(role)

user['location']['city'] = 'Dallas'
with open('firstYaml-edited.yml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)