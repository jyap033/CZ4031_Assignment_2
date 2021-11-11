
from tkinter import *
from tkinter import ttk
from utils import QepParser
from annotation import GraphGenerator


class interface:
    def __init__(self, conn, table_info):
        self.window = Tk()
        self.window.geometry("1030x750")
        self.window.title("cz4031 Project 2")
        self.generator = GraphGenerator()
        self.parser = QepParser()

        self.panel_1 = PanedWindow(bd=2, relief=RIDGE, height=350, width=500)
        self.panel_1_label = Label(self.panel_1, text="User input")
        self.panel_1_textarea = Text(self.panel_1, height=20, width=62)

        self.panel_2 = PanedWindow(bd=2, relief=RIDGE, height=350, width=1010)
        self.panel_2_textarea = Text(self.panel_2, height=20, width=125)
        self.panel_2_label = Label(self.panel_2, text="Annotated Result")

        self.panel_3 = PanedWindow(bd=2, relief=RIDGE, height=350, width=500)
        self.panel_3_label = Label(self.panel_3, text="Schema")

        self.visualise_button = Button(self.window, text="Visualise", relief=RIDGE, font=("arial", 12, "bold"),
                                       width=20,
                                       command=self.generator.generate, state='disable')
        self.submit_button = Button(self.window, text="Submit", relief=RIDGE, font=("arial", 12, "bold"), width=20,
                                    command=self.submit)

        self.db_conn = conn
        self.db_cursor = self.db_conn.cursor()
        self.totalSteps = 0
        self.table_info = table_info

    def submit(self):

        text = self.panel_1_textarea.get("1.0", "end-1c")
        if not text.lower().startswith("explain"):
            text = f"explain analyze {text}"
        # execute query
        try:
            self.db_cursor.execute(text)
            self.visualise_button.configure(state='active')

        except Exception as err:
            self.db_conn.rollback()
            self.panel_2_textarea.configure(state='normal')
            self.panel_2_textarea.delete('1.0', END)
            self.panel_2_textarea.insert(END, err)
            self.panel_2_textarea.configure(state='disabled')
            self.visualise_button.configure(state='disabled')

            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            return

        # save original qep (qep.txt)
        qep_lines = []
        for (qep_line,) in self.db_cursor.fetchall():
            qep_lines.append(qep_line)
        with open('qep.txt', 'w') as file_object:
            for line in qep_lines:
                file_object.write(line + "\n")

        # do parsing
        qep_json = ""
        try:
            node = self.parser.parse(qep_lines)
            qep_json = node.to_json_pretty()
        except ValueError as err:
            self.panel_2_textarea.configure(state='normal')
            self.panel_2_textarea.delete('1.0', END)
            self.panel_2_textarea.insert(END, err)
            self.panel_2_textarea.configure(state='disabled')
            self.visualise_button.configure(state='disabled')
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            return

        # save parsed qep (qep.json)
        with open('qep.json', 'w') as file_object:
            file_object.write(qep_json)

        # display
        self.panel_2_textarea.configure(state='normal')
        self.panel_2_textarea.delete('1.0', END)
        self.panel_2_textarea.insert(END, qep_json)
        self.panel_2_textarea.configure(state='disabled')


    def initialise(self):
        # panel1(Userinput)
        self.panel_1.place(x=10, y=20)
        self.panel_1_label.config(font=("Courier", 14))
        self.panel_1_label.pack()
        self.panel_1_textarea.pack()

        # panel2(annotated input)
        self.panel_2.place(x=10, y=380)
        self.panel_2_textarea.configure(state='disabled')
        self.panel_2_label.config(font=("Courier", 14))
        self.panel_2_label.pack()
        self.panel_2_textarea.pack()

        # panel3(Schema)
        self.panel_3.place(x=520, y=20)
        self.panel_3_label.config(font=("Courier", 14))
        self.panel_3_label.place(relx=0.0, rely=0.0)

        self.visualise_button.place(x=808, y=700)
        self.submit_button.place(x=304, y=340)

        # configure the grid layout
        self.panel_3.rowconfigure(0, weight=1)
        self.panel_3.columnconfigure(0, weight=1)

        # create a treeview
        tree = ttk.Treeview(self.panel_3)

        tree.heading("#0", text='Schema', anchor='w')

        # adding data
        i = 0
        for (k, v) in (self.table_info.items()):
            tree.insert('', END, text=k, iid=i, open=False)
            parent = i
            internal_i = 0
            for j in v:
                i += 1
                tree.insert('', END, text=j, iid=i, open=False)

                tree.move(i, parent, internal_i)
                internal_i += 1
            i += 1
        tree.pack()
        self.panel_3.add(tree)
        self.window.mainloop()
