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



# I removed all previous comments for project 1, only highlight comments for the new code in project 2.
class Branch(bank_pb2_grpc.createServicer):

    def __init__(self, ID, Balance):
        self.ID = ID
        self.Balance = Balance
        self.recvMsg = []
    # adding the property of clock for each branch.
        self.clock = 1
    # adding the property of clockRecord to log all clock related process to generate output files.
        self.clockRecord = []



# define a series if sub-interface for project 2.
    def eventReceive(self, RemoteClock):
            self.clock = max(self.clock, RemoteClock) + 1
    
    def eventExecute(self):
        self.clock += 1
    
    def propagateSend(self):
        self.clock += 1
    
    def propagateReceive(self, RemoteClock):
        self.clock = max(self.clock, RemoteClock) + 1
    
    def propagateExecute(self):
        self.clock += 1
    
    def propagateResponse(self, RemoteClock):
        self.clock = max(self.clock, RemoteClock) + 1

    def eventResponse(self):
        self.clock += 1



# Function to initial branch to branch propogation.
    def BranchToBranchIn (self, branchB, money, eventID, interface, clockA):
        if self.ID != branchB['id']:
                    with grpc.insecure_channel('localhost:{0}'.format(50000 + self.ID + branchB['id']*1000)) as channel:
                        stub = bank_pb2_grpc.createStub(channel)
                        response = stub.propagate(bank_pb2.BranchRequest(ID = self.ID, EventID = eventID, Interface = interface, Money = money, Clock = clockA))
                        self.recvMsg = self.recvMsg + [response]
                    # process propagate Response
                        self.propagateResponse(response.BClock)
                    # log this process
                        if interface != 'query':
                            self.clockRecord = self.clockRecord + [{"id":eventID, "name":"{0}_broadcast_response".format(interface), "clock":self.clock}]
                            self.appendEventOutput("Output_file_event{0}.json".format(eventID), [{"clock":self.clock, "name":"{0}_broadcast_response".format(interface)}])
                    channel.close()



# Function to update the output .json file for each event
    def appendEventOutput(self, jsonFile, newRecord):
        with open(jsonFile, "r") as appendFile:
            currentData = json.load(appendFile)
        
        currentData = currentData + newRecord

        with open(jsonFile, "w") as newFile:
            json.dump(currentData, newFile, indent=6)



    def Query(self, Money, eventID):
    # process eventExecute for any local query. There is no propagation for query.
        self.eventExecute()
        
    def Withdraw(self, Money1, eventID):
    # process eventExecute for any local withdraw
        self.eventExecute()    
    # log the process
        self.clockRecord = self.clockRecord + [{"id":eventID, "name":"withdraw_excute", "clock":self.clock}]
        self.appendEventOutput("Output_file_event{0}.json".format(eventID), [{"clock":self.clock, "name":"withdraw_excute"}])

        self.Balance -= Money1

        for eachother in Parsing_Input_json.branchList:
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money1, eventID, 'withdraw', self.clock))
            t.start()
            t.join()

    def Deposit(self, Money2, eventID):
    # process eventExecute for any local deposit
        self.eventExecute()
    # log the process
        self.clockRecord = self.clockRecord + [{"id":eventID, "name":"deposit_excute", "clock":self.clock}]
        self.appendEventOutput("Output_file_event{0}.json".format(eventID), [{"clock":self.clock, "name":"deposit_excute"}])

        self.Balance += Money2
        
        for eachother in Parsing_Input_json.branchList:
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money2, eventID, 'deposit', self.clock))
            t.start()
            t.join()



# the function to handle propagation request from other branches
    def propagate(self, request, context):
    
    # process the propagateReceive
        self.propagateReceive(request.Clock)
        
        if request.Interface == 'withdraw':
        # log the process
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"withdraw_broardcast_reqeust", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"withdraw_broardcast_reqeust"}])
        # process the propagateExecute    
            self.propagateExecute()
        # log the process
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"withdraw_broardcast_execute", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"withdraw_broardcast_execute"}])
        # update local balance replica
            self.Balance -= request.Money
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID), BClock = self.clock)
        
    # 'deposit' is similar to 'withdraw'
        elif request.Interface == 'deposit':
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"deposit_broardcast_request", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"deposit_broardcast_reqeust"}])
            
            self.propagateExecute()
            
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"deposit_broardcast_execute", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"deposit_broardcast_execute"}])
            
            self.Balance += request.Money
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID), BClock = self.clock)

    # Propagtion of 'query' will do nothing, but will process propagateExecute
        elif request.Interface == 'query':
            self.propagateExecute()
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID), BClock = self.clock)



# MsgDelivery function will take the gRPC request from the corresponding customer, take branch process accordingly.
    def MsgDelivery(self, request, context):
    # Assume the default clock on all customer side is 1
        remoteClock = 1
    # Process the eventReveive
        self.eventReceive(remoteClock)

        if request.Interface == 'query':
        # Process the eventExecute
            self.Query(request.Money, request.EventID)
            time.sleep(3)
        # Process the eventResponse
            self.eventResponse()
        # Generate the interim .json output for branch received 'query request' (branch 1)
            with open("Output_file_branch{0}.json".format(self.ID), "w") as outputFile:
                json.dump(self.clockRecord, outputFile, indent=6)
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID)) # I include the branch ID into "Status" (will be shown in output file) for better clarity.


        elif request.Interface == 'withdraw':
        # log the process
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"withdraw_request", "clock":self.clock}]
            eventOutput = [{"clock":self.clock, "name":"withdraw_request"}]
        # Generate the interim .json output for each 'withdraw' event
            with open("Output_file_event{0}.json".format(request.EventID), "w") as outputFile:
                json.dump(eventOutput, outputFile, indent=6)
            self.Withdraw(request.Money, request.EventID)
        # Sleep for 1 sec to wait for all propoagation process to be finished
            time.sleep(1)
        # Process the eventResponse
            self.eventResponse()
        # log the process
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"withdraw_response", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"withdraw_response"}])
        # Generate the interim .json output for each branch received 'withdraw' request (branch 3).
            with open("Output_file_branch{0}.json".format(self.ID), "w") as outputFile:
                json.dump(self.clockRecord, outputFile, indent=6)
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID)) # I include the branch ID into "Status" (will be shown in output file) for better clarity.

    # 'deposit' is similar to 'withdraw'
        elif request.Interface == 'deposit':
            
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"deposit_request", "clock":self.clock}]
            eventOutput = [{"clock":self.clock, "name":"deposit_request"}]
            with open("Output_file_event{0}.json".format(request.EventID), "w") as outputFile:
                json.dump(eventOutput, outputFile, indent=6)
            self.Deposit(request.Money, request.EventID)
            time.sleep(1) 
            self.eventResponse()
            
            self.clockRecord = self.clockRecord + [{"id":request.EventID, "name":"deposit_response", "clock":self.clock}]
            self.appendEventOutput("Output_file_event{0}.json".format(request.EventID), [{"clock":self.clock, "name":"deposit_response"}])

            with open("Output_file_branch{0}.json".format(self.ID), "w") as outputFile:
                json.dump(self.clockRecord, outputFile, indent=6)
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID)) # I include the branch ID into "Status" (will be shown in output file) for better clarity.


# Define the function to create each branch as gRPC server, and add all the ports needed.
# Take a parameter "eachbranch", so I can iterate the branch list to create all of them.
def serve(eachbranch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    bank_pb2_grpc.add_createServicer_to_server(Branch(eachbranch['id'], eachbranch['balance']), server)
    
    # This port is to communicate with corresponding customer.
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
