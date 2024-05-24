import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Initial values for global variables
testGridsize = 8
testCliplimit = 4
count1 = 180
count2 = 80

def update_values(*args):
    global testGridsize, testCliplimit, count1, count2
    testGridsize = gridsize_scale.get()
    testCliplimit = cliplimit_scale.get()
    count1 = count1_scale.get()
    count2 = count2_scale.get()
    if testGridsize < 1:
        testGridsize = 1
    if testCliplimit < 1:
        testCliplimit = 1

def update_frame():
    global testGridsize, testCliplimit, count1, count2
    ret, frame = cam.read()
    if ret:
        # Get the original dimensions of the frame
        height, width = frame.shape[:2]
        # Define the max dimensions you want (e.g., max width of 640 and max height of 480)
        max_width = 640
        max_height = 480

        # Calculate the ratio to maintain aspect ratio
        video_ratio = width / height
        if width > height:  # Widescreen
            new_width = min(max_width, width)
            new_height = int(new_width / video_ratio)
        else:  # Portrait or square
            new_height = min(max_height, height)
            new_width = int(new_height * video_ratio)
        
        # Resize the frame while maintaining aspect ratio
        frame_resized = cv2.resize(frame, (new_width, new_height))

        gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        floatClip = testCliplimit * 0.5
        clahe = cv2.createCLAHE(clipLimit=floatClip, tileGridSize=(testGridsize, testGridsize))
        cl1 = clahe.apply(gray_frame)
        clamp = np.uint8(np.interp(cl1, [count2, count1], [0, 255]))
        equ = clahe.apply(clamp)

        img = Image.fromarray(equ)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    lmain.after(10, update_frame)


# Initialize main window
root = Tk()
root.title("Video CLAHE Filter by Faisal Jafar")

# Create scales for trackbar equivalents
gridsize_scale = Scale(root, from_=1, to=24, orient=HORIZONTAL, label="Grid Size")
gridsize_scale.set(testGridsize)
gridsize_scale.pack()

cliplimit_scale = Scale(root, from_=1, to=40, orient=HORIZONTAL, label="Clip Limit")
cliplimit_scale.set(testCliplimit)
cliplimit_scale.pack()

count1_scale = Scale(root, from_=180, to=500, orient=HORIZONTAL, label="Count1")
count1_scale.set(count1)
count1_scale.pack()

count2_scale = Scale(root, from_=80, to=500, orient=HORIZONTAL, label="Count2")
count2_scale.set(count2)
count2_scale.pack()

# Setup a label for displaying the video
lmain = Label(root)
lmain.pack()

# Bind update of values to the scales
gridsize_scale.bind("<Motion>", update_values)
cliplimit_scale.bind("<Motion>", update_values)
count1_scale.bind("<Motion>", update_values)
count2_scale.bind("<Motion>", update_values)

# Start video capture
cam = cv2.VideoCapture(0)

# Function to be called repeatedly for video updates
update_frame()

# Start the GUI
root.mainloop()

# Release resources
cam.release()
cv2.destroyAllWindows()

