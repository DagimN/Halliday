from tkinter import *
from PIL import ImageTk, Image
import cv2
import math
import keyboard
import os
import csv

window = Tk()
window.title("Classifier for Halliday")
window.configure(width=400, height=300)
window.configure(bg='lightgray')

tilesDirectory = "C:\\Users\\dagmn\\Pictures\\3D Map Dataset\\generated tiles (150)"
classDirectory = "C:\\Users\\dagmn\\Documents\\Projects\\Python train\\dataset\\collection\\"
tiles = os.listdir(tilesDirectory)
tileIndex = 0

options = os.listdir(classDirectory)
objectClass = StringVar()
objectClass.set( options[0] )
objectClassName = StringVar()
classDropDown = OptionMenu( window, objectClass, *options )
classImages = []

objectCoordinates = []
image = cv2.imread(tilesDirectory + '\\' + tiles[tileIndex])
objectImage = Image.new('RGB', (image.shape[0], image.shape[1]), color=(255, 255, 255))
test = ImageTk.PhotoImage(objectImage)
label1 = Label(image=test)

def mouse_callback(event, x, y, flags, params):
    copyPressed = True if keyboard.is_pressed('x') else False
    erasePressed = True if keyboard.is_pressed('e') else False

    if event == cv2.EVENT_MOUSEMOVE and copyPressed:
        getPixelsFromBrush(x, y, 10, erase=False)
    if event == cv2.EVENT_MOUSEMOVE and erasePressed:
        getPixelsFromBrush(x, y, 10, erase=True)

def getPixelsFromBrush(x, y, radius, erase):
    global objectCoordinates, image, objectImage, label1
    label1.destroy()

    for i in range(0,radius):
        for j in range(0,radius):
            if(checkIfInsideBrush(x + i, y + j)):
                color = [255, 255, 255] if erase else image[y+j,x+i]
                objectCoordinates.append((x + i, y + j, color))
                objectImage.putpixel( (x + i,y + j), (color[2], color[0], color[1]))

    test = ImageTk.PhotoImage(objectImage)
    label1 = Label(image=test)
    label1.image = test
    label1.place(x=0, y=0)

def checkIfInsideBrush(x, y):
    global image
    
    if(x < image.shape[0] and y < image.shape[1]):
        return True
    
    return False

def submitClass():
    global options, classDropDown, classImages, objectImage, classLabel
    className = objectClassName.get()

    if not (className == ''):
        if not(options.__contains__(className)):
            options.append(className)
            classDropDown.destroy()
            classDropDown = OptionMenu( window, objectClass, *options )
            classDropDown.pack()
            classDropDown.place(x=200, y=40) 

            os.mkdir(path="C:\\Users\\dagmn\\Documents\\Projects\\Python train\\dataset\\collection\\" + className)
    else:
        className = objectClass.get()
    
    classImages.append((className,objectImage))

    classLabel = Label(window, text=str(len(classImages)))
    classLabel.place(x=320, y=80)

def addClass():
    global image, objectImage, classImages, label1
    objectImage = Image.new('RGB', (image.shape[0], image.shape[1]), color=(255, 255, 255))
    test = ImageTk.PhotoImage(objectImage)
    label1.destroy()
    label1 = Label(image=test)
    label1.place(x=0, y=0)

def finish():
    global image, tiles, tileIndex, classImages
    
    writeToDataset()
    classImages.clear()
    
    tileIndex = tileIndex + 1
    image = cv2.imread(tilesDirectory + '\\' + tiles[tileIndex])
    cv2.imshow("What objects are there?", image)

def writeToDataset():
    global classImages
    csvHeader = ['filename', 'classname', 'destination', 'objectdata']

    for image in classImages:
        className, objectImage = image
        directory = classDirectory + className + '\\'

        if(os.path.exists(directory + 'dataset.csv')):
            inputFile = open(directory + 'dataset.csv', 'r')
            csvFile = csv.reader(inputFile)
            index = len(list(csvFile)) - 1
            inputFile.close()
        else:
            inputFile = open(directory + 'dataset.csv', 'w', newline='')
            writer = csv.writer(inputFile)
            index = 1
            
            writer.writerow(csvHeader)
            inputFile.close()

        outputFile = open(directory + 'dataset.csv', 'a', newline='')
        fileName = className.lower() + str(index) + '.png'
        writer = csv.writer(outputFile)

        writer.writerow([fileName, className, directory, objectImage])
        cv2.imwrite(directory + fileName, objectImage)
        outputFile.close()

def selectAll():
    global image, objectImage
    objectImage = image
    submitClass()
    finish()
    
classDropDown.pack()
classDropDown.place(x=200, y=40)

submitButton = Button(window, text='Submit', command=submitClass)
submitButton.place(x=200, y=80)

addButton = Button(window, text='Add', command=addClass)
addButton.place(x=270, y=80)

finishButton = Button(window, text='Finish', command=finish)
finishButton.place(x=340, y=80)

allButton = Button(window, text='All', command=selectAll)
allButton.place(x=200, y=120)

classTextField = Entry(window, textvariable=objectClassName)
classTextField.place(x=200, y=10)

classLabel = Label(window, text=str(len(classImages)))
classLabel.place(x=320, y=80)

cv2.namedWindow('What objects are there?', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('What objects are there?', mouse_callback)
cv2.imshow("What objects are there?", image)

window.mainloop()