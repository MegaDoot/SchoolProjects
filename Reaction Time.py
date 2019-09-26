import tkinter as tk
import turtle
import time
from random import randrange
import threading

FONT = "Consolas"
FG = "black"
BG = "white"
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 200
CANVAS_PADX = 10
CANVAS_PADY = 10


def get_time():
    return int(round(time.time() * 1000))


def add_suffix(num):
    num = str(num)
    append = {"1": "st", "2": "nd", "3": "rd"}.get(num[-1], "th")
    return num + append


def style(size):
    return {"fg": FG, "bg": BG, "font": (FONT, size)}

def flatten(array):
    answer = []
    for el in array:
        answer += el
    return answer

def mean(array):
    return sum(array) // len(array)

def get_scores():
    with open("times.txt", "r") as file:
##        return file.readlines()
        return [list(map(int, line.rstrip("\n").split(","))) for line in file.readlines()]

def add_scores(scores):
    current = get_scores()
    open("times.txt", "w").close()
    with open("times.txt", "a") as file:
        for i in range(len(scores)):
            current[i].append(scores[i])
        print(current)
        for row in range(len(current)):
            if current == [] and current[row] > 600: #Anomalous
                continue
            to_write = str(current[row])[1:-1].replace(" ", "")
            print("write:", to_write)
            file.write(to_write)
            file.write("\n")    
##        file.write(current)

class Graph(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.grid(row=0, column=0, sticky="NESW")
        self.t_screen = turtle.TurtleScreen(self.canvas)
        self.t_screen.delay(0)
        self.line_t = turtle.RawTurtle(self.t_screen)
        self.line_t.setpos(100, 100)
        self.scale_t = turtle.RawTurtle(self.t_screen)
##        self.scale_t.pu()
        self.draw_all()

    def draw_all(self):
        flattened = sorted(flatten(get_scores()))
        borders = (min(flattened), max(flattened))
        self.scale_t.setpos(CANVAS_PADX - (CANVAS_WIDTH / 2), CANVAS_PADY - (CANVAS_HEIGHT / 2))
        self.scale_t.write(str(borders[0]), align="center", font=(FONT, 20))

class FrameLbl(tk.Frame):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master=master)
        self.configure(width=width, height=height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_propagate(False)
        self.lbl = tk.Label(self, **kwargs)
        self.lbl.grid(sticky="NESW")


class Table(tk.Frame):
    def __init__(self, master, rows, columns):
        super().__init__(master=master)
        self.rows = rows
        self.columns = columns
        self.array = [
            [FrameLbl(
                self, 160, 30, text="", relief="solid",
                borderwidth=2, **style(15)) for _ in range(columns)
                ] for _ in range(rows)
                ]
        for row in range(rows):
            for column in range(columns):
                self.array[row][column].grid(row=row, column=column)

    def __setitem__(self, coords, value):
        self.array[coords[0]][coords[1]].lbl.config(text=value)

    def __getitem__(self, coords):
        return self.array[coords[0]][coords[1]]

    def highlight(self, row, column):
        for r in range(self.rows):
            for c in range(self.columns):
                self.array[r][c].lbl.config(bg=BG)
        self.array[row][column].lbl.config(bg="yellow")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg=BG)
        self.grid_columnconfigure(0, weight=1)
        self.title("Window")
        self.state("zoomed")
        self.user_count = 0
        self.game_frame = MainFrame(self, bg=BG)
        self.game_frame.grid(row=0, column=0)
        self.mainloop()


class MainFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.master = master
        
        tk.Label(self, text="Test your reaction times!", **style(40)).grid(
            row=0, column=0)
        tk.Message(self, text="""Press begin and press any key as soon as you
see the rectangle change colour. It will change randomly a total of 5 times
and only your scores will be recorded for others to compete against!""",
                   width=1500, justify="center", **style(15)).grid(
                       row=1, column=0)
        self.start_btn = tk.Button(self, text="Begin!", state="normal", command=self.start, **style(25))
        self.start_btn.grid(row=2, column=0, pady=10)
        self.colour = tk.Frame(self, bg="red", width=500, height=100)
        self.colour.grid(row=3, column=0, pady=10)
        self.info_lbl = tk.Label(self, text="", **style(20))
        self.info_lbl.grid(row=4, column=0)
        self.graph_btn = tk.Button(self, text="View Graph", command=self.to_graph, **style(20))
        self.graph_btn.grid(row=6, column=0)

        self.graph = Graph(self)
        
        self.table = Table(self, 3, 7)

        for col in range(1, 6):
            self.table[0, col] = col
        self.table[0, 6] = "Average"
        self.table[1, 0] = "Your time (ms)"
        self.table[2, 0] = "Average (ms)"
        self.reset_table_times()
        self.table.grid(row=7, column=0)
        
        self.has_pressed = tk.BooleanVar(self, value=False)
        self.master.bind("<Key>", lambda event : threading.Thread(target=self.key_pressed).start())


    def key_pressed(self):
        self.update_idletasks()
        print(self.colour.cget("bg"))
        if self.colour.cget("bg") == "green":
            self.has_pressed.set(True)
        else:
            print("penalty")
            self.additional_time += 0.5

    def to_graph(self):
        self.table.grid_remove()
        self.graph.grid(row=7, column=0)

    def one_loop(self, loop):
        print(self.additional_time)
        time.sleep(self.additional_time)
        self.additional_time = 0
        self.start_time = get_time()
        self.colour.config(bg="green")
        self.update()
        self.wait_variable(self.has_pressed)
        time_taken = get_time() - self.start_time
        self.table[1, loop + 1] = time_taken
        row_contents = self.table.array[1][1:loop + 2]
        self.row_values = tuple(int(frame_lbl.lbl.cget("text")) for frame_lbl in row_contents)
        print(self.row_values)
        self.best = min(self.row_values)
        self.table[1, 6] = mean(self.row_values)
        self.table.highlight(1, self.row_values.index(self.best) + 1)
        self.colour.config(bg="red")
        self.update_idletasks()

    def reset_table_times(self):
        scores = tuple(map(mean, get_scores()))
##        print(scores)
        for col in range(1, 6):
            self.table[1, col] = "-"
            self.table[2, col] = scores[col - 1]
        self.table[1, 6] = "-"
        self.average = mean(tuple(map(mean, get_scores())))
        self.table[2, 6] = self.average

    def start(self):
        self.info_lbl.config(text="Get ready, {} user this evening!".format(add_suffix(self.master.user_count + 1)))
        self.reset_table_times()
        self.start_btn.config(state="disabled")
        self.update_idletasks()
        
        time.sleep(2)
        self.additional_time = 0
        self.info_lbl.config(text="Press any key as soon as it turns green!")
        for n in range(4):
            self.master.after(randrange(2000, 4000), self.one_loop(n))
        self.one_loop(4)
        self.start_btn.config(state="normal")
        extra = "Good job!" if self.best < self.average else "Better luck next time!"
        self.info_lbl.config(text=f"Your best: {self.best}, average: {self.average}. " + extra)
        add_scores(self.row_values)
        self.master.user_count += 1

if __name__ == "__main__":
    app = App()
