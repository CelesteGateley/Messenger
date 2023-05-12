from socket import *
from threading import Thread
from time import sleep
from tkinter import *

import winsound

current_address = '127.0.0.1'
connect_to = '127.0.0.1'
username = 'Username'
port = 99
sock = socket(AF_INET, SOCK_STREAM)


def listen(addr='127.0.0.1', port='99'):
    sv = socket(AF_INET, SOCK_STREAM)
    sv.bind((addr, port))
    sv.listen(5)
    add_text("Started Listening")
    while True:
        c, addr = sv.accept()
        add_text("Connection Recieved From" + str(addr))
        while True:
            try:
                resp = bytes.decode(c.recv(1024))
            except:
                add_text("CONNECTION TO " + addr[0] + " FORCIBLY CLOSED")
                break
            add_text(resp)
            name_len = len(resp.split(":", 1)[0])
            row_number = int(text_field.index('end-1c').split('.')[0]) - 1
            text_field.tag_add("remote_name", str(row_number) + ".0", str(row_number) + "." + str(name_len))
            root.state('normal')
            winsound.MessageBeep()
            text_field.see('end')
            if resp == 'dc.disconnect()':
                c.send(str.encode("(DISCONNECT REGISTERED. CLOSING CONNECTION)"))
                c.close()
                break


def add_text(x):
    text_field.config(state=NORMAL)
    text_field.insert(END, str(x) + "\n")
    text_field.config(state=DISABLED)


def clear_text():
    input_field.delete(0, 'end')


def start_socket(addr='127.0.0.1', port=99, s=sock):
    connected = False
    tries = 0
    while not connected and tries < 10:
        try:
            s.connect((connect_to, port))
            connected = True
        except:
            tries += 1
            add_text("Connection Failed on Attempt " + str(tries) + ". Retrying in 5 seconds")
            sleep(2)
    if not connected:
        exit(0)


def send_message(event, sock=sock):
    if input_field.get() != "":
        add_text(username + ": " + input_field.get())
        row_number = int(text_field.index('end-1c').split('.')[0]) - 1
        text_field.tag_add("local_name", str(row_number) + ".0", str(row_number) + "." + str(len(username)))
        sock.send(str.encode(username + ": " + input_field.get()))
        clear_text()
        if input_field.get == 'dc.disconnect()':
            add_text(bytes.decode(sock.recv(1024)))
            sock.close()
            exit(0)


root = Tk()  # Root pane of the window
root.title("Messenger Client")  # Sets the title

frame = Frame(root)  # Frame for the text box
frame.pack()  # Adds it to the window
input_line = Frame(root)  # Frame for the input and submit buttons
input_line.pack(side=BOTTOM)  # Adds it to the window

scroll_bar = Scrollbar(frame)  # Scrollbar for the text frame
scroll_bar.pack(side=RIGHT, fill=Y)  # Adds it to the right hand side and fills that side
text_field = Text(frame, yscrollcommand=scroll_bar.set)  # Creates the text window, linking it to the scrollbar
text_field.pack(side=TOP)  # Adds it to the window
text_field.config(state=DISABLED)  # Disables text input
text_field.tag_configure("local_name", foreground="blue")
text_field.tag_configure("remote_name", foreground="red")
scroll_bar.config(command=text_field.yview)  # Tells the scrollbar what to do

input_field = Entry(input_line, width=80)  # Input box for the submission
input_field.bind('<Return>', send_message)
input_field.pack(side=LEFT, fill=X)  # Adds it to the window
submit = Button(input_line, text="Submit", command=lambda: send_message(sock))
submit.pack(side=LEFT)

listener = Thread(target=listen, args=(current_address, 99))

root.after(1000, listener.start)
root.after(2000, lambda: start_socket(connect_to, port))
root.mainloop()
