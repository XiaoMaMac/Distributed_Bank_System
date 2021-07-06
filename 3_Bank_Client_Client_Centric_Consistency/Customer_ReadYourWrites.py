from __future__ import print_function
import logging

import grpc

import bank_pb2
import bank_pb2_grpc

import Parsing_Input_json
from Parsing_Input_json import customerList2 as clist

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
        self.outputMonotonicWrites = []
        self.writesets = [0]
    
    def showInfo(self):
        print(self.ID)
        print(self.Event)
        print(self.recvMsg)
        print(self.stub)
    
    def addRecvMsg(self, newRecvMsg):
        self.recvMsg = self.recvMsg + newRecvMsg

    def addMonotonicWritesOutput(self, newOutput):
        self.outputMonotonicWrites = self.outputMonotonicWrites + newOutput

    def createStub(self):
        for event in self.Event:
            channel = grpc.insecure_channel('localhost:{0}'.format(event['dest'] + 50000)) # Customer/Branch 1 will use "50001", Customer/Branch 2 will use "50002", ... , Customer/Branch N will use "5000N".
            stub = bank_pb2_grpc.createStub(channel)
            self.stub = stub

        #for event in self.Event:
            if event['interface'] == 'query':
                response = self.stub.MsgDeliveryRead(bank_pb2.clientRequestRead(ID = self.ID, Interface = event['interface'], LastEventID = self.writesets[len(self.writesets)-1]))
                #toBeAddedMsg = [{'interface':'query', 'result':response.Status, 'money':response.Balance}]
                monotonicWritesMsg = [{'id':self.ID, 'balance':response.Balance}]
                self.addMonotonicWritesOutput(monotonicWritesMsg)

            else:
                response = self.stub.MsgDeliveryWrite(bank_pb2.clientRequestWrite(ID = self.ID, Interface = event['interface'], Money = event['money'], LastEventID = self.writesets[len(self.writesets)-1]))
                #toBeAddedMsg = [{'interface':event['interface'], 'result':response.Status}]

            print(response.AssignedEventID, event['interface'], response.Balance)
        
            #self.addRecvMsg(toBeAddedMsg)

            self.writesets.append(response.AssignedEventID)
        
            channel.close()

            print(self.writesets)


customerList = [] 
for customer in clist:
        newCustomer = Customer(customer['id'], customer['events'])
        customerList.append(newCustomer)


def run(person):
    person.createStub()

#def outputResult():
#    output_json = [] 
#    for person in customerList:
#        output_json.append({'id':person.ID, 'recv':person.recvMsg})
#    return output_json

def MonotonicWritesOutput():
    output_json = []
    for person in customerList:
        output_json.append(person.outputMonotonicWrites)
    return output_json

#def writeJsonResult(result):
#    with open("Output_file_Project1.json", "w") as outputFile:
#        outputFile.write('\n'.join(json.dumps(eachresult) for eachresult in result))

def writeJsonResultMonotonicWrites(result):
    with open("Output_file_Project3readYourWrites.json", "w") as outputFile:
        outputFile.write('\n'.join(json.dumps(eachresult) for eachresult in result))



# This is the main function (ENTRY POINT)!!!
def start():
    logging.basicConfig()  
    
    for person in customerList:   
        t = threading.Thread(target = run, args=(person,))
        t.start()

    t.join()

    # I wait for 3 seconds just to make sure all the threads are completed. (otherwise, I somehow cannot get the last thread...)
    time.sleep(3)

    # Generate the output file for PROJECT 1 as write it into a .json file.
    #outputJsonResult = outputResult()
    #writeJsonResult(outputJsonResult) 

    monotonicWritesResult = MonotonicWritesOutput()
    writeJsonResultMonotonicWrites(monotonicWritesResult)



