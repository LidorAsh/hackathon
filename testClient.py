import socket
import struct
import sys, select
from struct import *
import threading


def client_program():
    udp_port = 13117

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        client.bind(("", udp_port))
        
        

        print("Client started, listening for offer requests... ")
        while True:
            try:
                data, addr = client.recvfrom(1024)
                (magicCookie, msg_type, server_port) = struct.unpack('IbH', data)
                #Check the message format:
                if magicCookie == 0xabcddcba:
                    if msg_type == 0x2:
                        SERVER_ADDR = (addr[0],server_port)
                        #SERVER_ADDR = ("172.99.0.8",2008)
                        print(f"Received offer from {SERVER_ADDR[0]}, attempting to connect...")
                        # Create a TCP/IP socket
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                        sock.connect(SERVER_ADDR)
                        print(f"Connected to server {SERVER_ADDR[0]}.")                    
                        break
            except:
                continue


        
        try:
            print("Please wait.")
            # Send the name of the team
            sock.sendall(str.encode("The Saviors\n"))

            # welcoming message
            data = sock.recv(2048).decode('utf-8')
            print(data)

            #send the answer
            def add_input():
                i, o, e = select.select( [sys.stdin], [], [], 10 )
                if(i):
                    sock.sendall(str.encode(sys.stdin.readline()[0].strip()))

            input_thread = threading.Thread(target=add_input, args=())
            input_thread.daemon = True
            input_thread.start()
        
            data = sock.recv(2048).decode('utf-8')
            print(data)
                              


        except ConnectionError:
            print("Server disconnected, listening for offer requests...")
            sock.close()
                


if __name__ == '__main__':
    client_program()