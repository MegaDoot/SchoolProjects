import tkinter as tk
import tkinter.ttk as ttk
import math
#√

FG = "black"
BG = "white"
FONT = "Calibri"
BTN_STYLE = {"bg":BG, "fg":FG, "font":(FONT, 30)}
ROWS = 4
COLUMNS = 6
BTN_HEIGHT = 60
BTN_WIDTH = 100
PADX = 3
PADY = 5

#For use in calculator
class Functions:
    sqrt = math.sqrt
    tan = math.tan

    @staticmethod
    def sin(x):
        return math.sin(math.radians(x))

    @staticmethod
    def cos(x):
        return math.cos(math.radians(x)) 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.answer = tk.Entry(fg=FG,bg=BG)
        self.scale=1
        
        self.nums_frame = tk.Frame(self)
        self.input_val = tk.StringVar(self, value = "")
        self.input = tk.Entry(self, state="normal", fg=FG, bg=BG, font=(FONT, 30), width=0, textvariable=self.input_val, bd=0, highlightthickness=0)
        self.input.bind("<Key>", lambda event: "break")
        self.input.focus_set()
        
        self.output = tk.Entry(self, state="disabled", disabledforeground=FG, disabledbackground=BG, font=(FONT, 40), width=0, bd=0, justify = "left")
        #width=0: width is governed by 'sticky' parameter in grid
        

        f = self.add_btn

        f("√", 0, 0, op=True)
        f("**", 0, 1, op=True)
        f("%", 0, 2, op=True)
        f("//", 0, 3, op=True)
        f("CLR", 0, 4, command=lambda: self.input_val.set(""))

        f("*", 1, 3, op=True)
        f("+", 2, 3, op=True)
        f("(", 3, 3)

        f("/", 1, 4)
        f("-", 2, 4)
        f(")", 3, 4)
        

        for n in range(1, 10):
            row = 3-((n-1)//3)
            column = (n-1)%3
            print(row, column)
            f(str(n), row, column)

        f("0", 4, 0)
        f(".", 4, 1)
        f("sin", 4, 2)
        f("cos", 4, 3)
        f("tan", 4, 4)

        f("DEL", 5, 2, command=self.delete_char)
        f("Ans", 5, 3)
        f("=", 5, 4, command=self.evaluate)
        #Place down everything
        
        self.input.grid(row=1, column=0, sticky="NESW")
        self.output.grid(row=2, column=0, sticky="NESW")
        self.nums_frame.grid(row=3, column=0, sticky="NESW")
        self.mainloop()

    def get_curs(self): #Entry cursor position
        return self.input.index(tk.INSERT)

    def delete_char(self):
        cursor_pos = self.get_curs()
        if cursor_pos != 0:
            current = list(self.input_val.get())
            del current[cursor_pos - 1]
            self.input.icursor(cursor_pos - 1)
            self.input_val.set("".join(current))

    def add_text(self, text):
        func = False
        if text == "√":
            text = "√()"
            func = True
        cursor_pos = self.get_curs()
        print(cursor_pos)
        current = self.input_val.get()
        current = list(current)
        current.insert(cursor_pos, text)
        current = "".join(current)
        self.input_val.set(current)
        offset = len(text)
        if func:
            offset -= 1
        self.input.icursor(cursor_pos + offset)
        print(current)

    def evaluate(self):
        text = self.input_val.get()
        text = text.replace("√", "sqrt")
        print("text:", text)
        try:
            result = eval(text)
            self.set_result(result, FG)
        except Exception as error:
            self.set_result(type(error).__name__, "red")
    
    def set_result(self, text, colour):
        self.output.config(state="normal")
        self.output.config(fg=colour)
        self.output.delete(0, "end")
        self.output.insert(0, text)
        self.output.config(state="disabled")

    def add_btn(self, text, row, column, command=None, frame=None, rowspan=1, columnspan=1, op=False):
        if frame is None:
            frame = self.nums_frame
        print(text, command)
        if command is None:
            #print("command for '{}' is None".format(text))
            command = lambda: self.add_text(text)
        frame = tk.Frame(master=self.nums_frame, height=BTN_HEIGHT * rowspan, width=BTN_WIDTH * columnspan)
        frame.grid_propagate(False)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, pady = PADY, padx = PADX)
        tk.Button(frame, text=text, command=command, **BTN_STYLE).grid(row=0, column=0, sticky="NESW")
    
if __name__ == "__main__":
    app = App()
