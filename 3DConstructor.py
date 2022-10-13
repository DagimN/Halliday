#NOTE: Shadow angle(Black surface) can include height information to get from
import cv2
import PIL
import numpy as np
import random
import matplotlib.pyplot as plt
plt.style.use('seaborn')

maskLocation = 'dataset\\Building\\val_images\\SMTile10008.png'
tempFilePath = 'tempRaw.png'
tempCleanFilePath = 'tempClean.png'
tempVerticeFilePath = 'tempVertices.png'
NOISE_THRESHOLD = 80

def searchNoise(viewedPixelCoordinates, pendingCoordinates, center, mapObject, directions, edged_image):
    pathExists = False

    if not viewedPixelCoordinates.__contains__(center):
        viewedPixelCoordinates.append(center)

        if edged_image[center[1], center[0]] == 255:
            mapObject.append(center)

            for direction in directions:
                if edged_image[direction[1], direction[0]] == 255 and not mapObject.__contains__(direction):
                    pendingCoordinates.append(direction)
                    mapObject.append(direction)
                    pathExists = True
                    travelPath(direction[0], direction[1], viewedPixelCoordinates, pendingCoordinates, edged_image, mapObject, 1)    
                
        if not pathExists:
            if len(pendingCoordinates) == 0:
                clearPixels(edged_image, mapObject)
            else:
                coords = pendingCoordinates[0]
                pendingCoordinates.remove(pendingCoordinates[0])
                travelPath(coords[0], coords[1], viewedPixelCoordinates, pendingCoordinates, edged_image, mapObject, 1)    

def searchVertices(validPixelCoordinates, directions, AREA_VIEW, edged_image, center):
    rows = edged_image.shape[0]
    columns = edged_image.shape[1]
    if not validPixelCoordinates.__contains__(center):
            
        for direction in directions:
            for i in range(AREA_VIEW):
                if direction == directions[0] or direction == directions[2]:
                    posPointCoord = (direction[1], direction[0] + i if direction[0] + i < rows else direction[0])
                    negPointCoord = (direction[1], direction[0] - i if direction[0] - i < rows else direction[0])
                        
                    if edged_image[posPointCoord] == 255 and not validPixelCoordinates.__contains__(posPointCoord):
                        edged_image[posPointCoord] = 128
                        validPixelCoordinates.append(posPointCoord)
                        
                    if edged_image[negPointCoord] == 255 and not validPixelCoordinates.__contains__(negPointCoord):
                        edged_image[negPointCoord] = 128
                        validPixelCoordinates.append(negPointCoord)
                else:
                    posPointCoord = (direction[1] + i if direction[1] + i < columns else direction[1], direction[0])
                    negPointCoord = (direction[1] - i if direction[1] - i < columns else direction[1], direction[0])

                    if edged_image[posPointCoord] == 255 and not validPixelCoordinates.__contains__(posPointCoord):
                        edged_image[posPointCoord] = 128
                        validPixelCoordinates.append(posPointCoord)
                        
                    if edged_image[negPointCoord] == 255 and not validPixelCoordinates.__contains__(negPointCoord):
                        edged_image[negPointCoord] = 128
                        validPixelCoordinates.append(negPointCoord)
    
def chooseVertices(clear_edged_image):
    vertices_image = clear_edged_image
    verticeCoordinates = []
    AREA_VIEW = 7

    print('Choosing Vertices =>')

    for x in range(0, clear_edged_image.shape[0], AREA_VIEW):
        for y in range(0, clear_edged_image.shape[1], AREA_VIEW):
            travelPath(x, y, verticeCoordinates, None, vertices_image, None, AREA_VIEW)

    vertices_image = np.array(vertices_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempVerticeFilePath, vertices_image)
    return cv2.imread(tempVerticeFilePath)

def travelPath(xIndex, yIndex, viewedPixelCoordinates, pendingCoordinates, edged_image, mapObject, AREA_VIEW):
    rows = edged_image.shape[0]
    columns = edged_image.shape[1]

    north = (xIndex - AREA_VIEW if xIndex - AREA_VIEW >= 0 else 0, yIndex) 
    northEast = (xIndex - AREA_VIEW if xIndex - AREA_VIEW >= 0 else 0, yIndex + AREA_VIEW if yIndex + AREA_VIEW < columns else columns - 1)     
    northWest = (xIndex - AREA_VIEW if xIndex - AREA_VIEW >= 0 else 0, yIndex - AREA_VIEW if yIndex - AREA_VIEW >= 0 else 0)  
    south = (xIndex + AREA_VIEW if xIndex + AREA_VIEW < rows else rows - 1, yIndex) 
    southEast = (xIndex + AREA_VIEW if xIndex + AREA_VIEW < rows else rows - 1, yIndex + AREA_VIEW if yIndex + AREA_VIEW < columns else columns - 1)  
    southWest = (xIndex + AREA_VIEW if xIndex + AREA_VIEW < rows else rows - 1, yIndex - AREA_VIEW if yIndex - AREA_VIEW >= 0 else 0)  
    east = (xIndex, yIndex + AREA_VIEW if yIndex + AREA_VIEW < columns else columns - 1) 
    west = (xIndex, yIndex - AREA_VIEW if yIndex - AREA_VIEW >= 0 else 0) 
    center = (xIndex, yIndex)

    if AREA_VIEW == 1:
        directions = [north, northEast, east, southEast, south, southWest, west, northWest]
        searchNoise(viewedPixelCoordinates, pendingCoordinates, center, mapObject, directions, edged_image)
    else:
        directions = [north, east, south, west]
        searchVertices(viewedPixelCoordinates, directions, AREA_VIEW, edged_image, center)
                           
def clearPixels(edged_image, mapObject):
    size = len(mapObject)
    if not size == 0:
        pixelColor =  255 if size % 255 > NOISE_THRESHOLD else 0 

        for pixel in mapObject:
            edged_image[pixel[1], pixel[0]] = pixelColor
                                        
        mapObject.clear() 
                                    
def cleanNoise(edged_image):
    rows = edged_image.shape[0] 
    columns = edged_image.shape[1]
    yIndex = 0
    xIndex = 0
    viewedPixelCoordinates = []     
    mapObject = []
    validCoordinates = []    
    pendingCoordinates = []

    print('Cleaning Noise =>')

    while yIndex < columns:
        xIndex = 0
        while xIndex < rows:
            travelPath(xIndex, yIndex, viewedPixelCoordinates, pendingCoordinates, edged_image, mapObject, 1)
            xIndex += 1
                    
        yIndex += 1

    edged_image = np.array(edged_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempCleanFilePath, edged_image)
    return cv2.imread(tempCleanFilePath)   

def showImages(loaded_image, edged_image, clear_edged_image, vertices_image):
    plt.figure(figsize=(50,50))
    
    plt.subplot(1,4,1)
    plt.imshow(loaded_image,cmap="gray")
    plt.axis("off")
    plt.title("Original Image")

    plt.subplot(1,4,2)
    plt.imshow(edged_image,cmap="gray")
    plt.axis("off")
    plt.title("Canny Edge Detected Image")

    plt.subplot(1,4,3)
    plt.imshow(clear_edged_image,cmap="gray")
    plt.axis("off")
    plt.title("Noise Cleared")

    plt.subplot(1,4,4)
    plt.imshow(vertices_image,cmap="gray")
    plt.axis("off")
    plt.title("Choosen Vertices")

    plt.show()

def main():
    print('Started => ')
    loaded_image = cv2.imread(maskLocation)
    loaded_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2GRAY)

    non_black_image = [[0 if (j < 60) else j for j in i] for i in gray_image]
    non_black_image = np.array(non_black_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempFilePath, non_black_image)
    non_black_image = cv2.imread(tempFilePath)

    edged_image = cv2.Canny(non_black_image, threshold1=30, threshold2=260)
    cv2.imwrite(tempFilePath, edged_image)
    
    clear_edged_image = cleanNoise(edged_image=edged_image)
    vertices_image = cv2.imread(tempCleanFilePath)
    vertices_image = cv2.cvtColor(vertices_image,cv2.COLOR_BGR2GRAY)
    vertices_image = chooseVertices(vertices_image)

    showImages(loaded_image=loaded_image, edged_image=cv2.imread(tempFilePath), clear_edged_image=clear_edged_image, vertices_image=vertices_image)

if __name__ == "__main__":
    main()