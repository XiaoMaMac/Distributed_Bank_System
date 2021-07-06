gRPC Written Report

Problem Statement
[What is the problem statement?]

A bank system needs to handle huge amounts of request from the customers concurrently on daily basis. Furthermore, a bank system may need to establish multiple branches to stratify customers and handle their requests separately, and also to fulfill the needs related to geographical diversity. Therefore, and based on these demands, we are expected to build a distributed system for bank service.  

Goal
[What is the goal of the problem statement?]

We aim to create a distributed bank system with multiple branches which can handle requests from multiple customers concurrently. This system will allow each customer to send requests (query, withdraw, and deposit) to one particular branch and receive the responses. Meanwhile, on the bank side, branch can communicate with all the fellow branches (concurrently) to timely update the balance replica in each branch. All the communications need to be realized with remote procedure call (RPC).

Setup
[What are the relevant technologies for the setup and their versions?]
•	gRPC module in python was used for the customer-branch and branch-branch communications.
•	grpcio-tools was used to compile .proto file to generated two gRPC related script.
•	Threading module in python was used for multiprocessing purpose in three parts: 1. All customers can send their requests simultaneously; 2. All branches can process requests simultaneously; 3. The propagation message from one branch to its fellow branches can be sent simultaneously.
•	Time module in python was used to sleep a process whenever needed.
•	Input and output files were both in .json format, and json module in python was used to parse the input file and to generate the output file.
•	All code was produced in VS code IDE and run with python 3.8.2.
•	Separate validation has been conducted in Ubuntu 20-04-1 in VMware Fusion.
•	This project was done in macOS Big Sur 11.2.3.    

Implementation Processes
[What are the implementation processes?]


a.	Parsing the input file

1.	Input file was given in .json format. 

2.	Using json module to read the input file

3.	Parse the input information, separate the customer information and branch information.

4.	Store customer information in a list customerList, and store branch information in a list branchList. These two lists will be further used in later processes.
 

b.	gRPC setup and scripts design

1.	A bank.proto fille was created in proto3 syntax, which includes two services information. One is the for customer-branch gRPC communication (“MsgDelivery”), another is for branch-branch gRPC communication (“propogate”).

2.	bank.proto file was compiled into bank_pb2.py and bank_pb2_grpc.py files.

3.	A customer script (Bank_Client_Customer.py) and a branch script (Bank_Server_Branch.py) were created.


c.	Customer script

1.	A customer class was defined with properties such as ID, events, etc, which will base on the input information to generate corresponding customer and with specified number.

2.	Within the customer class, a createStub function was implemented, which will allow this customer to iterate his/her event list, create stub and send a request to the corresponding branch for one event (see below port assigning rule for channel information). To minimize the waste of space, each channel will be closed once the gRPC request/response have been completed. Within this createStub function, all the response received from the branch will be stored in destinate format and will be used to generate output .json file in the end of this script.

3.	In the main function, a multi-thread approach was implemented, to iterate all the customers and let them start sending requests simultaneously. All the received information will be collected and written into a .json file in destinate format within current directory.

4.	Port assigning rule (between customer and branch): The communication between customer [‘id’ = X] and branch [‘id’ = X] will be sent via port at ‘localhost (50000 + X)’. 


d.	Branch Script

1.	A function named BranchToBranch was defined to send propagation information from one branch to another. This function will be used later in branch class to allow the sending of requests to all branches (except the current branch) in a multi-thread process. 

2.	A branch class as gRPC servicer was defined with properties such as ID, balance, etc. Three critical functions were defined within class:
•	A function named MsgDelivery was defined to receive the request from customer and return response back to the customer.
•	Function named Withdraw or Deposit (two functions with similar structure), respectively, to decrease or increase the balance replica in this branch and send propagation message to all other fellow branch using BranchToBranch function mentioned above (multi-thread was used here to allow all propagations were sent simultaneously).
•	A function named propagate was defined to let current branch to handle propagation requests sent from all other branches for updating balance replica in current branch.

3.	A function named serve was separately defined to allow the initiation of each branch as a server on gRPC server and to add all the ports needed for communication.  

4.	In the main function, multi-thread was used to allow all the branches will be started simultaneously.

5.	Port assigning rule (between branch and branch): A independent channel was used for the communication from one particular branch to another particular branch (one-direction). For gRPC request send from branch X to branch Y, the channel will be used is ‘localhost (50000 + Y*1000 + X). For example, propagation message sent from branch 1 to branch 2 will be via ‘localhost 52001’, while propagation message sent from branch 2 to branch1 will be via ‘localhost 51002’.


e.	Run the whole project

1.	Put the Input_file.json file in the same directory as all the python scripts.

2.	In a terminal, run python file Bank_Server_Branch.py:
$ python3 Bank_Server_Branch.py      
		
3.	In a different terminal, run python file Bank_Client_Customer.py:
$ python3 Bank_Client_Customer.py

4.	Output results can be found in Output_file.json in the same directory.



Results
[What are the implementation results and their justifications?]

All the implementations were successful. With any input file in proper format, we are able to complete the following:
1.	Successfully parse the input.
2.	All customers can send request concurrently.
3.	Any branch can work independently and adjust it’s own balance replica.
4.	Balance replica in all branches can be updated timely and concurrently.
5.	Directly generate output file in proper format

With given example, on the customer side, information will also be shown to indicate the success of each request:
3 withdraw 330
2 deposit 500
1 query 500
3 query 500
2 query 500

With given example, final output file will be:
{"id": 1, "recv": [{"interface": "query", "result": "success, at branch1", "money": 500}]}
{"id": 2, "recv": [{"interface": "deposit", "result": "success, at branch2"}, {"interface": "query", "result": "success, at branch2", "money": 500}]}
{"id": 3, "recv": [{"interface": "withdraw", "result": "success, at branch3"}, {"interface": "query", "result": "success, at branch3", "money": 500}]}


The project has been tested on Ubuntu 20-04-1 in VMware Fusion and proven to be functional properly.



