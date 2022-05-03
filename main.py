# Digit Prediction Project
# Henry Callin
# 5/2/2022

# Imports
import os
import sys
import tkinter as tk
import PIL.ImageOps
import numpy as np
from sklearn.svm import SVC
import pandas as pd
import win32gui
import PIL
from PIL import ImageGrab

# Import dataset
os.chdir(sys._MEIPASS)
data = np.array(pd.read_csv('train.csv'))

# Split train/test sets
trainX = data[0:900, 1:]
trainY = data[0:900, 0]
testX = data[200:1100, 1:]
testY = data[200:1100, 0]

# Create models and train them
Gamma = 0.001
C = 1
model = SVC(kernel='poly', C=C, gamma=Gamma)
model.fit(trainX, trainY)
predY = model.predict(testX)


# Create GUI
class App(tk.Tk):

    # Initializing GUI elements
    def __init__(self):

        tk.Tk.__init__(self)
        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Prediction: ", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Predict", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        # Grid structure
        self.canvas.grid(row=3, column=0, pady=2)
        self.label.grid(row=0, column=0, pady=2, padx=90)
        self.classify_btn.grid(row=1, column=0, pady=2, padx=4)
        self.button_clear.grid(row=2, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    # Clear canvas
    def clear_all(self):
        self.canvas.delete("all")

    # Get and process drawn image
    def classify_handwriting(self):

        # Get the drawn image
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        img = ImageGrab.grab(rect)

        # Image processing
        img = img.resize((28, 28))  # Resize image to 28x28
        img = img.convert('L')  # Convert to grayscale
        img = PIL.ImageOps.invert(img)  # Invert white and black to match model
        img = np.array(img)  # Convert image to an array
        img = img.reshape(1, 784)   # Reshape array to match model

        digit = model.predict(img)[0]   # Predict digit using model

        self.label.configure(text='Prediction: ' + str(digit))  # Display the digit predicted

    # Draw lines on canvas
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


# Calls the GUI
app = App()
tk.mainloop()
