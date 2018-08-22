from classes import *
from tkinter import ttk
from tkinter import *
import json
from _thread import start_new_thread
from tkinter.ttk import *
class Calculator:

    def __init__(self, master):

        self.master = master
        master.title("Boibot vs Eviebot vs Cleverbot")
        self.master.geometry("375x400")
        self.status_label_text = IntVar()
        self.status_label_text.set("Status")
        self.status_label = Label(master, textvariable=self.status_label_text)

        self.label1_label_text = IntVar()
        self.label1_label_text.set("Bot #1")
        self.label1_label = Label(master, textvariable=self.label1_label_text)

        self.label2_label_text = IntVar()
        self.label2_label_text.set("Bot #2")
        self.label2_label = Label(master, textvariable=self.label2_label_text)

        self.bot1_mode = IntVar()

        self.radio1=Radiobutton(self.master, text="Cleverbot", variable= self.bot1_mode, value=1)
        self.radio2=Radiobutton(self.master, text="Eviebot", variable= self.bot1_mode, value=2)
        self.radio3=Radiobutton(self.master, text="BoiBot", variable= self.bot1_mode, value=3)
        self.bot2_mode = IntVar()
        self.radio4=Radiobutton(self.master, text="Cleverbot", variable=self.bot2_mode, value=1)
        self.radio5=Radiobutton(self.master, text="Eviebot", variable=self.bot2_mode, value=2)
        self.radio6=Radiobutton(self.master, text="BoiBot", variable=self.bot2_mode, value=3)


        self.label3_label_text = IntVar()
        self.label3_label_text.set('Entry message.\n You can use JSON to provide list  \n ["elo","siema","heloł"]')
        self.label3_label = Label(master, textvariable=self.label3_label_text)
        #vcmd = master.register(self.start) # we have to wrap the command
        self.entry = Text(master, width=40, height=3)

        self.label4_label = Label(master, text="length of conversation")
        self.lenght = Entry(master, width=40)

        self.label5_label = Label(master, text="# of simultaneous conversations")
        self.amount = Entry(master, width=40)

        self.start_button = Button(master, text="Start", command=lambda: self.start())


        # LAYOUT

        self.label1_label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.status_label.grid(row=0, column=2, columnspan=1, sticky=N)

        self.radio1.grid(row=1, column=0, columnspan=1, sticky=E)
        self.radio2.grid(row=1, column=1, columnspan=1, sticky=E)
        self.radio3.grid(row=1, column=2, columnspan=1, sticky=E)

        self.label2_label.grid(row=2, column=0, columnspan=3,pady=(10,2),sticky=W)

        self.radio4.grid(row=3, column=0, columnspan=1, sticky=E)
        self.radio5.grid(row=3, column=1, columnspan=1, sticky=E)
        self.radio6.grid(row=3, column=2, columnspan=1, sticky=E)

        self.label3_label.grid(row=4, column=0, columnspan=3,pady=(10,2),sticky=N)
        self.entry.grid(row=5, column=0, columnspan=3)

        self.label4_label.grid(row=6, column=0, columnspan=3,pady=(10,2),sticky=N)
        self.lenght.grid(row=7, column=0, columnspan=3)

        self.label5_label.grid(row=8, column=0, columnspan=3,pady=(10,2),sticky=N)
        self.amount.grid(row=9, column=0, columnspan=3)

        self.start_button.grid(row=10, column=0, columnspan=3)




    def start(self):
        msg=self.entry.get("1.0", END)
        start_new_thread(self.go,(self.bot1_mode,self.bot2_mode,int(self.amount.get()), int(self.lenght.get()),msg))


    def go(self,bot1,bot2,amount,lenght,msg):

        for i in range(amount):
            msg_list=[]
            if '[' in msg and ']' in msg:
                msg_list = json.loads(msg)

            bot1=None
            if self.bot1_mode.get()==1:
                bot1 = CleverBot()
            elif self.bot1_mode.get()==2:
                bot1=Existor("evie")
            elif self.bot1_mode.get()==3:
                bot1=Existor("boi")

            bot2=None
            if self.bot2_mode.get()==1:
                bot2 = CleverBot()
            elif self.bot2_mode.get()==2:
                bot2=Existor("evie")
            elif self.bot2_mode.get()==3:
                bot2=Existor("boi")
            con=Conversation(bot1,bot2)
            if len(msg_list)>0:
                msg=choice(msg_list)
            else:
                msg=msg
            con.start(lenght=lenght,start=msg)
            con.save_history_to_file("hist3_"+str(i)+".txt")
            con.end()

root = Tk()
my_gui = Calculator(root)
root.mainloop()
"""
randy = [
    "Kocham cię",
    "Nazywasz się Arek?!!!",
    "Gdzie mieszkasz kochanie?",
    "Podetrzyj mi dupe",
    "Podetrzyj mi nos",
    "Tylko mirko",
    "Jeseem filozofem",
    "Jestem studentem prawa",
    "Wiesz, że jestem studentem prawa?",
    "Jesteś żydem",
    "Zjedź kurczaka i tyle chińczyku murzyński",
]
for i in range(10):
    clever =Existor("evie")
    clever2 = Existor("boi")

    con = Conversation(clever,clever2)
    con.start(lenght=15, start=choice(randy))
    con.save_history_to_file("hist3_"+str(i)+".txt")
    con.end()
"""
