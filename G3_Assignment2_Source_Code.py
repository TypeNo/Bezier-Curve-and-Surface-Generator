import tkinter as tk

def de_casteljau(control_points, t):
    if len(control_points) == 1:
        return control_points[0]
    else:
        new_points = []
        for i in range(len(control_points) - 1):
            x = (1 - t) * control_points[i][0] + t * control_points[i + 1][0]
            y = (1 - t) * control_points[i][1] + t * control_points[i + 1][1]
            new_points.append((x, y))
        return de_casteljau(new_points, t)

control_points = []

def on_canvas_motion(event):
    x, y = event.x, event.y
    
    coordinate_label.config(text=f"Mouse Position: ({x - 300}, {300 - y})")

def on_canvas_click(event):
    x, y = event.x, event.y
    control_points.append((x, y))
    
    coordinate_label.config(text=f"Mouse Click: ({x - 300}, {300 - y})")
    
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="red")
    
    label_text = f"({x - 300}, {300 - y})"
    canvas.create_text(x + 20, y - 20, text=label_text, fill="blue", font=("Helvetica", 10))

    if len(control_points) >= 2:
        canvas.create_line(control_points[-2], control_points[-1], fill="blue")

    if len(control_points) >= 3:
        redraw_bezier_curve()

def reset_control_points():
    global control_points
    control_points = []
    canvas.delete("all")
    draw_coordinate_grid()

def draw_coordinate_grid():
    canvas.create_line(0, canvas_height // 2, canvas_width, canvas_height // 2, fill="black")  
    canvas.create_line(canvas_width // 2, 0, canvas_width // 2, canvas_height, fill="black")  

    for x in range(canvas_width // 6, canvas_width, canvas_width // 6):
        canvas.create_line(x, (canvas_height // 2) - 5, x, (canvas_height // 2) + 5, fill="black")
        label_text = str(x - (canvas_width // 2))
        canvas.create_text(x, (canvas_height // 2) + 20, text=label_text, font=("Helvetica", 10))

    for y in range(canvas_height // 6, canvas_height, canvas_height // 6):
        canvas.create_line((canvas_width // 2) - 5, y, (canvas_width // 2) + 5, y, fill="black")
        label_text = str((canvas_height // 2) - y)
        canvas.create_text((canvas_width // 2) + 20, y, text=label_text, font=("Helvetica", 10))

def redraw_bezier_curve():
    canvas.delete("curve")
    t_values = [i / 100 for i in range(101)]
    curve_points = [de_casteljau(control_points, t) for t in t_values]
    for i in range(100):
        x1, y1 = curve_points[i]
        x2, y2 = curve_points[i + 1]
        canvas.create_line(x1, y1, x2, y2, fill="green", tags="curve")

def on_mousewheel(event):
    scale_factor = 1.1
    if event.delta > 0:
        canvas.scale("all", event.x, event.y, scale_factor, scale_factor)
    else:
        canvas.scale("all", event.x, event.y, 1/scale_factor, 1/scale_factor)

root = tk.Tk()
root.title("Bezier Curve with Mouse Input")

canvas_width = 600
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
canvas.bind("<Motion>", on_canvas_motion)
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<MouseWheel>", on_mousewheel)

coordinate_label = tk.Label(root, text="Mouse Position: (0, 0)")
coordinate_label.pack()

reset_button = tk.Button(root, text="Reset Control Points", command=reset_control_points)
reset_button.pack()

draw_coordinate_grid() 

root.mainloop()
