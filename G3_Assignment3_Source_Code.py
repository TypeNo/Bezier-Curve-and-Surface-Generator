import tkinter as tk
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def de_casteljau(control_points, t):
    if len(control_points) == 1:
        return control_points[0]
    else:
        new_points = []
        for i in range(len(control_points) - 1):
            x = (1 - t) * control_points[i][0] + t * control_points[i + 1][0]
            y = (1 - t) * control_points[i][1] + t * control_points[i + 1][1]
            z = (1 - t) * control_points[i][2] + t * control_points[i + 1][2]
            new_points.append((x, y, z))
        return de_casteljau(new_points, t)

control_points = []

def on_canvas_motion(event):
    x, y = event.x, event.y
    coordinate_label.config(text=f"Mouse Position: ({x - 300}, {300 - y})")

def add_point_from_entries():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        control_points.append((x, y, z))

        canvas.create_oval(x + 300 - 4, 300 - y - 4, x + 300 + 4, 300 - y + 4, fill="red")

        label_text = f"({x}, {y}, {z})"
        canvas.create_text(x + 300 + 20, 300 - y - 20, text=label_text, fill="blue", font=("Helvetica", 10))

        if len(control_points) >= 3:
            redraw_bezier_curve()

    except ValueError:
        print("Invalid input. Please enter numeric values for x, y, and z.")

def reset_control_points():
    global control_points
    control_points = []
    canvas.delete("all")
    if hasattr(root, "canvas_agg"):
        root.canvas_agg.get_tk_widget().destroy()  # Destroy the 3D plot canvas if it exists
        delattr(root, "canvas_agg")

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
    if len(control_points) >= 3:
        canvas.delete("curve")
        t_values = np.linspace(0, 1, 100)
        curve_points = np.array([de_casteljau(control_points, t) for t in t_values])
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2], color="green", linewidth=0, alpha=0.5)

        # Plot control points on the 3D plot with labels
        control_points_array = np.array(control_points)
        ax.scatter(control_points_array[:, 0], control_points_array[:, 1], control_points_array[:, 2], color='red', marker='o', s=50)
        for i, (x, y, z) in enumerate(control_points):
            ax.text(x, y, z, f'({x}, {y}, {z})', fontsize=8)

        # Display the 3D plot in tkinter window
        draw_3d_plot_on_canvas(fig)

def draw_3d_plot_on_canvas(figure):
    root.canvas_agg = FigureCanvasTkAgg(figure, master=root)
    root.canvas_agg.draw()
    root.canvas_agg.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_mousewheel(event):
    scale_factor = 1.1
    if event.delta > 0:
        canvas.scale("all", event.x, event.y, scale_factor, scale_factor)
    else:
        canvas.scale("all", event.x, event.y, 1/scale_factor, 1/scale_factor)

root = tk.Tk()
root.title("Bezier Curve with Number Pad Input")

canvas_width = 600
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
canvas.bind("<Motion>", on_canvas_motion)
canvas.bind("<MouseWheel>", on_mousewheel)

entry_x = tk.Entry(root, width=10)
entry_y = tk.Entry(root, width=10)
entry_z = tk.Entry(root, width=10)

entry_x.pack(side=tk.LEFT)
entry_y.pack(side=tk.LEFT)
entry_z.pack(side=tk.LEFT)

button_add_point = tk.Button(root, text="Add Point", command=add_point_from_entries)
button_add_point.pack(side=tk.LEFT)

coordinate_label = tk.Label(root, text="Mouse Position: (0, 0)")
coordinate_label.pack()

reset_button = tk.Button(root, text="Reset Control Points", command=reset_control_points)
reset_button.pack()

draw_coordinate_grid() 

root.mainloop()
