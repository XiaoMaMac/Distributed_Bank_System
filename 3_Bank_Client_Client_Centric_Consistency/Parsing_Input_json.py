
import json

# Parsing Input_File_Monotonic_Writes.json
with open("Input_File_Monotonic_Writes.json") as inputFile:
    InputF = json.load(inputFile)

customerList = []
branchList = []

for i in range(len(InputF)):
    if InputF[i]["type"] == "customer":
        customerList.append(InputF[i])
    elif InputF[i]["type"] == "bank":
        branchList.append(InputF[i])



# Parsing Input_File_ReadYourWrites.json
with open("Input_File_ReadYourWrites.json") as inputFile:
    InputF2 = json.load(inputFile)

customerList2 = []
branchList2 = []

for i in range(len(InputF2)):
    if InputF2[i]["type"] == "customer":
        customerList2.append(InputF2[i])
    elif InputF2[i]["type"] == "bank":
        branchList2.append(InputF2[i])



# Code below were used to assure the proper parsing of input during code writing.

#print(len(customerList))
#print(len(branchList))
    
#print(customerList[0]['events'])
#print(customerList)

#print(len(customerList2))
#print(len(branchList2))
    
#print(customerList2[0]['events'])
#print(customerList2)