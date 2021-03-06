# chat_client.py

import sys, socket, select, string, os

def get_passpw():
    os.system("stty -echo") 
    hiddenpss = input ('passwd:')
    os.system("stty echo")
    return hiddenpss

def main_client():
   
    host = '140.123.102.181'
    port = 3003
    istalk = 0
    talkwho =''
    initlog = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect\n')
        sys.exit()
     
    print ('Connected to remote host. You can start sending messages\n')
    user = input('user:')
    pwd = get_passpw()
 
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(1024)
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    tmp = data.decode('utf-8')
                    temp =tmp.split()
                    if(temp[len(temp)-1] == 'talknow'):
                        istalk = 1
                        talkwho =str(temp[0])
                        buff=''
                        num=2
                        while(num < (len(temp)-1)):
                            buff = buff + temp[num] + ' '
                            num += 1
                        #buff = temp[len(temp)-1] + ' says:'+ buff
                        print(buff)
                    else:
                        print(data.decode('utf-8'))
                    
            
            else :
                # user entered a message
                if(initlog == 0):
                    userpwd = user + ' ' + pwd
                    s.send(str.encode(userpwd))
                    initlog = 1
                else:
                    msg = input('')
                    boxa = msg.split()
                    if(msg == 'exit talk'):
                        istalk = 0
                        talkwho = ''
                    if (istalk == 1):
                        s.send(str.encode('send '+ talkwho +' '+ msg + ' talknow '+ user ))
                    else:
                        if(msg == 'listuser'):
                           s.send(str.encode('listuser '+user))
                        elif (msg == 'logout'):
                           s.send(str.encode('logout '+user))
                           sys.exit()
                        elif (msg[0:9] == 'broadcast'):
                           s.send(str.encode(msg + ' ' + user))
                        elif(msg[0:4] == 'send'):
                           s.send(str.encode(msg + ' ' + user))
                        elif(msg[0:4] == 'talk'):
                           #s.send(str.encode(msg + ' ' + user))
                           istalk = 1
                           talkwho = boxa[1]

if __name__ == "__main__":

    sys.exit(main_client())

