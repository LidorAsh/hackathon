import socket
import sys


def client_program():
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", 13117))
        
        

        print("Client started, listening for offer requests... ")
        data, addr = client.recvfrom(1024)
        header = data[:5]
        message = data[7:].decode('utf-8') #The message
        #print(addr[0])
        address = addr[0]
        
        #SERVER_ADDR = (0,0)
        #Check the message format:
        if header == bytes.fromhex('abcddcba') + bytes.fromhex('02'):
            dest_port = int.from_bytes(data[5:7],"big")
            #print(dest_port)
            #print(address)
            SERVER_ADDR = (address,dest_port)

    
        
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            #server_address = (addr[0], dest_port)
            print(f"Received offer from {SERVER_ADDR[0]}, attempting to connect...")
            sock.connect(SERVER_ADDR)
            print("Connected! Please wait for more instructions.")
            
            try:
                # Send the name of the team
                name = input("Enter name:")
                sock.sendall(str.encode(name))

                # welcoming message
                data = sock.recv(2048).decode('utf-8')
                print(data)

                #send the answer
                answer = input()
                sock.sendall(str.encode(answer))

                data = sock.recv(2048).decode('utf-8')
                print(data)


            finally:
                print("Server disconnected, listening for offer requests...")
                sock.close()
                

    

    """
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    #client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) ##################
    #client_socket.bind(('',13117))###########################

    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
    """


if __name__ == '__main__':
    client_program()