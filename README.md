# Threaded, server monitored, client to client communication
---

## Introduction

The focus of this project was to develop a simple topology associating a server to at least three clients simultaneously and enable communication among them following a particular instruction format. The project was entirely realized using python 3 and runs perfectly on the command line. The goal of the project was to understand the interactions between the client and the server and improve our knowledge concerning the socket programming. It is a good experience to understand how a server can interconnect many machines and enable transformation and exchange of information between them.

## Design and concept description

### Multithreading

The concept of multithreading refers to a type of execution model that enables multiple threads to exist within the context of a process such that they execute independently but share their process resources. A thread maintains a list of information relevant to its execution including the priority schedule, exception handlers, a set of CPU registers, and stack state in the address space of its hosting process.

### Sockets Programming

Each machine possesses a wide array of sockets that can be used to establish communication and receive information from other machines. Some sockets are already preassigned to specific functions and protocols and cannot be used for establishing a non-conventional connection to other machines. Nonetheless, the available sockets can be used to establish the communication using the Python program developed specially for it.


### How do the server and clients use sockets?

Sockets allow communication between two different processes on the same or different machines. To be more precise, it's a way to talk to other computers using standard Unix file descriptors. In Unix, every I/O action is done by writing or reading a file descriptor. A file descriptor is just an integer associated with an open file and it can be a network connection, a text file, a terminal, or something else.

The server possesses multiple sockets that can be used at any time by any client to communicate with the server. The problem is that the server cannot communicate with all of the clients sequentially as he does not know which client will fire an instruction first or the timeframe of the communication between each client. The server cannot “watch” all sockets at the same time in sequential architecture. That is why the communication requires threading to be optimal.

In effect, with threading, the server will now be listening simultaneously to all the different ports and associate an execution thread to each of them without interrupting the thread execution of the other one. Hence each communication between a client and the server is independent of the other. But another question arises. If each client is connected to the server with a threaded connection independent of the other, how to send information to the other client?

### Client to client communication

Every time a client establishes a connection with the server, an execution thread is created to enable an uninterrupted exchange of information between the client and the server. One important detail is to understand that the client uses a single thread with the server, its main execution feed. Therefore, any he listens to the server as if he was the only one connected to the server. This means that an instruction not associated with the thread the server generated for the specific client can still go through and be received by the client by simply specifying that the message should be sent to the connection port of the client.

In summary, a client will send instructions to the server. The server will listen to the instructions on the thread he defined for the client. If the instructions are valid, the server will process the different instructions. The instructions should be sent to the right client after processing. The server will simply look for the connection entity related to the other client and simply use them, still within the execution thread of the first client, and deliver the message to the destination client.

## Results

As you can see in the first part of the program, the server accepts connection from different clients. Also, it saves every information concerning the saved client along with the communication. Among that information, we can find the port, the socket, the IP address and the connection instance (python object used to enable communication between the server and the client).

The different clients can communicate with each other using the format ```%client_name%message.``` The server will then look in the list of associated clients information and send the message to the right client. In the case the communication cannot be established or the client defined is not valid, an error message is printed in the server.

## Conclusion

The threading associated with the socket programming enables us to understand how servers can handle multiple requests at the same time without hindering their potential. The server can associate an execution thread to each client connected and provide information upon request of each. The development was done using Python due to its simplicity and the amount of code used to define the different functionalities.

---

## Annex

#### How to operate

To launch, simply use the command 

 > ```$    python3 server.py```

To run any client, just use the command 
 > ```$    python3 client.py```

Each client requires the same command. Up to 5 clients can
work simultaneously.

#### Links:

- https://www.techopedia.com/definition/24297/multithreading-computer-architecture
- https://www.geeksforgeeks.org/socket-programming-cc/


