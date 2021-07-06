from __future__ import print_function
import logging

import grpc

import bank_pb2
import bank_pb2_grpc

import Parsing_Input_json
from Parsing_Input_json import customerList as clist

import json
import threading
import time

# For better readibility, I removed all comments in project1, only show comments related to project 2, to reflect my modification here.
class Customer:
    def __init__(self, ID, Event):
        self.ID = ID
        self.Event = Event
        self.recvMsg = []
        self.stub = None
    
    def showInfo(self):
        print(self.ID)
        print(self.Event)
        print(self.recvMsg)
        print(self.stub)
    
    def addRecvMsg(self, newRecvMsg):
        self.recvMsg = self.recvMsg + newRecvMsg

    def createStub(self):
        channel = grpc.insecure_channel('localhost:{0}'.format(self.ID + 50000)) # Customer/Branch 1 will use "50001", Customer/Branch 2 will use "50002", ... , Customer/Branch N will use "5000N".
        stub = bank_pb2_grpc.createStub(channel)
        self.stub = stub

        for event in self.Event:
            response = self.stub.MsgDelivery(bank_pb2.clientRequest(ID = self.ID, EventID = event['id'], Interface = event['interface'], Money = event['money']))
            print(response.ID, event['interface'], response.Balance)
            
            toBeAddedMsg = [{'interface':'query', 'result':response.Status, 'money':response.Balance}]
            toBeAddedMsg2 = [{'interface':event['interface'], 'result':response.Status}]
            
            if event['interface'] == 'query':
                self.addRecvMsg(toBeAddedMsg)
            else: self.addRecvMsg(toBeAddedMsg2)
        
        channel.close()


customerList = [] 
for customer in clist:
        newCustomer = Customer(customer['id'], customer['events'])
        customerList.append(newCustomer)


def run(person):
    person.createStub()

def outputResult():
    output_json = [] 
    for person in customerList:
        output_json.append({'id':person.ID, 'recv':person.recvMsg})
    return output_json

def writeJsonResult(result):
    with open("Output_file_Project1.json", "w") as outputFile:
        outputFile.write('\n'.join(json.dumps(eachresult) for eachresult in result))




# This is the main function (ENTRY POINT)!!!
if __name__ == '__main__':
    logging.basicConfig()  
    
    for person in customerList:   
        t = threading.Thread(target = run, args=(person,))
        t.start()

    t.join()

    # I wait for 3 seconds just to make sure all the threads are completed. (otherwise, I somehow cannot get the last thread...)
    time.sleep(3)

    # Generate the output file for PROJECT 1 as write it into a .json file.
    outputJsonResult = outputResult()
    writeJsonResult(outputJsonResult) 

    # To genereate final output for PROJECT 2. I wait for 5s, just to make sure all processes on the Branch side have been completed.
    time.sleep(5)
    # import the script for generating finaloutput for project2.
    import Script_for_Final_Output_for_project2
    # call the class function in another script and generate the final output for PROJECT 2.
    Script_for_Final_Output_for_project2.generateFinalOutcomeProject2()


