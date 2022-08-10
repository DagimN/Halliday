from tkinter import *
from PIL import ImageTk, Image
from numpy import asarray
from shapely.geometry import Point, Polygon
import cv2
import math
import keyboard
import os
import csv
import base64

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
history = []

#TODO: Improve
polygonCoords = []
polygonCoordsX = []
polygonCoordsY = []

objectCoordinates = []
image = cv2.imread(tilesDirectory + '\\' + tiles[tileIndex])
objectImage = Image.new('RGBA', (image.shape[0], image.shape[1]), color=(255, 255, 255, 0))
test = ImageTk.PhotoImage(objectImage)
label1 = Label(image=test)

def mouse_callback(event, x, y, flags, params):
    copyPressed = True if keyboard.is_pressed('x') else False
    erasePressed = True if keyboard.is_pressed('e') else False
    tagPressed = True if keyboard.is_pressed('p') else False

    if event == cv2.EVENT_MOUSEMOVE and copyPressed:
        getPixelsFromBrush(x, y, 10, erase=False)
    if event == cv2.EVENT_MOUSEMOVE and erasePressed:
        getPixelsFromBrush(x, y, 10, erase=True)
    if event == cv2.EVENT_LBUTTONDOWN:
        getPixelsFromPolygon(x, y)

def getPixelsFromBrush(x, y, radius, erase):
    global objectCoordinates, image, objectImage, label1
    label1.destroy()

    for i in range(0,radius):
        for j in range(0,radius):
            if(checkIfInsideBrush(x + i, y + j)):
                color = [255, 255, 255, 0] if erase else image[y+j,x+i]
                objectCoordinates.append((x + i, y + j, color))
                objectImage.putpixel( (x + i,y + j), (color[2], color[0], color[1], color[3]) if erase else (color[2], color[0], color[1]))

    test = ImageTk.PhotoImage(objectImage)
    label1 = Label(image=test)
    label1.image = test
    label1.place(x=0, y=0)

def getPixelsFromPolygon(x, y):
    global polygonCoordsX, polygonCoordsY, image, objectCoordinates, objectImage, label1
    label1.destroy()

    if not polygonCoordsX.__contains__((x, y)):
        polygonCoordsX.append((x, y))
        polygonCoordsY.append((y, x))
        polygonCoords.append((x, y))

        polygonCoordsX.sort()
        polygonCoordsY.sort()
        arrayInitialX, yitemp = polygonCoordsX[0]
        arrayInitialY, xitemp = polygonCoordsY[0]
        arrayFinalX, yftemp = polygonCoordsX[len(polygonCoordsX) - 1]
        arrayFinalY, xftemp = polygonCoordsY[len(polygonCoordsY) - 1]
        
        rangeX = arrayFinalX - arrayInitialX
        rangeY = arrayFinalY - arrayInitialY

        if len(polygonCoordsX) > 2:
            for i in range(0, rangeX):
                for j in range(0, rangeY):
                    polygon = Polygon(polygonCoords)
                    point = Point(arrayInitialX + i, arrayInitialY + j)

                    if point.within(polygon):
                        color = image[arrayInitialY+j,arrayInitialX+i]
                        objectCoordinates.append((arrayInitialX + i, arrayInitialY + j, color))
                        objectImage.putpixel( (arrayInitialX + i, arrayInitialY + j), (color[2], color[0], color[1]))
        
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
    global options, classDropDown, classImages, objectImage, classLabel, tiles, tileIndex
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

    tileName = tiles[tileIndex]
    classImages.append((className, objectImage, tileName))

    classLabel = Label(window, text=str(len(classImages)))
    classLabel.place(x=320, y=80)

def addClass():
    global image, objectImage, classImages, label1, polygonCoords, polygonCoordsX, polygonCoordsY
    objectImage = Image.new('RGBA', (image.shape[0], image.shape[1]), color=(255, 255, 255, 0))
    test = ImageTk.PhotoImage(objectImage)
    label1.destroy()
    label1 = Label(image=test)
    label1.place(x=0, y=0)

    polygonCoords.clear()
    polygonCoordsX.clear()
    polygonCoordsY.clear()

def finish():
    global image, tiles, tileIndex, classImages, polygonCoords, polygonCoordsX, polygonCoordsY
    
    writeToDataset()
    classImages.clear()
    
    polygonCoords.clear()
    polygonCoordsX.clear()
    polygonCoordsY.clear()

    if tileIndex < len(tiles) - 1:
        while True:  
            tileIndex = tileIndex + 1
        
            if not history.__contains__(tiles[tileIndex]):
                break
        
        image = cv2.imread(tilesDirectory + '\\' + tiles[tileIndex])
        cv2.imshow("What objects are there?", image)
    else:
        #TODO: Use a dialog to print the message
        print('Classification Completed')

def writeToDataset():
    global classImages
    csvHeader = ['filename', 'previousfname', 'classname', 'destination', 'objectdata']

    for image in classImages:
        className, objectImage, previousfname = image
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

        writer.writerow([fileName, previousfname, className, directory, base64.b64encode(asarray(objectImage))])
        objectImage.save(directory + fileName)
        outputFile.close()

def selectAll():
    global image, objectImage
    objectImage = Image.open(tilesDirectory + '\\' + tiles[tileIndex])
    submitClass()
    finish()
    
def traceBackPrevious():
    global tileIndex, tiles, image

    for className in os.listdir(classDirectory):
        csvDirectory = f'{classDirectory}{className}\\dataset.csv'

        if os.path.exists(csvDirectory):
            inputFile = open(csvDirectory, 'r')

            for row in csv.reader(inputFile):
                if not (row[1] == 'previousfname' and history.__contains__(row[1])):
                    history.append(row[1])
    
    while history.__contains__(tiles[tileIndex]):
        tileIndex = tileIndex + 1
        image = cv2.imread(tilesDirectory + '\\' + tiles[tileIndex])
        cv2.imshow("What objects are there?", image)

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

traceBackPrevious()

window.mainloop()
