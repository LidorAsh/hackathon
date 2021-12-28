#from os import startfile
import socket
import struct
import time
from struct import *
import threading
import scapy.all as scapy
import random
import queue


def server_program():

    dev = scapy.get_if_addr('eth1')
    test = scapy.get_if_addr('eth2')
    tcp_port = 2005

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #UDP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.bind((dev, 13117)) #can delete this line
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("", tcp_port)) #change this to dev
    # Listen for incoming connections
    sock.listen(2) 

    player1name, player2name = '', ''
    connection1, connection2 = None, None

    magic_cookie = 0xabcddcba
    offer_msg_type = 0x2

    while True:  
        time.sleep(1)
        def waiting():
            t = threading.currentThread()
            print(f"Server started, listening on IP address {dev}")
            header = struct.pack('!IbH', magic_cookie, offer_msg_type, tcp_port)
            
            #header = bytes.fromhex('abcddcba') + bytes.fromhex('02') + bytes.fromhex('07D5')
            while getattr(t, "do_run", True):
                server.sendto(header, ('<broadcast>', 13117))
                time.sleep(1)


        def threaded_clients(id, connection, message, answer, lock, result_queue):
            #time.sleep(1)
            try:
                connection.sendall(str.encode(message))
                data = connection.recv(2048).decode('utf-8')
                #if data != "0":
                lock.acquire()
                result_queue.put((id, data))
                lock.release()
            except ConnectionError:
                return
           


        th = threading.Thread(target=waiting, args=())
        th.start()

        if(connection1 == None):
            connection1, client_address1 = sock.accept()
            print("Player 1 connected")

        if(connection2 == None):
            connection2, client_address2 = sock.accept()
            print("Player 2 connected")
        th.do_run = False
        th.join()
        
                  
        #get the names of the teams
        if len(player1name) == 0:
            player1name = connection1.recv(2048).decode('utf-8')
            if len(player1name) == 0:   
                print("Player 1 has disconnected, looking for another player...")   
                connection1 = None

        
        if len(player2name) == 0:
            player2name = connection2.recv(2048).decode('utf-8')
            if len(player2name) == 0:
                print("Player 2 has disconnected, looking for another player...")
                connection2 = None

        
        if (connection1 == None) or (connection2 == None):
            continue


        print("Game begin!")
        print("Player 1: "+player1name)
        print("Player 2: "+player2name)

        i = random.randint(1,5)
        j = random.randint(1,4)

        message = f"""\nWelcome to Quick Maths.\nPlayer 1: {player1name}\nPlayer 2: {player2name}\n==\nPlease answer the following question as fast as you can:\nHow much is {i}+{j}?"""

        q = queue.Queue()
        lock = threading.Lock()
        player1 = threading.Thread(target=threaded_clients, args=(1, connection1, message, i+j, lock, q))
        player2 = threading.Thread(target=threaded_clients, args=(-1, connection2, message, i+j, lock, q))

        time.sleep(10)
        player1.start()
        player2.start()


        try:
            result = q.get(timeout=10)
            if result[0]==1:
                if int(result[1]) == i+j:
                    winnername = player1name
                else:
                    winnername = player2name

            elif result[0] == -1:
                if int(result[1]) == i+j:
                    winnername = player2name
                else:
                    winnername = player1name
        
        except:
            result = (0,0)
            winnername = "Draw"


        message = f"\nGame over!\nThe correct answer was {i+j}!\nCongratulations to the winner: {winnername}"
        try:       
            connection1.send(str.encode(message))
        except:
            print(f"Disconnected Player:{player1name}")

        try:
            connection2.send(str.encode(message))
        except:
            print(f"Disconnected Player:{player2name}")

        
        connection1, connection2= None, None
        player1name, player2name = '', ''
        print("Game over, sending out offer requests...")

        

if __name__ == '__main__':
    server_program()
