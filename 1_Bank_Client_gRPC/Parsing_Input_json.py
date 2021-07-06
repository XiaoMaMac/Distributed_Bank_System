
import json

with open("Input_File.json") as inputFile:
    InputF = json.load(inputFile)

# To save customer information and branch information into separate lists for later use.
customerList = []
branchList = []

for i in range(len(InputF)):
    if InputF[i]["type"] == "customer":
        customerList.append(InputF[i])
    elif InputF[i]["type"] == "branch":
        branchList.append(InputF[i])


# Code below were used to assure the proper parsing of input during code writing.

#print(len(customerList))
#print(len(branchList))
    
#print(customerList[0]['id'])
#print(customerList)