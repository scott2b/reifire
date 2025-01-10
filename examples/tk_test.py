"""Simplest possible canvas test."""

import tkinter as tk

# Create the main window
root = tk.Tk()
root.geometry('300x200')  # Force window size

# Create a canvas that fills the window
canvas = tk.Canvas(root, bg='white')
canvas.pack(expand=True, fill='both')

# Draw a red rectangle that fills most of the canvas
canvas.create_rectangle(10, 10, 290, 190, fill='red')

root.mainloop() 