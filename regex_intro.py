import re  # 1 import re module

PATTERN = r"GigabitEthernet[1-4]"  # 2 Regex pattern
INTERFACE = "interface GigabitEthernet2 ip address 10.11.0.1 255.255.255.0"

pattern2 = "[abc][123]"
data2 = "abc123cba321"

result = re.search(PATTERN, INTERFACE)
result2 = re.search(pattern2, data2)
result3 = re.findall(pattern2, data2)
result4 = re.split(pattern2, data2)

print(result)
print(result2)
print(result3)
print(result4)
