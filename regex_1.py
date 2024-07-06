import re

DATA = "xyz785abc5xy2"
PATTERN = r"[abc][1-7]"
match = re.search(PATTERN, DATA)
if match:
    print(match.group())
else:
    print("No match found")
