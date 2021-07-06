Client-Centric Consistency Written Report

Problem Statement
In a distributed system, multiple replications for shared data exist to improve the performance and reliability of the entire system. An important perspective is to keep all the replications consistent with certain restriction, which is typically achieved by propagation for any write, usually not for read, operations. However, any propagation process takes time. Thus, if the same client makes operations on different replicas within a short time, there is a possibility that the propagation is slower than as expected and this client may see or work on conflict data content on different replications. To solve this issue, a client-centric consistency design may need to be implemented into the distributed system.    

Goal
To implement client-centric consistency design into our previously built distributed bank system. Specifically, we aim to achieve the consistency of both “monotonic-writes” and “read-your-writes”.

Setup
This is similar to Project 1 and Project 2 (setup unique to Project 3 are highlighted).
1.	gRPC module in python was used for the customer-branch and branch-branch communications. 
2.	grpcio-tools was used to compile .proto file to generated two gRPC related script. 
3.	Threading module in python was used for multiprocessing purpose in three parts: 1. All customers can send their requests simultaneously (in Project 3 here, we only need to deal with one customer); 2. All branches can process requests simultaneously; 3. The propagation message from one branch to its fellow branches can be sent simultaneously. 
4.	Time module in python was used to sleep a process whenever needed. 
5.	Random module in python was used to assigning ID to each event.
6.	Input and output files were both in .json format, and json module in python was used to parse the input file and to generate final output files. 
7.	All code was produced in VS code IDE and run with python 3.8.2. 
8.	Separate validation has been conducted in Ubuntu 20-04-1 in VMware Fusion. This project was done in macOS Big Sur 11.2.3. 

Implementation Processes
1.	Allow one customer to send request to any branch (bank)
In our previous system, for branch with ID “X”, we opened a port with number 50000 + X to receive request from customer side. For instance, branch 1 will listen to request sent to 50001.
To make a single customer can send request to any branch, we take advantage of “dest” within “events” in the input file. For each event, the request will be sent to port 50000 + “dest”.

2.	Maintain a “writesets” for each customer and each branch
For customer side, we added a new class property named “writesets” which is a list of number of event ID.
Similarly, for branch side, we added a new class property named “writesets” which is a list of number of event ID.
In each writesets, we gave an initial element “0”. This is because the gRPC request between customer and branch will now include an event ID number (see below). Therefore, we may need a value for the very first customer request, in order to avoid an error.

3.	Generate a random ID for each event on branch side
We use random.randint() on the branch side to assigned a random ID to any event received from the customer side. The range of event ID was arbitrarily set to be 0 – 10000.
To avoid the duplication in the event ID, we will compare the newly generated ID to current writesets to make sure there is no duplication. The actual code looks like below:
while True:
            newEventID = random.randint(0, 10000)
            if newEventID not in self.writesets:
                break
This implementation can be found in MsgDeliveryRead() and MsgDeliveryWrite() functions.

4.	Propagation, response, and maintain of event ID for customer and branch
Once the ID has been generated for event, it will be tied to this event for any customer and branch. And this ID will be appended to writesets of all customers and branches.

Event ID in propagation: The event ID was implemented into the gRPC call between branch and branch. Therefore, whenever a branch generates an event ID, it will propagate the ID to all its fellow branches.

Event ID in response: The event ID was also implemented into the gRPC response between customer and branch. So, when the destination branch sends back the gRPC response, it also sends the event ID back to customer. 

Maintaining event ID: The event ID will be kept essentially everywhere. This is achieved by append the new event ID into the writesets of destination branch, fellow branches, and customer. So eventually, the writesets among all branches will be the same. Importantly, the event ID will be appended to the writesets of this branch only after this branch has completed the operation. So when we check any branch’s writesets, if we see an event ID, we know that that event has been completed at this branch.

5.	Implementation of “monotonic writes” and “read your writes”
We used an implementation similar to a “lock” to achieve this goal.
When a customer sends a request to a destination branch, it also send the last element in his/her writesets, which represent the ID of his/her last event.
Then the destination branch receives this ID and will first check if this ID is in its writesets. If the ID is in the writesets, the branch will continue to perform the request; if the ID is not in the writesets (which means the previous propagation for this event has not been completed), this branch will hold the request and wait until the corresponding propagation to be finished before performing the request. Specifically, this is achieved by code below:
while True:
            if request.LastEventID in self.writesets:
                break
      The was implemented in both MsgDeliveryRead() and MsgDeliveryWrite(), so the entire system will realize both monotonic writes and read you writes.


6.	Scripts for two input files
A script has been written to handle input file related to “monotonic writes”, which is named “Customer_MonotonicWrites.py”.
Another script has been written to handle input file related to “read your writes”, which is named “Customer_ReadYourWrites.py”.
Finally, a main script has been written to import and run both abovementioned scripts. The final script is named “Customer_MainScript.py”.

7.	Run Project 3
•	In a terminal, run “Branch.py”
•	In a different terminal, run “Customer_MainScript.py”
•	Wait until all processes to be completed
•	The final output for “monotonic writes” can be found in “Output_file_Project3monotonicWrites.json”; the final output for “read your writes” can be found in “Output_file_Project3readYourWrites.json”
      

Results
1.	Monotonic writes can be achieved.
This output can be found in “Output_file_Project3monotonicWrites.json”.
With the given input file, the output will be looking like below:
[{"id": 1, "balance": 0}]
This indicates that for customer 1, his/her “withdraw” operation on branch 2 was happened after his/her previous “deposit” operation on branch 1.

2.	Read your writes can be achieved.
This output can be found in “Output_file_Project3readYourWrites.json”.
With the given input file, the output will be looking like below:
[{"id": 1, "balance": 400}]
This indicates that for customer 1, his/her “query” operation on branch 2 was happened after his/her pervious “deposit” operation on branch 1.

3.	Tracing the processes in real-time. 
During the running of the project, I particularly let the terminal print out the branch ID and the real-time writesets on branch side, to trace the success updates on writesets.
For example, the branch terminal will record:

bank1, [0, 22]
bank2, [0, 22, 2724]
bank2, [0, 22, 2724, 4929]
bank1, [0, 22, 2724, 8567]
bank2, [0, 22, 2724, 4929, 8567, 534]

The customer terminal will print out the event ID, operation, money and real-time writesets for this customer:

22 deposit 400
[0, 22]
2724 withdraw 0
[0, 22, 2724]
4929 query 0
[0, 22, 2724, 4929]

8567 deposit 400
[0, 8567]
534 query 400
[0, 8567, 534]
By tracing these information, we can visualize how each ID has been generated for each event, and how this ID was gradually added to the writesets for branches or customers.
4.	The entire code has been tested on Ubuntu, and proven to be functional properly.

