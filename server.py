import socket
import sys
import traceback
from threading import Thread

clients_list  = []      # Keeps the different clients information

def main():
    start_server()


def start_server():
    host = "127.0.0.1"
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        assign_new_client(ip,port,connection)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()



    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    sender_name = find_client_by_port(port)
    print(sender_name)

    while is_active:
        try:
            client_input = receive_input(connection, max_buffer_size)

            if client_input == "quit":
                print("Client is requesting to quit")
                remove_client(port)
                connection.close()
                print("Connection " + ip + ":" + port + " closed")
                print("The list of clients is " + str([client["name"] for client in clients_list]))
                is_active = False
            else:
                print("client_port:"+str(port)+": ",format(client_input['message']))
                try:
                    client_input["client"]["connection"].sendall(("<"+str(sender_name)+">: "+str(client_input["message"])).encode("utf8"))
                    print("Transmission completed")
                except:
                    print("Cannot resolve transmission")
                connection.sendall("-".encode("utf8"))
        except Exception as e:
            print(e)




def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):

    '''
        the input will be composed of two parts
            1 - the destination
            2 - The message
        If any of these two parts is empty, an exception is raised
        if not, we check the destination to see if the referred machine is still present
        then we send the complete sentence to the destination
    '''

    if input_str == "quit":
        return "quit"

    elements = str.split(input_str,"%")
    if len(elements)<3:
        return "Invalid syntax the code is of the form %DESTINATION%MSG"
    destination = elements[1]
    message = elements[2]


    try:
        client = find_client_by_name(destination)
        message_parsed = {"client":client,"message":message}
        return message_parsed
    except Exception:
        raise Exception("Client not found")

# This function adds the newly connected client to the clients list
# It also assigns a name to the client based on its arrival

def assign_new_client(ip,port,connection):
    size_list = len(clients_list)
    client_name = "client_"+str(size_list)
    new_client = {"name":client_name,"ip": ip, "port": port, "connection":connection}
    clients_list.append(new_client)
    size_list += 1
    print("The list of clients is " + str([client["name"] for client in clients_list]))

# Detects the client by port and remove it from the clients list

def remove_client(port):
    client_name = find_client_by_port(port)
    clients_list.pop(find_client_index(client_name))

# This function detects and returns the client details
# it raises an Exception if no corresponding client is found

def find_client_by_name(name_client):
    for i in clients_list:
        if i['name'] == name_client:
            return i
    raise Exception("User not found")

# this function detects and returns the clients name
# It raises an exception if the port is not found

def find_client_by_port(port_client):
    for i in clients_list:
        if i['port'] == port_client:
            return i['name']
    raise Exception("Port not found")

#returns the index on the client

def find_client_index(name_client):
    for i in range(len(clients_list)):
        if(clients_list[i]["name"] == name_client):
            return i




if __name__ == "__main__":
    main()