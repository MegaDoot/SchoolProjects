"""
Add:
Constants & Variables
Assignment
Selection
Nested Selection
Iteration
Nested Loops *
Arithmetic Operators
Subroutines
Functions
Parameters+Arguments
Exception Handling
"""

import tkinter as tk
import tkinter.ttk as ttk
import math
import dryclass as dc
#√ Pol, Rec, Ln, e, pi

FG = "black"
BG = "white"
FONT = "Monospace"
BTN_STYLE = {"bg":BG, "fg":FG, "font":(FONT, 30)}
ROWS = 6
COLUMNS = 5
BTN_HEIGHT = 60
BTN_WIDTH = 100
PADX = 3
PADY = 5
FUNCS = {"sqrt":0, "sin":0, "cos":0, "tan":0, "abs":0, "log":1, "asin":0, "acos":0, "atan":0, "ln":0, "Pol":1, "Rec":1}
CONSTS = ("e", "π")
ROUND = lambda n: round(n, 7)
MOVEMENT_KEYS = ("Right", "Left", "Up", "Down", "Home", "End", "Next", "Prior")

sqrt = math.sqrt
log = math.log
π = math.pi
e = math.e

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

def asin(x):
    return math.degrees(math.asin(x))

def acos(x):
    return math.degrees(math.acos(x))

def atan(x):
    return math.degrees(math.atan(x))

def Pol(x, y):
    return NumPair(*(sqrt((x ** 2) + (y ** 2)), atan(y / x)), ("x", "y"))

def Rec(r, theta):
    return NumPair(*(r * cos(theta), r * sin(theta)), ("r", "θ"))

@dc.add_methods("__main__.NumPair: obj.pair[0]; int, float: obj", *dc.Opers.MATH)
class NumPair:
    def __init__(self, val_1, val_2, chars):
        self.pair = [val_1, val_2]
        self.chars = chars

    def __repr__(self):
        return str(f"{self.chars[0]}={self.pair[0]},{self.chars[1]}={self.pair[1]}")

    def __round__(self, places):
        return NumPair(*map(ROUND, self.pair), self.chars)

##test = NumPair(3, 4)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        for row in range(3):
            self.grid_rowconfigure(row, weight=1)
        self.title("Calculator")
        self.grid_columnconfigure(0, weight=1)
        self.answer = tk.Entry(fg=FG,bg=BG)
        self.scale = 1
        self.entry_frame = tk.Frame(self, height=90)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_propagate(False)
        self.nums_frame = tk.Frame(self)
        for column in range(COLUMNS):
            self.nums_frame.grid_columnconfigure(column, weight=1)
        for row in range(ROWS):
            self.nums_frame.grid_rowconfigure(row, weight=1)
        
        self.input_val = tk.StringVar(self, value = "")
        self.input = tk.Entry(self.entry_frame, state="normal", fg=FG, bg=BG, font=(FONT, 30), width=0, textvariable=self.input_val, bd=0, highlightthickness=0)
        self.input_val.trace("w", lambda *args: self.input.focus_set())
        self.input.focus_set()
        self.output = tk.Entry(self.entry_frame, state="normal", fg=FG, bg=BG, disabledforeground=FG, disabledbackground=BG, font=(FONT, 30), width=0, bd=0, justify = "right")
        #width=0: width is governed by 'sticky' parameter in grid
        for entry in (self.input, self.output):
            entry.bind("<Key>", self.entry_event)
        self.input.bind("<Button-1>", lambda *args: self.set_result("", FG))
        
        self.ans = 0

        f = self.add_btn

        f("√", 0, 0, operator=True)
        f("**", 0, 1, operator=True)
        f("%", 0, 2, operator=True)
        f("//", 0, 3, operator=True)
        f("CLR", 0, 4, command=self.clear_all)

        f("*", 1, 3, operator=True)
        f("+", 2, 3, operator=True)
        f("(", 3, 3)

        f("/", 1, 4, operator=True)
        f("-", 2, 4, operator=True)
        f(")", 3, 4)
        

        for n in range(1, 10):
            row = 3-((n-1)//3)
            column = (n-1)%3
            f(str(n), row, column)

        f("0", 4, 0)
        f(".", 4, 1)
        f("sin", 4, 2)
        f("cos", 4, 3)
        f("tan", 4, 4)

        f("ln", 5, 0)
        f("log", 5, 1)
        f("asin", 5, 2)
        f("acos", 5, 3)
        f("atan", 5, 4)

##        f("*10**", 6, 0, operator=True, write="E")
        f("abs", 6, 0)
        f("e", 6, 1, operator=True)
        f("π", 6, 2)
        f("Pol", 6, 3)
        f("Rec", 6, 4)
        
        f(",", 7, 0)
        f("↑", 7, 1, command=lambda: self.set_result("", FG))
        f("DEL", 7, 2, command=self.delete_char)
        f("Ans", 7, 3)
        f("=", 7, 4, command=self.evaluate)

        #Place down everything
        self.input.grid(row=1, column=0, sticky="NESW")
        self.output.grid(row=2, column=0, sticky="NESW")
        
        self.entry_frame.grid(row=0, column=0, sticky="NESW")
        self.nums_frame.grid(row=2, column=0, sticky="NESW")

        self.update_idletasks() # Updates winfo height and width
##        print(self.winfo_width(), self.winfo_height())
        self.minsize(self.winfo_width(), self.winfo_height())
        
        self.mainloop()

    def get_curs(self): #Entry cursor position
        return self.input.index(tk.INSERT)

    def entry_event(self, event):
        key = event.keysym
        print(key)
        if not key in MOVEMENT_KEYS:
            return "break"
        if key in ("Up", "Prior"):
            self.input.focus_set()
            return
        if key in ("Down", "Next"):
            self.output.focus_set()
##        print(event.__dict__)

    def clear_all(self):
        self.input_val.set("")
        self.set_result("", FG)

    def delete_char(self):
        self.input.focus_set()
        if self.output.get() != "":
            self.clear_all()
        cursor_pos = self.get_curs()
        if cursor_pos != 0:
            current = list(self.input_val.get())
            del current[cursor_pos - 1]
            self.input.icursor(cursor_pos - 1)
            self.input_val.set("".join(current))

    def add_text(self, text, operator=False):
##        try:
##            selection = self.input.selection_get()
##            print(*dir(self.input), sep = "\n")
##            print(selection)
##            print(self.input.ANCHOR)
##        except Exception as error:
##            print(error)
        if self.output.get() != "":
            self.set_result("", FG)
            if operator:
                self.input_val.set("Ans")
                self.input.icursor(3)
            else:
                self.input_val.set("")
        func = False
        if text in FUNCS.keys() or text == "√":
            if text == "√":
                commas = 0
            else:
                commas = FUNCS[text] #Number of parameters - 1 = numer of commas
            text += "(" + "," * commas + ")"
            func = True
        cursor_pos = self.get_curs()
        current = self.input_val.get()
        current = list(current)
        current.insert(cursor_pos, text)
        current = "".join(current)
        self.input_val.set(current)
        offset = len(text)
        if func:
            offset -= commas + 1
        self.input.icursor(cursor_pos + offset)

    def evaluate(self):
        text = self.input_val.get()
        text = text.replace("√", "sqrt")
##        text = text.replace("E", "*10**")
##        for func in FUNCS:
##            text = text.replace(func, "Functions." + func)
        text = text.replace("Ans", "(" + str(self.ans) + ")")
##        text = text.replace("e", "(e)")
        text = list(text)
        for x in range(len(text)):
            if text[x] == "e":
                if x < len(text) - 1:
                    if text[x + 1] != "c": #Not in 'Rec'
                        text[x] = "(e)"
                else:
                    text[x] = "(e)"
        text = "".join(text)
        print(f"text:'{text}'")
        try:
            result = eval(text)
##            print(f"result:'{result}'")
            result = ROUND(result)
            self.set_result(result, FG)
            self.ans = result
        except Exception as error:
            print(error)
            self.set_result(type(error).__name__, "red")
    
    def set_result(self, text, colour):
        if text == "":
            self.input.focus_set()
        else:
            self.output.focus_set()
##        self.output.config(state="normal")
        self.output.config(disabledforeground=colour)
        self.output.delete(0, "end")
        self.output.insert(0, text)
##        self.output.config(state="disabled")

    def add_btn(self, text, row, column, command=None, frame=None, rowspan=1, columnspan=1, operator=False, write=None):
        if write is None:
            write = text
        if frame is None:
            frame = self.nums_frame
        if command is None:
            #print("command for '{}' is None".format(text))
            def command():
                return self.add_text(write, operator)
        frame = tk.Frame(master=self.nums_frame, height=BTN_HEIGHT * rowspan, width=BTN_WIDTH * columnspan)
        frame.grid_propagate(False)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, pady = PADY, padx = PADX)
        tk.Button(frame, text=text, command=command, **BTN_STYLE).grid(row=0, column=0, sticky="NESW")
    
if __name__ == "__main__":
    app = App()
