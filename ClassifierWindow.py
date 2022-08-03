from tkinter import *
from PIL import ImageTk, Image
import cv2
import math

window = Tk()
window.title("Classifier for Halliday")
window.configure(width=600, height=300)
window.configure(bg='lightgray')

submitButton = Button(window, text='Submit')
submitButton.place(x=400, y=40)

addButton = Button(window, text='Add')
addButton.place(x=470, y=40)

classTextField = Entry(window)
classTextField.place(x=400, y=10)

# image1 = Image.open("dataset/training/building/building1.png")
# print(list(image1.getdata()))

canvas = Canvas(window, width=150, height=150)
canvas.place(x=200, y=0)

objectCoordinates = []
image = cv2.imread("dataset/training/building/building1.png")

# Circle Formula: (x - h)^2 + (y - k)^2 = r^2
def mouse_callback(event, x, y, flags, params):
    if event == 1:
        getPixelsFromBrush(x, y, 5)
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def getPixelsFromBrush(x, y, radius):
    global objectCoordinates, image, sample

    for i in range(0,radius):
            for j in range(0,radius):
                if(checkIfInsideBrush(x + i, y + j, x, y, radius)):
                    sample = Image.new('RGB', (150, 150))
                    test = ImageTk.PhotoImage(sample)
                    label1 = Label(image=test)
                    label1.image = test
                    label1.place(x=0, y=0)

                    color = image[x+i,y+j]
                    objectCoordinates.append((x + i, y + j, color))
                    print((color[0], color[1], color[2]))
                    sample.putpixel( (x + i,y + i), (color[0], color[1], color[2]))

def checkIfInsideBrush(x, y, centerx, centery, radius):
    global image
    
    if((math.pow((x - centerx), 2) + math.pow((y - centery), 2))  <= math.pow(radius, 2)):
        if(x < image.shape[0] and y < image.shape[1]):
            return True
    
    return False



cv2.namedWindow('Sample', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Sample', mouse_callback)

cv2.imshow("Sample", image)

window.mainloop()

