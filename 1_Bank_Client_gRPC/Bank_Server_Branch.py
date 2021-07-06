from concurrent import futures
import logging
from os import close
from google.protobuf import message

import grpc

# Import gRPC related files
import bank_pb2
import bank_pb2_grpc

# Import the parsing results from input file. The BRANCH information are particularly needed here.
import Parsing_Input_json
from Parsing_Input_json import branchList as bList

# Import other modules needed here.
import time
import threading



# I generally defined this function for propagation between two branches (from branchA to branchB), so I can conduct multiprocessing later for propogation.
#def BranchToBranch (branchA, branchB, money, eventID, interface):
#    # To exclude propagate to this branch itself.
#    if branchA.ID != branchB['id']:
#                # Use unique port for each branch-to-branch communication. This is acheived by using mathmatic formula taking account branch IDs.
#                with grpc.insecure_channel('localhost:{0}'.format(50000 + branchA.ID + branchB['id']*1000)) as channel:
#                    stub = bank_pb2_grpc.createStub(channel)
#                    response = stub.propagate(bank_pb2.BranchRequest(ID = branchA.ID, EventID = eventID, Interface = interface, Money = money))
#                    # Save the response message from other branches.
#                    branchA.recvMsg = branchA.recvMsg + [response]
#                # Close the port after request completion.
#                channel.close()



# Define the class of branch, which are all gRPC servicers.
class Branch(bank_pb2_grpc.createServicer):

    def __init__(self, ID, Balance):
        # Branch ID.
        self.ID = ID
        # The initial balance replica in this branch. 
        self.Balance = Balance
        # Recived message from other branches.
        self.recvMsg = []
        # I DID NOT store the stublist from customer, which seems not needed in my program here.
    
    def BranchToBranchIn (self, branchB, money, eventID, interface):
        # To exclude propagate to this branch itself.
        if self.ID != branchB['id']:
                    # Use unique port for each branch-to-branch communication. This is acheived by using mathmatic formula taking account branch IDs.
                    with grpc.insecure_channel('localhost:{0}'.format(50000 + self.ID + branchB['id']*1000)) as channel:
                        stub = bank_pb2_grpc.createStub(channel)
                        response = stub.propagate(bank_pb2.BranchRequest(ID = self.ID, EventID = eventID, Interface = interface, Money = money))
                        # Save the response message from other branches.
                        self.recvMsg = self.recvMsg + [response]
                    # Close the port after request completion.
                    channel.close()


    # I defined a query function just to keep it consistent in structure.
    def Query(self):
        pass
    

    # Withdraw function: Descrease the balance replica of this branch, and propagate the information to other branches.
    def Withdraw(self, Money1, eventID):
        self.Balance -= Money1

        # Send branch-to-branch request via gRPC to all branches except this branch itself. Use different channel for different communication.
        for eachother in Parsing_Input_json.branchList:
            # BranchToBranch function is defined at the beginning of this script.
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money1, eventID, 'withdraw'))
            t.start()
        t.join()



    # Deposit function: Increase the balance replica of this branch, and propagate the information to other branches.
    # The design is similar to Withdraw function.
    def Deposit(self, Money2, eventID):
        self.Balance += Money2

        for eachother in Parsing_Input_json.branchList:
            t = threading.Thread(target = self.BranchToBranchIn, args=(eachother, Money2, eventID, 'deposit'))
            t.start()
        t.join()

    
    # I combined "Branch.Propagate_Withdraw" and "Branch.Propagate_Deposit" into one function.
    # Propagate function, taking the gRPC request from other branches.
    def propagate(self, request, context):
        # Based on event interface, update accordingly. Return message includes eventID and ID of this branch.
        if request.Interface == 'withdraw':
            self.Balance -= request.Money
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID))
        
        elif request.Interface == 'deposit':
            self.Balance += request.Money
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID))
        
        # Propagtion of 'query' will do nothing.
        elif request.Interface == 'query':
            return bank_pb2.updateResponse(BResponse = 'Event {0}, successfully updated in branch {1}'.format(request.EventID, self.ID))


    # MsgDelivery function will take the gRPC request from the corresponding customer, take branch process accordingly.
    def MsgDelivery(self, request, context):

        # Based on customer request per event, initiate different branch process. 
        if request.Interface == 'query':
            # As requested in this project, 'query' request will wait 3 seconds to make sure completion of branch-to-branch propagation.
            time.sleep(3)
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID)) # I include the branch ID into "Status" (will be shown in output file) for better clarity.

        elif request.Interface == 'withdraw':
            # Initiate Withdraw function and pass Money and EventID.
            self.Withdraw(request.Money, request.EventID)
            return bank_pb2.branchResponse(ID = request.ID, Balance = self.Balance, Status = 'success, at branch{0}'.format(self.ID)) # I include the branch ID into "Status" (will be shown in output file) for better clarity.

        elif request.Interface == 'deposit':
            # Initiate Deposit function and pass Money and EventID.
            self.Deposit(request.Money, request.EventID)
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
