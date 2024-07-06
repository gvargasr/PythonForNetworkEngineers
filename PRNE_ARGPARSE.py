import argparse

text = "This program takes input for router information"
parser = argparse.ArgumentParser(description=text)
parser.add_argument("-R", "--router", help="Enter Router Name")
parser.add_argument("-IP", help="Enter ip address")

router = parser.parse_args()

print(f"The router name is {router.router} with ip address {router.IP}")
