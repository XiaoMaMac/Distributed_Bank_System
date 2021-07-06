from __future__ import print_function
import logging

import grpc

# Import the gRPC related files.
import bank_pb2
import bank_pb2_grpc

# Import the parsing results from initial .json input file. We particularly need the CUSTOMER infomation here)
import Parsing_Input_json
from Parsing_Input_json import customerList as clist

# Import other modules which will be needed here.
import json
import threading
import time


# Define the class for customers.
class Customer:
    def __init__(self, ID, Event):
        # Customer's ID.
        self.ID = ID
        # The event(s) of this customer, which should be a list.
        self.Event = Event
        # The message recieved from corresponding branch. I also use this list to generate output file.
        self.recvMsg = []
        # Save the last stub this customer has used.
        self.stub = None
    
    # I used this function to check the status of each customer during my coding.
    def showInfo(self):
        print(self.ID)
        print(self.Event)
        print(self.recvMsg)
        print(self.stub)
    
    # I used this function to collect messege from branch. 
    def addRecvMsg(self, newRecvMsg):
        self.recvMsg = self.recvMsg + newRecvMsg

    # This function will let this customer create a stub to send request to corresponding branch, execute the request, and save the recieved message.
    # I combined the customer.createStub and customer.excuteEvents into ONE function here, so I got proper handle on the port's open&close.
    def createStub(self):
        channel = grpc.insecure_channel('localhost:{0}'.format(self.ID + 50000)) # Customer/Branch 1 will use "50001", Customer/Branch 2 will use "50002", ... , Customer/Branch N will use "5000N".
        stub = bank_pb2_grpc.createStub(channel)
        # Save the current stub to object property.
        self.stub = stub

        # Iterate the event lists for this customer, and send MsgDelivery request to corresponding branch.
        for event in self.Event:
            response = self.stub.MsgDelivery(bank_pb2.clientRequest(ID = self.ID, EventID = event['id'], Interface = event['interface'], Money = event['money']))
            # Print key inform for checking progress.
            print(response.ID, event['interface'], response.Balance)
            # Create the received message from branch into output formats. 
            toBeAddedMsg = [{'interface':'query', 'result':response.Status, 'money':response.Balance}]
            toBeAddedMsg2 = [{'interface':event['interface'], 'result':response.Status}]
            # The output format for 'query' is a bit different from 'withdraw' and 'deposit'. 
            if event['interface'] == 'query':
                self.addRecvMsg(toBeAddedMsg)
            else: self.addRecvMsg(toBeAddedMsg2)
        # Close the channel.
        channel.close()


# Create all customers based on input file.
customerList = [] 
for customer in clist:
        newCustomer = Customer(customer['id'], customer['events'])
        customerList.append(newCustomer)


# Create a function to send customer request. I used this function in multi-thread design. 
def run(person):
    person.createStub()


# Define the function to create the output data.
def outputResult():
    output_json = [] 
    for person in customerList:
        output_json.append({'id':person.ID, 'recv':person.recvMsg})
    return output_json
# Function to write the output data as .json file with required format.
def writeJsonResult(result):
    with open("Output_file.json", "w") as outputFile:
        outputFile.write('\n'.join(json.dumps(eachCustomer) for eachCustomer in result))




# This is the main function (ENTRY POINT)!!!
if __name__ == '__main__':
    logging.basicConfig()  
    
    # Send each person's events to corresponding branch simultaneously by multi-thread.
    for person in customerList:   
        t = threading.Thread(target = run, args=(person,))
        t.start()

    # Sychronous all threads after completion of gRPC process.
    t.join()

    # I wait for 3 seconds just to make sure all the threads are completed. (otherwise, I somehow cannot get the last thread...)
    time.sleep(3)

    # Generate the output file as write it into a .json file.
    outputJsonResult = outputResult()
    writeJsonResult(outputJsonResult) 


