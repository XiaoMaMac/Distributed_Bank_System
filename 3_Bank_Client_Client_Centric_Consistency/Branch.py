from concurrent import futures
import logging
from os import close
from google.protobuf import message

import grpc

import bank_pb2
import bank_pb2_grpc

import Parsing_Input_json
from Parsing_Input_json import branchList as bList

import time
import threading
import json

import random


class Branch(bank_pb2_grpc.createServicer):

    def __init__(self, ID, Balance):
        self.ID = ID
        self.Balance = Balance
        self.recvMsg = []
        self.clock = 1
        self.clockRecord = []    
    # Add the writesets to each branch
        self.writesets = [0]


# Function to initial branch to branch propogation.
    def BranchToBranchIn (self, branchB, money, eventID, interface, clockA):
        if self.ID != branchB['id']:
                    with grpc.insecure_channel('localhost:{0}'.format(50000 + self.ID + branchB['id']*1000)) as channel:
                        stub = bank_pb2_grpc.createStub(channel)
                        response = stub.propagate(bank_pb2.BranchRequest(ID = self.ID, AssignedEventID = eventID, Interface = interface, Money = money, Clock = clockA))
                        self.recvMsg = self.recvMsg + [response]
                    channel.close()


    def Query(self, eventID):
        pass
        
    def Withdraw(self, Money1, eventID):   
        self.Balance -= Money1
        for eachother in Parsing_Input_json.branchList:
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money1, eventID, 'withdraw', self.clock))
            t.start()
            t.join()

    def Deposit(self, Money2, eventID):
        self.Balance += Money2
        for eachother in Parsing_Input_json.branchList:
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money2, eventID, 'deposit', self.clock))
            t.start()
            t.join()


# the function to handle propagation request from other branches
    def propagate(self, request, context):
        if request.Interface == 'withdraw':
        # update local balance replica
            self.Balance -= request.Money
        # update the branch writesets
            self.writesets.append(request.AssignedEventID)
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.AssignedEventID, self.ID), BClock = self.clock)
    # 'deposit' is similar to 'withdraw'
        elif request.Interface == 'deposit':
            self.Balance += request.Money
            self.writesets.append(request.AssignedEventID)
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.AssignedEventID, self.ID), BClock = self.clock)
    # Propagtion of 'query' will do nothing, but will update branch writesets
        elif request.Interface == 'query':
            self.writesets.append(request.AssignedEventID)
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.AssignedEventID, self.ID), BClock = self.clock)



# MsgDelivery function will take the gRPC request from the customer, take branch process accordingly.
    def MsgDeliveryRead(self, request, context):
        
        # This while loop serve as a lock to achieve both Monotonic Writes and Read-Your-Writes 
        while True:
            if request.LastEventID in self.writesets:
                break

        # This while loop is to assigned a random ID to each events, and make sure event ID is not duplicated
        while True:
            newEventID = random.randint(0, 10000)
            if newEventID not in self.writesets:
                break
        
        # Excute the read function
        self.Query(newEventID)
        # Update the branch writesets.
        self.writesets.append(newEventID)
        
        # Do not need the sleep for 3 secs in project now, since we have read-your-writes implementated
        #time.sleep(3)
        
        # Print a status on terminal, to check if everything works well so far 
        print('bank{0}, {1}'.format(self.ID, self.writesets))
        return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID), AssignedEventID = newEventID) # I include the branch ID into "Status" (will be shown in output file) for better clarity.

    def MsgDeliveryWrite(self, request, context):

        # This while loop serve as a lock to achieve both Monotonic Writes and Read-Your-Writes 
        while True:
            if request.LastEventID in self.writesets:
                break

        # This while loop is to assigned a random ID to each events, and make sure event ID is not duplicated
        while True:
            newEventID = random.randint(0, 10000)
            if newEventID not in self.writesets:
                break

        if request.Interface == 'withdraw':
        # Excute the Withdraw function
            self.Withdraw(request.Money, newEventID)
        # Update the branch writesets
            self.writesets.append(newEventID)
        # Do not need this sleep I put in project 2 now, since we have monotonic write implemented
        # Sleep for 1 sec to wait for all propoagation process to be finished
            #time.sleep(1)
            print('bank{0}, {1}'.format(self.ID, self.writesets))
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID), AssignedEventID = newEventID) # I include the branch ID into "Status" (will be shown in output file) for better clarity.

    # 'deposit' is similar to 'withdraw'
        elif request.Interface == 'deposit':
        # Excute the Deposit function
            self.Deposit(request.Money, newEventID)
        # Update the branch writesets
            self.writesets.append(newEventID)
        # Do not need this sleep I put in project 2 now, since we have monotonic write implemented
            #time.sleep(1) 
            print('bank{0}, {1}'.format(self.ID, self.writesets))
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID), AssignedEventID = newEventID) # I include the branch ID into "Status" (will be shown in output file) for better clarity.


# Define the function to create each branch as gRPC server, and add all the ports needed.
# Take a parameter "eachbranch", so I can iterate the branch list to create all of them.
def serve(eachbranch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_createServicer_to_server(Branch(eachbranch['id'], eachbranch['balance']), server)
    # This port is to communicate with customer.
    server.add_insecure_port('[::]:{0}'.format(50000 + eachbranch['id']))
    # To add unique port to each fellow branch except this branch itself.
    for eachother in bList:
        if eachbranch['id'] != eachother['id']:
            server.add_insecure_port ('[::]:{0}'.format(50000 + eachbranch['id']*1000 + eachother['id']))
    # Start the server, and wait until mannual termination
    server.start()
    server.wait_for_termination()





# This is the main function (ENTRY POINT)!!!
if __name__ == '__main__':
    logging.basicConfig()
    
    # Iterate the input branch list, start all the branches. Using multi-thread to keep all branch working simultaneously. 
    for eachbranch in bList:
      t = threading.Thread(target = serve, args=(eachbranch,))
      t.start()
