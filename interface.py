#Codes for ui
import json
from tkinter import *

class interface:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("1030x750")
        self.window.title("cz4031 Project 2")


    def submit(self):
        #save input
        text = self.panel_1_textarea.get("1.0", "end-1c")
        with open('test.txt', 'w') as file_object:
            file_object.write(text)

        #load input
        self.panel_2_textarea.configure(state='normal')
        self.panel_2_textarea.delete('1.0', END)
        #this suppose to be in json
        with open('test.txt', 'r') as file:
            output = file.read()
        self.panel_2_textarea.insert(END,output)
        self.panel_2_textarea.configure(state='disabled')

    def gui(self):
        # panel1(Userinput)
        self.panel_1 = PanedWindow(bd=2, relief=RIDGE, height=350, width=500)
        self.panel_1.place(x=10, y=20)
        self.panel_1_label = Label(self.panel_1, text="User input")
        self.panel_1_label.config(font=("Courier", 14))
        self.panel_1_textarea = Text(self.panel_1, height=20, width=62)
        self.panel_1_label.pack()
        self.panel_1_textarea.pack()

        # panel2(annotated input)
        self.panel_2 = PanedWindow(bd=2, relief=RIDGE, height=350, width=500)
        self.panel_2.place(x=10, y=380)
        self.panel_2_label = Label(self.panel_2, text="Annotated Result")
        self.panel_2_textarea = Text(self.panel_2, height=20, width=62)
        self.panel_2_textarea.configure(state='disabled')
        self.panel_2_label.config(font=("Courier", 14))
        self.panel_2_label.pack()
        self.panel_2_textarea.pack()

        # panel3(QEP input)
        self.panel_3 = PanedWindow(bd=2, relief=RIDGE, height=710, width=500)
        self.panel_3.place(x=520, y=20)
        self.panel_3_label = Label(self.panel_3, text="Visualize")
        self.panel_3_label.config(font=("Courier", 14))
        self.panel_3_label.place(relx=0.0, rely=0.0)

        # Submit button
        self.submitbtn = Button(self.window, text="Submit", relief=RIDGE, font=("arial", 12, "bold"), width=20,
                           command=self.submit)
        self.submitbtn.place(x=300, y=340)
        self.window.mainloop()


