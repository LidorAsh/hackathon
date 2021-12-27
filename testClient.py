import socket
import struct
import sys, select
from struct import *


def client_program():
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(('<broadcast>', 13117))
        #client.connect(("", 13117))
        
        

        print("Client started, listening for offer requests... ")
        while True:
            try:
                data, addr = client.recvfrom(1024)
                (magicCookie, msg_type, server_port) = struct.unpack('!IbH', data)
                #Check the message format:
                if magicCookie == 0xabcddcba:
                    if msg_type == 0x2:
                        dest_port = int.from_bytes(data[5:7],"big")
                        SERVER_ADDR = (addr[0],server_port)
                        break
            except:
                print("connection failed " + str(addr[0]))

        
        
            
        print(f"Received offer from {SERVER_ADDR[0]}, attempting to connect...")
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.connect(SERVER_ADDR)
        
        try:
            # Send the name of the team
            sock.sendall(str.encode("Instinct\n"))

            # welcoming message
            data = sock.recv(2048).decode('utf-8')
            print(data)

            #send the answer
            i, o, e = select.select( [sys.stdin], [], [], 10 )
            if (i):
                answer = sys.stdin.readline().strip()
            else:
                answer = "0"
                
            sock.sendall(str.encode(answer))

            data = sock.recv(2048).decode('utf-8')
            print(data)


        except ConnectionError:
            print("Server disconnected, listening for offer requests...")
            sock.close()
                


if __name__ == '__main__':
    client_program()