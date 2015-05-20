# chat_server.py
 
import sys, socket, select, os, datetime

SOCKET_LIST = []
RECV_BUFFER = 1024
name_list = ['server']
offTom = ''
offPeter = ''
offJohn = ''
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if (socket != server_socket and socket != sock) :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if (socket in SOCKET_LIST):
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":

    __author__='Boris'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 3003))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
    
    print ('Server started!')
 
    while 1:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        read_sockets,write_sockets,error_sockets = select.select(SOCKET_LIST,[],[],0)
      
        for sock in read_sockets:
            #print('1')
            # a new connection request recieved
            if (sock == server_socket): 
                sc, sockname = server_socket.accept()
                SOCKET_LIST.append(sc)
                #broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
                #print('2\n')
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                  
                    if data:
                        dedata = data.decode("utf-8")
                        #print(dedata)
                        userpwd = dedata.split(' ')
                        if (userpwd[0] == 'Tom'):
                             if(userpwd[1] == '0615'):
                                  name_list.append('Tom')
                                  sock.sendall(str.encode("Client Tom connects success!\n"+offTom))
                                  offTom = ''
                             else:
                                  SOCKET_LIST.remove(sock)
                        elif (userpwd[0] == 'Peter'):
                             if(userpwd[1] == '0616'):
                                  name_list.append('Peter')
                                  sock.sendall(str.encode("Client Peter connects success!\n"+offPeter))
                                  offPeter = ''
                             else:
                                  SOCKET_LIST.remove(sock)
                        elif (userpwd[0] == 'John'):
                             if(userpwd[1] == '0617'):
                                  name_list.append('John')
                                  sock.sendall(str.encode("Client John connects success!\n"+offJohn))
                                  offJohn = ''
                             else:
                                  SOCKET_LIST.remove(sock)

                        elif (userpwd[0] == 'listuser'):
                             sock.sendall(str.encode(str(name_list)))

                        elif (userpwd[0] == 'send'):
                             flag = 0
                             isoff = 0
                             for i in name_list:
                                 buff=' '
                                 if(userpwd[1] == i):
                                     isoff = 1
                                     num = 2
                                     while(num < (len(userpwd)-1)):
                                           buff = buff + userpwd[num] + ' '
                                           num += 1
                                     buff = userpwd[len(userpwd)-1] + ' says:'+ buff
                                     SOCKET_LIST[flag].sendall(str.encode(buff))
                                 flag += 1
                             if(isoff == 0 ):
                                 buff = ''
                                 num = 2
                                 while(num < (len(userpwd)-1)):
                                     buff = buff + userpwd[num] + ' '
                                     num += 1
                                 buff = userpwd[len(userpwd)-1] + ' says:'+ buff

                                 if(userpwd[1] == 'Tom'):
                                     offTom = buff
                                 elif(userpwd[1] == 'Peter'):
                                     offPeter = buff
                                 elif(userpwd[1] == 'John'):
                                     offJohn[1] = buff
                                 else:
                                     print('You have wrong ID.\n')
                        elif (userpwd[0] == 'logout'):
                             SOCKET_LIST.remove(sock)
                             name_list.remove(userpwd[1])
                             print(userpwd[1]+ ' is logout.\n')
                        elif (userpwd[0] == 'broadcast'):
                             buff = ''
                             num = 1
                             while(num < (len(userpwd)-1)):
                                  buff = buff + userpwd[num] + ' '
                                  num += 1
                             buff = userpwd[len(userpwd)-1] + ' broadcast says : '+ buff
                             broadcast(server_socket,sock,str.encode(buff))
                        # there is something in the socket
                        # print "Broadcast all!"
                        #broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    
                        # at this stage, no data means probably the connection has been broken
                       # broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    print('')  
   
      
