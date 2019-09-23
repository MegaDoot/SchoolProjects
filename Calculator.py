import tkinter as tk
import tkinter.ttk as ttk
#√

FG = "black"
BG = "white"
FONT = "Calibri"
BTN_STYLE = {"bg":BG, "fg":FG, "font":(FONT, 30)}
ROWS = 4
COLUMNS = 6
BTN_SIZE = 100

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.answer = tk.Entry(fg=FG,bg=BG)
        self.scale=1
        
        self.nums_frame = tk.Frame(self)
        
##        self.nums_frame.grid_propagate(False)
##        for row in range(4):
##            self.nums_frame.grid_rowconfigure(row, weight=1)
##        for column in range(5):
##            self.nums_frame.grid_columnconfigure(column, weight=1)
        self.screen_val = tk.StringVar(self, value = "")
        self.screen = tk.Entry(self, state="normal", fg=FG, bg=BG, font=(FONT, 50), width = 0, textvariable=self.screen_val)
        self.screen.bind("<Key>", lambda event: "break")
        self.screen.focus_set()
        #width=0: width is governed by 'sticky' parameter in grid
        

        f = self.add_btn

        f("√", 0, 0, op=True)
        f("**", 0, 1, op=True)
        f("%", 0, 2, op=True)
        f("//", 0, 3, op=True)
        f("CLR", 0, 4, command=lambda: self.screen_val.set(""))

        f("*", 1, 3, op=True)
        f("+", 2, 3, op=True)
        f("(", 3, 3)
        f("Ans", 4, 3)

        f("/", 1, 4)
        f("-", 2, 4)
        f(")", 3, 4)
        f("=", 4, 4)

        for n in range(1, 10):
            row = 3-((n-1)//3)
            column = (n-1)%3
            print(row, column)
            f(str(n), row, column)

        f(0, 4, 0)
        f(".", 4, 1)
        f("DEL", 4, 2)
        
        #Place down everything
        
        self.screen.grid(row=1, column=0, sticky="NESW", pady=10)
        self.nums_frame.grid(row=2, column=0, sticky="NESW")
        self.mainloop()

    def get_curs(self): #Entry cursor position
        return self.screen.index(tk.INSERT)
    
    def add_text(self, text):
        func = False
        if text == "√":
            text = "√()"
            func = True
        cursor_pos = self.get_curs()
        print(cursor_pos)
        current = self.screen_val.get()
        current = list(current)
        current.insert(cursor_pos, text)
        current = "".join(current)
        self.screen_val.set(current)
        offset = len(text)
        if func:
            offset -= 1
        self.screen.icursor(cursor_pos + offset)
        print(current)

    def evaluate(self):
        text = self.screen_val.get()
        self.text.replace("√", "sqrt")

    def error(self):
        pass

    def add_btn(self, text, row, column, command=None, frame=None, rowspan=1, columnspan=1, op=False):
        if frame is None:
            frame = self.nums_frame
        print(text, command)
        if command is None:
            #print("command for '{}' is None".format(text))
            command = lambda: self.add_text(text)
        frame = tk.Frame(master=self.nums_frame, height=BTN_SIZE * rowspan, width=BTN_SIZE * columnspan)
        frame.grid_propagate(False)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan)
        tk.Button(frame, text=text, command=command, **BTN_STYLE).grid(row=0, column=0, sticky="NESW")
    
if __name__ == "__main__":
    app = App()
