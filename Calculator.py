import tkinter as tk
import tkinter.ttk as ttk

FG = "black"
BG = "white"
FONT = "Consolas"
BTN_STYLE = {"bg":BG, "fg":FG, "font":(FONT, 30)}
ROWS = 4
COLUMNS = 6
BTN_SIZE = 100

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.answer = tk.Entry(fg=FG,bg=BG)
        
        self.nums_frame = tk.Frame(self)
##        self.nums_frame.grid_propagate(False)
##        for row in range(4):
##            self.nums_frame.grid_rowconfigure(row, weight=1)
##        for column in range(5):
##            self.nums_frame.grid_columnconfigure(column, weight=1)
        
        for n in range(1, 10):
            row = 3-((n-1)//3)
            column = (n-1)%3
            print(row, column)
            self.add_btn(n, row, column)
        self.add_btn()

        self.nums_frame.grid(row=1, column=0, sticky="NESW")

    def add_btn(self, text, row, column, function=lambda *args: None, frame=self.nums_frame):
        frame = tk.Frame(master=self.nums_frame, width=BTN_SIZE, height=BTN_SIZE)
        frame.grid_propagate(False)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=row, column=column)
        tk.Button(frame, text=text, **BTN_STYLE).grid(row=0, column=0, sticky="NESW")
    
if __name__ == "__main__":
    app = App()
