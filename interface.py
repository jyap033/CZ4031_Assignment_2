# Codes for ui
import json
from tkinter import *
from tkinter import ttk
from annotation import parse_node
from graph_generator import GraphGenerator


class interface:
    def __init__(self, conn, table_info):
        self.window = Tk()
        self.window.geometry("1030x750")
        self.window.title("cz4031 Project 2")
        self.generator = GraphGenerator()


        self.panel_1 = PanedWindow(bd=2, relief=RIDGE, height=350, width=500)
        self.panel_1_label = Label(self.panel_1, text="User input")
        self.panel_1_textarea = Text(self.panel_1, height=20, width=62)

        self.panel_2 = PanedWindow(bd=3, relief=RIDGE, height=350, width=1000)
        self.panel_2_textarea = Text(self.panel_2, height=20, width=125)
        self.panel_2_label = Label(self.panel_2, text="Annotated Result")

        self.panel_3 = PanedWindow(bd=1, relief=RIDGE, height=355, width=500)
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
        # save input
        text = self.panel_1_textarea.get("1.0", "end-1c")
        if not text.lower().startswith("explain"):
            text = f"explain analyze {text}"
        with open('test.txt', 'w') as file_object:
            file_object.write(text)

        # save qep
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

        qep_lines = []
        for (qep_line,) in self.db_cursor.fetchall():
            qep_lines.append(qep_line)
        with open('qep.txt', 'w') as file_object:
            for line in qep_lines:
                print(line)
                file_object.write(line + "\n")

        # save parsed qep
        qep_json = ""
        try:
            node, _ = parse_node(qep_lines)
            qep_json = node.to_json_pretty()
            ''' Iterate thru json and add steps '''
            nodeDict = json.loads(qep_json)
            self.totalSteps = 0
            self.traverseCountStep(nodeDict)
            self.traverseAddStep(nodeDict)
            qep_json = json.dumps(nodeDict, indent=4)
            # print(f"qep_json: {node.to_json()}")
        except ValueError as e:
            print(f"got Exception: {e}")

        with open('qep.json', 'w') as file_object:
            file_object.write(qep_json)

        # display
        self.panel_2_textarea.configure(state='normal')
        self.panel_2_textarea.delete('1.0', END)
        self.panel_2_textarea.insert(END, qep_json)
        self.panel_2_textarea.configure(state='disabled')

    ''' Traverse through parsed qep to count steps'''

    def traverseCountStep(self, nodeDict):
        self.totalSteps += 1
        if not "children" in nodeDict:
            return
        else:
            for i in range(len(nodeDict['children'])):
                self.traverseCountStep(nodeDict['children'][i])

    ''' Traverse through parsed qep to add the step '''

    def traverseAddStep(self, nodeDict):
        nodeDict['step'] = self.totalSteps
        self.totalSteps -= 1
        if not "children" in nodeDict:
            return
        else:
            for i in range(len(nodeDict['children']) - 1, -1, -1):
                self.traverseAddStep(nodeDict['children'][i])

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

        self.visualise_button.place(x=810, y=700)
        self.submit_button.place(x=300, y=340)


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
