import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funktion zum Erstellen des Würfels
def cube_definition():
    points = np.array([[-1, -1, -1],
                       [ 1, -1, -1],
                       [ 1,  1, -1],
                       [-1,  1, -1],
                       [-1, -1,  1],
                       [ 1, -1,  1],
                       [ 1,  1,  1],
                       [-1,  1,  1]])
    return points

# Funktion zum Erstellen der Kanten des Würfels
def get_cube_edges(points):
    edges = [
        [points[0], points[1]], [points[1], points[2]], [points[2], points[3]], [points[3], points[0]],  # Unterseite
        [points[4], points[5]], [points[5], points[6]], [points[6], points[7]], [points[7], points[4]],  # Oberseite
        [points[0], points[4]], [points[1], points[5]], [points[2], points[6]], [points[3], points[7]]   # Vertikalen
    ]
    return edges

# Funktion für die Animation
def update(frame, edges, ax):
    ax.cla()
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_facecolor('black')
    
    ax.set_axis_off()
    
    angle = np.radians(frame)
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                [np.sin(angle), np.cos(angle), 0],
                                [0, 0, 1]])
    
    tilted_points = np.dot(points, rotation_matrix)
    
    for edge in edges:
        edge_rot = np.dot(edge, rotation_matrix)
        ax.plot3D(*zip(*edge_rot), color="red", linewidth=2)

# Funktion für die Eingabe-Verarbeitung
def on_submit():
    input_text = input_field.get()
    text_field.config(state='normal')
    text_field.insert(tk.END, f"Eingegebener Text: {input_text}\n")
    text_field.config(state='disabled')
    input_field.delete(0, tk.END)

# Haupt-Programm
root = tk.Tk()
root.title("3D Cube Animation mit Eingabe")

# Erstelle das matplotlib-Figur-Objekt und die 3D-Achsen
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')

# Matplotlib-Canvas in das Tkinter-Fenster einbinden
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Definiere Würfel und Kanten
points = cube_definition()
edges = get_cube_edges(points)

# Animation
ani = FuncAnimation(fig, update, frames=range(0, 360, 2), fargs=(edges, ax), interval=50)

# Eingabefeld und Button
input_field = tk.Entry(root)
input_field.pack(side=tk.LEFT, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(side=tk.LEFT, padx=10, pady=10)

# Textfeld für Ausgaben
text_field = tk.Text(root, state='disabled', height=5, width=40)
text_field.pack(side=tk.BOTTOM, padx=10, pady=10)

# Startet die Tkinter Mainloop
root.mainloop()
