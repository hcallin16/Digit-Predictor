# Digit Prediction Project
# Henry Callin
# 5/2/2022

# Imports
import os
import sys
import tkinter as tk    # Used for GUI
import numpy as np   # Used for arrays
from sklearn.svm import SVC   # Used for the SVM model
import pandas as pd   # Used to read .csv files
import win32gui   # Used to grab drawn image
import PIL   # Pillow used for image processing
import PIL.ImageOps
from PIL import ImageGrab   # Used to grab drawn image

# Import dataset
#os.chdir(sys._MEIPASS)  # Changes filepath for PyInstaller
data = np.array(pd.read_csv('train.csv'))   # Import train dataset
testdata = np.array(pd.read_csv('test.csv'))    # Import test dataset

# Split train/test sets
trainX = data[0:200, 1:]
trainY = data[0:200, 0]
testX = testdata[0:200, 1:]
testY = data[0:200, 0]

# Create and train the model
model = SVC(kernel='linear')    # Creates linear SVM model
model.fit(trainX, trainY)   # Fit the model


# Create GUI
class GUI(tk.Tk):

    # Initializing GUI elements
    def __init__(self):

        tk.Tk.__init__(self)
        self.x = self.y = 0

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")    # Creates canvas and cursor
        self.label = tk.Label(self, text="Prediction: ", font=("Helvetica", 48))    # Creates 'prediction: ' text
        self.predict_button = tk.Button(self, text="Predict", command=self.predict_digit)  # Creates predict button
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_canvas)   # Creates clear button

        # Grid structure
        self.canvas.grid(row=3, column=0, pady=2)   # Grid location for canvas
        self.label.grid(row=0, column=0, pady=2, padx=90)   # Grid for label
        self.predict_button.grid(row=1, column=0, pady=2, padx=4)   # Grid location for predict button
        self.clear_button.grid(row=2, column=0, pady=2)   # Grid location for clear buttom

        self.canvas.bind("<B1-Motion>", self.draw_lines)

    # Clear canvas
    def clear_canvas(self):
        self.canvas.delete("all")   # Clears anything drawn on the canvas

    # Get and process drawn image
    def predict_digit(self):

        # Get the drawn image
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)   # Locates the drawn image area
        img = ImageGrab.grab(rect)   # Grabs the image itself

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
        r = 8   # Radius of drawn lines
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')   # Creates ovals where
        # user draws


# Calls the GUI
app = GUI()
tk.mainloop()
