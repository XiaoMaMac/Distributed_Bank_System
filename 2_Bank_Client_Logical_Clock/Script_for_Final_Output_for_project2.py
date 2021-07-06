
from Customer import outputResult
import json

import Parsing_Input_json
from Parsing_Input_json import branchList as bList
from Parsing_Input_json import customerList as cList

# Write all codes into a class, so this entire script can be called in Customer.py
class generateFinalOutcomeProject2:
    # Iterate all interim .json files for each branch, and save together
    outputBranchList = []
    for eachOne in bList:
        with open("Output_file_branch{0}.json".format(eachOne['id']), 'r') as inFile:
            outputBranchList.append(json.load(inFile))

    # Iterate all interim .json files for each 'withdraw' or 'deposit' event, and save together
    outputEventList = []
    eventIDList = []
    for eachOne in cList:
        for eachEvent in eachOne["events"]:
            if eachEvent["interface"] != "query":
                with open("Output_file_event{0}.json".format(eachEvent["id"], 'r')) as inFile:
                    outputEventList.append(json.load(inFile))
                    eventIDList.append(eachEvent["id"])


    # Create the list for final output
    FinalOutputProject2 = [] 
    branchIdx = 0
    eventIdx = 0
    for eachBranch in outputBranchList:
        branchIdx += 1
        newElement = {"pid":branchIdx, "data":eachBranch}
        FinalOutputProject2.append(newElement)

    for eachEvent in outputEventList:
        newElement = {"eventid": eventIDList[eventIdx], "data":eachEvent}
        eventIdx += 1
        FinalOutputProject2.append(newElement)    

    # Generate the final output .json file
    with open("Final_Output_Project2.json", 'w') as finalOutput:
        json.dump(FinalOutputProject2, finalOutput, separators=(',',':'), indent=2)
