from tkinter import *
from socket import *
from threading import Thread
from time import sleep
import winsound

curraddr = gethostname()
connaddr = '127.0.0.1'
username = 'Username'
port = 99
s = socket(AF_INET, SOCK_STREAM)
roomID = 0
compID = 0



def listen(addr='127.0.0.1', port='99'):
    sv = socket(AF_INET, SOCK_STREAM)
    sv.bind((addr, port))
    sv.listen(5)
    addtext("Started Listening")
    while True:
        c,addr = sv.accept()
        addtext("Connection Recieved From" + str(addr))
        while True:
            try:
                resp = bytes.decode(c.recv(1024))
            except:
                addtext("CONNECTION TO " + addr[0] + " FORCIBLY CLOSED")
                break
            addtext(resp)
            name_len = len(resp.split(":",1)[0]) 
            row_number = int(txtField.index('end-1c').split('.')[0])-1
            txtField.tag_add("remote_name", str(row_number)+".0", str(row_number)+"."+str(name_len))
            root.state('normal')
            winsound.MessageBeep()
            txtField.see('end')
            if resp == 'dc.disconnect()':
                c.send(str.encode("(DISCONNECT REGISTERED. CLOSING CONNECTION)"))
                c.close()
                break

def addtext(x):
    txtField.config(state=NORMAL)
    txtField.insert(END, str(x) + "\n")
    txtField.config(state=DISABLED)

def cleartxt():
    inputField.delete(0, 'end')

def startsocket(addr='127.0.0.1', port=99, s=s):
    connected = False
    tries = 0
    while not connected and tries < 10:
        try:
            s.connect((connaddr, port))
            connected = True
        except:
            tries += 1
            addtext("Connection Failed on Attempt " + str(tries) + ". Retrying in 5 seconds")
            sleep(2)
    if not connected:
        exit(0)

def sendmsg(event, sock=s):
    if inputField.get() != "":
        addtext(username + ": " + inputField.get()) 
        row_number = int(txtField.index('end-1c').split('.')[0])-1
        txtField.tag_add("local_name", str(row_number)+".0", str(row_number)+"."+str(len(username)))
        sock.send(str.encode(username + ": " + inputField.get()))
        cleartxt()
        if inputField.get == 'dc.disconnect()':
            addtext(bytes.decode(s.recv(1024)))
            s.close()
            exit(0) 

def makeip():
    global compID
    try:
        int(compNoInp.get())
    except:
        return False
    compID = compNoInp.get()

    
root = Tk()                                                 #Root pane of the window
root.title("Messenger Client")                              #Sets the title

frame = Frame(root)                                         #Frame for the text box
frame.pack()                                                #Adds it to the window
inpline = Frame(root)                                       #Frame for the input and submit buttons
inpline.pack(side=BOTTOM)                                   #Adds it to the window

selframe = Frame(root)


compNoInp = Entry(selframe, width=80)
compNoInp


scrollbar = Scrollbar(frame)                                #Scrollbar for the text frame
scrollbar.pack(side=RIGHT, fill=Y )                         #Adds it to the right hand side and fills that side
txtField = Text(frame, yscrollcommand=scrollbar.set)        #Creates the text window, linking it to the scrollbar
txtField.pack(side=TOP)                                     #Adds it to the window
txtField.config(state=DISABLED)                             #Disables text input
txtField.tag_configure("local_name", foreground="blue")
txtField.tag_configure("remote_name", foreground="red")
scrollbar.config(command=txtField.yview )                   #Tells the scrollbar what to do

inputField = Entry(inpline, width=80)                       #Input box for the submission
inputField.bind('<Return>', sendmsg)
inputField.pack(side=LEFT, fill=X)                          #Adds it to the window
submit = Button(inpline, text="Submit", command= lambda: sendmsg(s))
submit.pack(side=LEFT)


listener = Thread(target=listen, args=(curraddr, 99))

root.after(1000, listener.start)
root.after(2000, lambda: startsocket(connaddr, port))
root.mainloop()






