import tkinter as tk


WIDTH = 150
HEIGHT = 200
class PolylineDrawer:
    def __init__(self, master):
        self.master = master
        self.master.title("Polyline Drawer")

        self.canvas = tk.Canvas(self.master, bg="white", width=WIDTH, height=HEIGHT)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.polylines = []
        self.current_line = None     # canvas object
        self.selected_point = None   # coded as : (i, polyline)
        self.selected_point_square = None
        self.correction_entry = tk.Entry(self.master)
        self.correction_entry.pack()

        draw_button = tk.Button(self.master, text="Draw Polyline", command=self.start_drawing)
        draw_button.pack()

        correction_button = tk.Button(self.master, text="Correct Points", command=self.correct_points)
        correction_button.pack()

        clear_button = tk.Button(self.master, text="Clear", command=self.clear)
        clear_button.pack()

        export_button = tk.Button(self.master, text="Export Data", command=self.export_data)
        export_button.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.master.bind("<Escape>", self.remove_last_point)
        self.start_drawing()

    def clear(self):
        self.canvas.delete('all')
        self.polylines = [[]]
        self.current_line = None     # canvas object
        self.selected_point = None   # coded as : (i, polyline)
        self.selected_point_square = None

    def start_drawing(self):
        self.polylines.append([])
        self.current_line = None

    def on_click(self, event):
        x, y = event.x, event.y

        for polyline in self.polylines:
            for i, (px, py) in enumerate(polyline):
                if x - 5 <= px <= x + 5 and y - 5 <= py <= y + 5:
                    self.selected_point = (i, polyline)
                    self.display_selected_point()
                    return

        current_polyline = self.polylines[-1]
        current_polyline.append((x, y))

        if len(current_polyline) > 1:
            self.draw_line(current_polyline)
        else:
            self.draw_point(x,y)

    def on_double_click(self, event):
        x, y = event.x, event.y

        for polyline in self.polylines:
            for i, (px, py) in enumerate(polyline):
                if x - 5 <= px <= x + 5 and y - 5 <= py <= y + 5:
                    if len(polyline) > 2:
                        polyline.append(polyline[0])  # Close the polyline
                        self.draw_line(polyline)
                    return

    def on_drag(self, event):
        if self.selected_point is not None:
            x, y = event.x, event.y
            i, polyline = self.selected_point
            polyline[i] = (x, y)
            self.draw_line(polyline)
            self.display_selected_point()

    def draw_point(self, x, y):
        if self.selected_point:
            i, polyline = self.selected_point
            print(f"détruire {i}, d{polyline}")
            self.canvas.delete(self.selected_point_square)

        self.selected_point_square = self.canvas.create_rectangle(x-2, y-2, x+2, y+2)

    def draw_line(self, polyline):
        if self.current_line:
            self.canvas.delete(self.current_line)
        self.current_line = self.canvas.create_line(polyline, fill="black")


    def display_selected_point(self):
        if self.selected_point is not None:
            i, polyline = self.selected_point
            x, y = polyline[i]
            self.draw_point(x, y)
            self.correction_entry.delete(0, tk.END)
            self.correction_entry.insert(0, f"{x},{y}")

    def correct_points(self):
        correction_text = self.correction_entry.get()
        try:
            corrections = [int(coord) for coord in correction_text.split(",")]
            if len(corrections) == 2 and self.selected_point is not None:
                i, polyline = self.selected_point
                polyline[i] = (corrections[0], corrections[1])
                self.draw_line(polyline)
            else:
                print("Invalid correction format. Please enter two integers separated by a comma.")
        except ValueError:
            print("Invalid correction format. Please enter integers separated by a comma.")

    def remove_last_point(self, event):
        if self.polylines:
            current_polyline = self.polylines[-1]
            if current_polyline:
                current_polyline.pop()
                if len(current_polyline) > 1:
                    self.draw_line(current_polyline)

    def export_data(self):
        print("Exporting data:")
        lst = []
        for i, polyline in enumerate(self.polylines):
            pl_str = ", ".join([str(point) for point in polyline])
            lst.append("[" + pl_str + "]")
        print("["+", ".join(lst)+"]")

if __name__ == "__main__":
    root = tk.Tk()
    app = PolylineDrawer(root)
    root.mainloop()
