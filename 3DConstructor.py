#NOTE: Shadow angle(Black surface) can include height information to get from
import cv2
import PIL
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

maskLocation = 'dataset\\Building\\val_images\\SMTile10003.png'
tempFilePath = 'tempRaw.png'
tempCleanFilePath = 'tempClean.png'
NOISE_THRESHOLD = 10

#TODO: Make a function that removes all lines in pixels that are not above a certain threshold
def cleanNoise(edged_image):
    viewedPixelCoordinates = []
    previousCoordinates = []
    mapObjects = []
    mapObject = []

    xIndex = 0
    yIndex = 0
    rows = edged_image.shape[0] 
    columns = edged_image.shape[1]
    AREA_VIEW = 3
    

    while xIndex < rows:
        while yIndex < columns:
            north = (xIndex - 1, yIndex) if xIndex - 1 >= 0 else 0
            northEast = (xIndex - 1, yIndex + 1) if xIndex - 1 >= 0 and yIndex + 1 < columns else 0
            northWest = (xIndex - 1, yIndex - 1) if xIndex - 1 >= 0 and yIndex - 1 >= 0 else 0
            south = (xIndex + 1, yIndex) if xIndex + 1 < rows else 0
            southEast = (xIndex + 1, yIndex + 1) if yIndex + 1 < columns and xIndex + 1 < rows else 0
            southWest = (xIndex + 1, yIndex - 1) if yIndex - 1 >= 0 and xIndex + 1 < rows else 0
            east = (xIndex, yIndex + 1) if yIndex + 1 < columns else 0
            west = (xIndex, yIndex - 1) if yIndex - 1 >= 0 else 0
            center = (xIndex, yIndex)
            
            directions = [center, north, northEast, east, southEast, south, southWest, west, northWest]
            validCoordinates = []
            path = 0
            
            if not viewedPixelCoordinates.__contains__(center):
                #Checks area for white pixels
                for direction in directions:
                    if not direction == 0 and edged_image[direction[0], direction[1]] == 255 and not viewedPixelCoordinates.__contains__(direction):
                        validCoordinates.append(direction)
                        path += 1
                        
                        if path > 1 and not previousCoordinates.__contains__(direction):
                            previousCoordinates.append(direction)
                    else:
                        if previousCoordinates.__contains__(direction) and path == 0:
                            previousCoordinates.remove(direction)
                
                viewedPixelCoordinates.append(center)
                
                if not path == 0:
                    mapObject.append(validCoordinates[0])
                    xIndex, yIndex = validCoordinates[0]
                    
                else:
                    if len(mapObject) > NOISE_THRESHOLD:
                        mapObjects.append(mapObject)
                        xIndex = 0
                        yIndex = 0
                    else:
                        for coord in mapObject:
                            edged_image[coord[0], coord[1]] = 0
                    
                        if len(previousCoordinates) > 0:
                            previousCoordinate = previousCoordinates[0]
                            previousCoordinates.remove(previousCoordinate)
                            xIndex, yIndex = previousCoordinate   
                        else:
                            xIndex = 0
                            yIndex = 0
                    mapObject.clear()
            else:
                yIndex += 1
        xIndex += 1
        yIndex = 0 if yIndex > columns else yIndex + 1               

    edged_image = np.array(edged_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempCleanFilePath, edged_image)
    return cv2.imread(tempCleanFilePath)

            
def showImages(loaded_image, edged_image, clear_edged_image):
    plt.figure(figsize=(20,20))
    
    plt.subplot(1,3,1)
    plt.imshow(loaded_image,cmap="gray")
    plt.axis("off")
    plt.title("Original Image")

    plt.subplot(1,3,2)
    plt.imshow(edged_image,cmap="gray")
    plt.axis("off")
    plt.title("Canny Edge Detected Image")

    plt.subplot(1,3,3)
    plt.imshow(clear_edged_image,cmap="gray")
    plt.axis("off")
    plt.title("Noise Cleared")

    plt.show()

def main():
    loaded_image = cv2.imread(maskLocation)
    loaded_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2GRAY)

    non_black_image = [[0 if (j < 60) else j for j in i] for i in gray_image]
    non_black_image = np.array(non_black_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempFilePath, non_black_image)
    non_black_image = cv2.imread(tempFilePath)

    edged_image = cv2.Canny(non_black_image, threshold1=100, threshold2=170)
    cv2.imwrite(tempFilePath, edged_image)
    clear_edged_image = cleanNoise(edged_image=edged_image)

    showImages(loaded_image=loaded_image, edged_image=cv2.imread(tempFilePath), clear_edged_image=clear_edged_image)

    

if __name__ == "__main__":
    main()