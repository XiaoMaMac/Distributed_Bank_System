Logical Clock Written Report

Problem Statement
This project is based on the project 1 to further optimize the distributed bank system. Specifically, given there are communication between different branches on balance replica, it is essential to synchronize the local time (clock) for each branch, so every event is updated and synchronized in every node (branch) in our distributed bank system. This synchronization can be achieved with Lamport’s logical clock.

Goal
The goal of this project is to implement Lamport’s logical clock into the distributed bank system (specifically for branch side). Thus, the order of each subprocess of each event can be directly traced based on this logical clock value.

Setup
This is similar to Project 1.
•	gRPC module in python was used for the customer-branch and branch-branch communications. 
•	grpcio-tools was used to compile .proto file to generated two gRPC related script. 
•	Threading module in python was used for multiprocessing purpose in three parts: 1. All customers can send their requests simultaneously; 2. All branches can process requests simultaneously; 3. The propagation message from one branch to its fellow branches can be sent simultaneously. 
•	Time module in python was used to sleep a process whenever needed. 
•	Input and output files were both in .json format, and json module in python was used to parse the input file and to generate the interim and final output files. 
•	All code was produced in VS code IDE and run with python 3.8.2. 
•	Separate validation has been conducted in Ubuntu 20-04-1 in VMware Fusion. This project was done in macOS Big Sur 11.2.3. 

Implementation Processes
1.	Add the logical clock property to each branch

This is achieved by adding additional property for the branch class. So whenever a branch object is created, it has its own clock value.	
Meanwhile, each object has one additional property as “clockRecord”, which is a list to store “pid” logs and to help generate the final output.

2.	Define a series of class functions to update logical clock

Seven new class functions are defined for logical clock updating:

(1)	eventReceive: Take the parameter of “RemoteClock”; update the local clock to Max (local clock, remote clock) + 1. This is triggered when receiving the gRPC call from customer.

(2)	eventExecute: local clock + 1; This is triggered before local balance replica is changed based on “query”, “withdraw”, or “deposit”.

(3)	propagateSend: local clock + 1 before sending propagation message to one branch. For instance, if there are 3 branches totally, each branch will multicast propagation to 2 other branches, so the local clock will be added for 2 units overall; Like propagation itself, this is only triggered when receiving “withdraw” and “deposit”, but not “query”, request from customer.

(4)	propagateReceive: Take the parameter of “RemoteClock”; update the local clock to Max (local clock, remote clock) + 1; This is triggered when a branch received a propagation message from any other branch. Similarly, if one branch received two propagations from two different branches, the function will be triggered twice overall.

(5)	propoagateExecute: local clock + 1 before updating the balance replica accordingly based on a propagation message received.

(6)	propagateResponse: Take the parameter of “RemoteClock”; update the local clock to Max (local clock, remote clock) + 1; This function is triggered at the branch that initiate the propagation and is triggered to indicate the propagation message has been successfully received and executed at another branch; In a 3 branches example, this function will be triggered twice for each propagation process.

(7)	eventResponse: local clock + 1; This is triggered before sending gRPC response to customer side.   
  
3.	Implementation of these new functions into existing code
The “eventReceive” and “eventResponse” functions are both called within function “MsgDelivery” which is the function handle and response to customer’s gRPC request. All the “remote clocks” on customer side are set to be 1 as default value. For simplicity, I didn’t implement the remote clock into the gRPC message between customer and branch.

The “eventExecute” function is called within functions “Query”, “Withdraw”, and “Deposit” which are the functions to update local balance replica.

The “propagateSend” function is called within functions “Withdraw” and “Deposit” which are the functions to update local balance replica and initiate propagation.
Another related modification is that the gRPC message from branch to branch is now additionally include a clock value. Thus, when one branch calls gRPC to other branches, it will send its local clock value within the request, which will be considered as “remote clock” at other branches. 

The “propagateReceive” function is called within function “propagate” which is the function to handle gRPC request from other branches and update the local balance replica accordingly.
Similar as above, a modification is made on the gRPC response message from branch to branch. The response will now include the local clock value, which will be sent back to the original branch (which initiate this propagation) as “remote clock”.

The “propagateExecute” function is called within function “propagate” which is the function to handle gRPC request from other branches. It is called right before updating local balance replica.

The “propagateResponse” function is called within functions “Withdraw” and “Deposit”. It is called right after the completion of branch-to-branch gRPC process.

4.	Strategy to generate final output

The final output (Final_Output_project2.json) of this project contains two parts: “pid” and “event”. Specifically, with the input example, there are 3 “pid” related information and 2 “event” related information.

To generate final output json file, I first generate 5 interim files.

For each branch, I generate corresponding “pid” logs directly from each branch server based on “clockRecord” object property. So there will be “Output_file_branch1.json”, “Output_file_branch2.json”, “Output_file_branch3.json”.

The generation of “event” logs is a bit complicated, as the information are coming from multiple branch servers. Therefore, I first create an empty json file for each “withdraw” and “deposit” event when receiving request from customer. Specifically, here are “Output_file_event2.json” and “Output_file_event4.json”. And all branch servers will append new logs to this file if the logs are related to corresponding event.

Finally, I have a main script named “Script_for_Final_Output_for_project_2.py”, which will parse all the 5 interim output json files, and generate the final output in a single json file with required format, named “Final_Output_project2.json”. This script was imported and called to run in “Customer.py”.

5.	Sleep() in the process.

To make sure all the clock synchronization processes between branches have been completed, I added sleep for 1 second before generating interim json output.

To make sure all the interim json outputs have been completed before run the script to generate final output. I added sleep for 5 second at the last couple lines in Customer.py.

6.	Run the code

•	In one terminal, run “Branch.py” to start all branch servers.

•	In the second terminal, run “Customer.py” to start customer activities.

•	Wait until the entire process has finished. 


Results
•	The final output is a single json file: “Final_Output_project2.json”.

•	It contains all the subprocesses happened under each branch as individual “pid”. It also contains all the subprocesses happened for each “withdraw” and “deposit” event.

•	Within the logs of each “pid”, the order of subprocesses is listed following the logical clock with values from small to large, reflecting happen-before features.

•	Within the logs of each “event”, the order of subprocesses is listed following the logical clock with values from small to large, reflecting happen-before features.

•	The entire codes has been tested and can be run successfully in Ubuntu OS with VMware.
Final Output:
[
  {
    "pid":1,
    "data":[
      {
        "id":2,
        "name":"deposit_broardcast_request",
        "clock":4
      },
      {
        "id":4,
        "name":"withdraw_broardcast_reqeust",
        "clock":5
      },
      {
        "id":2,
        "name":"deposit_broardcast_execute",
        "clock":6
      },
      {
        "id":4,
        "name":"withdraw_broardcast_execute",
        "clock":7
      }
    ]
  },
  {
    "pid":2,
    "data":[
      {
        "id":2,
        "name":"deposit_request",
        "clock":2
      },
      {
        "id":2,
        "name":"deposit_excute",
        "clock":3
      },
      {
        "id":2,
        "name":"deposit_broadcast_response",
        "clock":8
      },
      {
        "id":4,
        "name":"withdraw_broardcast_reqeust",
        "clock":9
      },
      {
        "id":4,
        "name":"withdraw_broardcast_execute",
        "clock":10
      },
      {
        "id":2,
        "name":"deposit_broadcast_response",
        "clock":12
      },
      {
        "id":2,
        "name":"deposit_response",
        "clock":13
      }
    ]
  },
  {
    "pid":3,
    "data":[
      {
        "id":4,
        "name":"withdraw_request",
        "clock":2
      },
      {
        "id":4,
        "name":"withdraw_excute",
        "clock":3
      },
      {
        "id":4,
        "name":"withdraw_broadcast_response",
        "clock":8
      },
      {
        "id":2,
        "name":"deposit_broardcast_request",
        "clock":9
      },
      {
        "id":2,
        "name":"deposit_broardcast_execute",
        "clock":10
      },
      {
        "id":4,
        "name":"withdraw_broadcast_response",
        "clock":11
      },
      {
        "id":4,
        "name":"withdraw_response",
        "clock":12
      }
    ]
  },
  {
    "eventid":2,
    "data":[
      {
        "clock":2,
        "name":"deposit_request"
      },
      {
        "clock":3,
        "name":"deposit_excute"
      },
      {
        "clock":4,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":6,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":8,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":9,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":10,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":12,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":13,
        "name":"deposit_response"
      }
    ]
  },
  {
    "eventid":4,
    "data":[
      {
        "clock":2,
        "name":"withdraw_request"
      },
      {
        "clock":3,
        "name":"withdraw_excute"
      },
      {
        "clock":5,
        "name":"withdraw_broardcast_reqeust"
      },
      {
        "clock":7,
        "name":"withdraw_broardcast_execute"
      },
      {
        "clock":8,
        "name":"withdraw_broadcast_response"
      },
      {
        "clock":9,
        "name":"withdraw_broardcast_reqeust"
      },
      {
        "clock":10,
        "name":"withdraw_broardcast_execute"
      },
      {
        "clock":11,
        "name":"withdraw_broadcast_response"
      },
      {
        "clock":12,
        "name":"withdraw_response"
      }
    ]
  }
]




Extra Discussions:
There are two issues which may worth discussions in this project:
First issue: 
Though the output is following the happen-before rule and similar to the example output, there are some randomness associated with the order of each subprocesses for each time I run the entire program. For instance, below are results for “event 2” from two different runs:
Run 1:
  {
    "eventid":2,
    "data":[
      {
        "clock":2,
        "name":"deposit_request"
      },
      {
        "clock":3,
        "name":"deposit_excute"
      },
      {
        "clock":4,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":6,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":8,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":9,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":10,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":12,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":13,
        "name":"deposit_response"
      }
    ]
  },
  
  
Run 2:
  {
    "eventid":2,
    "data":[
      {
        "clock":2,
        "name":"deposit_request"
      },
      {
        "clock":3,
        "name":"deposit_excute"
      },
      {
        "clock":4,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":6,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":8,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":9,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":10,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":11,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":12,
        "name":"deposit_response"
      }
    ]
  },
  
I think the difference of clock values between different runs is caused by multi-processing implementations in my code: there are two places in our code I implement multi-processing/multi-thread using threading module: first, when customers sending gRPC request; second, when a branch sending propagation gRPC request.
Because of these two multi-processing steps, related subevents can happen simultaneously or with uncertain happen-before order. 
Second issue:
When generating the final output json file, I can produce it with standard json format. Also I use “indent = 2” argument to enhance readability.
However, I cannot figure out how to control the output into single line.
For example, the output I got for “event2” looks like:
 {
    "eventid":2,
    "data":[
      {
        "clock":2,
        "name":"deposit_request"
      },
      {
        "clock":3,
        "name":"deposit_excute"
      },
      {
        "clock":4,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":6,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":8,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":9,
        "name":"deposit_broardcast_reqeust"
      },
      {
        "clock":10,
        "name":"deposit_broardcast_execute"
      },
      {
        "clock":12,
        "name":"deposit_broadcast_response"
      },
      {
        "clock":13,
        "name":"deposit_response"
      }
    ]
  },

I cannot figure out a way to make the output looks like this:

{
    "eventid":2,
    "data":[
      {"clock":2,"name":"deposit_request"},
      {"clock":3,"name":"deposit_excute"},
      {"clock":4,"name":"deposit_broardcast_reqeust"},
      {"clock":6,"name":"deposit_broardcast_execute"},
      {"clock":8,"name":"deposit_broadcast_response"},
      {"clock":9,"name":"deposit_broardcast_reqeust"},
      {"clock":10,"name":"deposit_broardcast_execute"},
      {"clock":12,"name":"deposit_broadcast_response"},
      {"clock":13,"name":"deposit_response"}
    ]
  },
