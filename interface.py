# Codes for ui
import json
from tkinter import *

from annotation import parse_node


class interface:
    def __init__(self, conn):
        self.window = Tk()
        self.window.geometry("1030x750")
        self.window.title("cz4031 Project 2")
        self.db_cursor = conn.cursor()
        self.totalSteps = 0

    def submit(self):
        # save input
        text = self.panel_1_textarea.get("1.0", "end-1c")
        if not text.lower().startswith("explain"):
            text = f"explain analyze {text}"
        with open('test.txt', 'w') as file_object:
            file_object.write(text)

        # save qep
        self.db_cursor.execute(text)
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
