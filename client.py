import socket
import select
import sys

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")
    message = "Connected to host"

    while message != 'quit':
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, soc]

        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

        for socks in read_sockets:
            if socks == soc:
                message = socks.recv(5120).decode("utf8")
                if message == '-':
                    pass
                else:
                    print(message)
            else:
                message = sys.stdin.readline()
                soc.sendall(message.encode("utf8"))
                sys.stdout.flush()

    soc.close()
    exit()

if __name__ == "__main__":
    main()
