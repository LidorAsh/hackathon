#from os import startfile
import socket
import time
from struct import *
import threading
from scapy.all import *
import random
import queue

def server_program():

    dev = get_if_addr('eth1')
    test = get_if_addr('eth2')

    
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) #UDP
    server.bind((dev, 2005))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = (dev, 2005)
    sock.bind(server_address)
    #sock.settimeout(10)
    # Listen for incoming connections
    sock.listen(2)

    

    while True:    
        global winner 
        winner = 0   


        def waiting():
            t = threading.currentThread()
            print(f"Server started, listening on IP address {server_address[0]}")
            while getattr(t, "do_run", True):
                header = bytes.fromhex('abcddcba') + bytes.fromhex('02') + bytes.fromhex('07D5')
                server.sendto(header, ('<broadcast>', 13117))
                time.sleep(1)




        
        def threaded_clients(id, connection, message, answer, lock, result_queue):
            t = threading.currentThread()
            connection.sendall(str.encode(message))
            data = connection.recv(2048).decode('utf-8')
            lock.acquire()
            result_queue.put((id, data))
            """
            if data == answer:
                #global winner
                #winner = id
                result_queue.put(id*-1)
            
            else:
                #global winner
                #winner = id*-1
                result_queue.put(id)
                """
            lock.release()
           


        th = threading.Thread(target=waiting, args=())
        th.start()

        connection1, client_address1 = sock.accept()
        connection2, client_address2 = sock.accept()
        th.do_run = False
        th.join()

        

        #get the names of the teams
        player1name = connection1.recv(2048).decode('utf-8')
        player2name = connection2.recv(2048).decode('utf-8')

        print("Game begin!")

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
        
        player1.join(10)
        player2.join(10)

        result = q.get()

        #print(result)

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
        else:
            winnername = "Draw"

        """ 
        if winner==1:
            winnername = player1name
        elif winner == -1:
            winnername = player2name
        else:
            winnername = "Draw"
            """

        message = f"\nGame over!\nThe correct answer was {i+j}!\nCongratulations to the winner: {winnername}"
        connection1.send(str.encode(message))
        connection2.send(str.encode(message))

        #sock.close()
        print("Game over, sending out offer requests...")

        



if __name__ == '__main__':
    server_program()
    #m = threading.Thread(target=server_program, args=())
    #m.start()
    #m.join(5)
