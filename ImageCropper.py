import cv2
import os
import time

tilesDirectory = "C:\\Users\\dagmn\\Pictures\\3D Map Dataset\\tiles - 40m"

def generateTiles(tilesFolder):
    i = 0
    index = 1
    for file in os.listdir(tilesFolder):
        directory = "C:\\Users\\dagmn\\Pictures\\3D Map Dataset\\generated tiles (150)"
        print(tilesFolder + '\\' + file)
        image = cv2.imread(tilesFolder + '\\' + file)

        for x in range(0, len(image), 150):
            for y in range(0, len(image[x]), 150):
                i = i + 1
                fileName = '\\SMTile' + str(i) + '.png'
                w= x + 150
                h= y + 150
                crop_image = image[x:w, y:h]

                cv2.imshow("Cropped", crop_image)
                cv2.imwrite(directory + fileName, crop_image)
                
                num_images = (len(image) / 150) * (len(image[x]) / 150) 
                print(fileName + ' Progress: ' + str((i/(num_images * index) * 100)))
        
        index = index + 1

def writeTileImages():
    for itemClass in classes:
        i = 0
        directory = "C:\\Users\\dagmn\\Pictures\\3D Map Dataset\\classified tiles (150)\\" + itemClass
        os.mkdir(directory) 
        for item in process_data:
            print(item['class'])
            if(item['class'] == itemClass):
                i = i + 1
                cv2.imwrite(directory + "\\" + item['class'] + str(i) + '.png', crop_image)
    
generateTiles(tilesDirectory)