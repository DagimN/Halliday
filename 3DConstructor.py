#NOTE: Shadow angle(Black surface) can include height information
import cv2
import PIL
import numpy as np
import random
import matplotlib.pyplot as plt
from stl import mesh

plt.style.use('seaborn')
maskLocation = 'dataset\\Building\\val_images\\SMTile10003.png'
tempFilePath = 'tempRaw.png'
tempVerticeFilePath = 'tempVertices.png'
tempCleanFilePath = 'tempClean.png'
NOISE_THRESHOLD = 35

def cleanNoise(edged_image):
    rows = edged_image.shape[0]
    columns = edged_image.shape[1]
    viewedPixelCoordinates = []
    validPixelCoordinates = []
    mapObjects = []

    for x in range(rows):
        for y in range(columns):
            travelPath(x, y, viewedPixelCoordinates, validPixelCoordinates, mapObjects, edged_image)

    for mapObject in mapObjects:
        for pixel in mapObject:
            if len(mapObject) < NOISE_THRESHOLD:
                edged_image[pixel[1], pixel[0]] = 0
    
    edged_image = np.array(edged_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempCleanFilePath, edged_image)
    return {'objects': mapObjects, 'image': cv2.imread(tempCleanFilePath)}

def travelPath(xIndex, yIndex, viewedPixelCoordinates, validPixelCoordinates, mapObjects, edged_image):
    rows = edged_image.shape[0]
    columns = edged_image.shape[1]

    north = (xIndex - 1 if xIndex - 1 >= 0 else 0, yIndex) 
    northEast = (xIndex - 1 if xIndex - 1 >= 0 else 0, yIndex + 1 if yIndex + 1 < columns else columns - 1)     
    northWest = (xIndex - 1 if xIndex - 1 >= 0 else 0, yIndex - 1 if yIndex - 1 >= 0 else 0)  
    south = (xIndex + 1 if xIndex + 1 < rows else rows - 1, yIndex) 
    southEast = (xIndex + 1 if xIndex + 1 < rows else rows - 1, yIndex + 1 if yIndex + 1 < columns else columns - 1)  
    southWest = (xIndex + 1 if xIndex + 1 < rows else rows - 1, yIndex - 1 if yIndex - 1 >= 0 else 0)  
    east = (xIndex, yIndex + 1 if yIndex + 1 < columns else columns - 1) 
    west = (xIndex, yIndex - 1 if yIndex - 1 >= 0 else 0) 
    center = (xIndex, yIndex)

    directions = [north, northEast, east, southEast, south, southWest, west, northWest]
    pathExists = False
    
    if not viewedPixelCoordinates.__contains__(center):
        viewedPixelCoordinates.append(center)
            
        if edged_image[center[1], center[0]] == 255:
            validPixelCoordinates.append(center)
                
            for direction in directions: 
                if edged_image[direction[1], direction[0]] == 255:
                    pathExists = True
                    travelPath(direction[0], direction[1], viewedPixelCoordinates, validPixelCoordinates, mapObjects, edged_image) 

        if not pathExists and not len(validPixelCoordinates) == 0:
            mapObject = []
                
            for pixel in validPixelCoordinates:
                mapObject.append(pixel)
                
            mapObjects.append(mapObject)
            validPixelCoordinates.clear()

def showImages(loaded_image, edged_image, clear_edged_image):
    plt.figure(figsize=(50,50))
    
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

def createMesh(mapObjects):
    vertices = []
    faces = []
    
    for verticesCoords in mapObjects:
        for coords in verticesCoords:
            vertices.append((coords[0], coords[1], 0))
        for coords in verticesCoords:
            vertices.append((coords[0], coords[1], 30))

    #TODO: Optimize Construction
    for index, vertice in enumerate(vertices):
        if vertice[2] == 0:
            faces.append([index, (index + 1) % len(vertices), vertices.index((vertice[0], vertice[1], 30))])
            #faces.append([index, vertices.index((vertice[0], vertice[1], 30)), (vertices.index((vertice[0], vertice[1], 30)) + 1) % len(vertices)])
        else:
            faces.append([(index - 1) % len(vertices), vertices.index((vertice[0], vertice[1], 0)), index])
        #     faces.append([index, vertices.index((vertice[0], vertice[1], 0)), (vertices.index((vertice[0], vertice[1], 0)) + 1) % len(vertices)])

    vertices = np.array(vertices)
    faces = np.array(faces)
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    
    for i, face in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[face[j], :]

    cube.save('cube.stl')
    print("DONE!!!")

def main():
    print('Started => ')
    loaded_image = cv2.imread(maskLocation)
    loaded_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(loaded_image,cv2.COLOR_BGR2GRAY)

    non_black_image = [[0 if (j < 60) else j for j in i] for i in gray_image]
    non_black_image = np.array(non_black_image, dtype=np.dtype('f8'))
    cv2.imwrite(tempFilePath, non_black_image)
    non_black_image = cv2.imread(tempFilePath)

    edged_image = cv2.Canny(non_black_image, threshold1=64, threshold2=512)
    cv2.imwrite(tempFilePath, edged_image)
    
    cleared_image = cleanNoise(edged_image)

    createMesh(cleared_image['objects'])
    showImages(loaded_image=loaded_image, edged_image=cv2.imread(tempFilePath), clear_edged_image=cv2.imread(tempCleanFilePath))

if __name__ == "__main__":
    main()