from PIL import ImageGrab
import mouse
import pyautogui
import ctypes
import time

distanceX, distanceY = 4, 3
currentProgressX, currentProgressY = 0, 0
initialX, initialY = 13, 138
finalX, finalY = 1919, 988
saveImageX, saveImageY = 378, 103
saveButtonX, saveButtonY = 393, 106
saveX, saveY = 752, 673
readyStatusColor = (99, 145, 178)
mapQualityStatusScreenLocationX, mapQualityStatusScreenLocationY = 1896, 996 
imageIndex = 0

def minimizeVsCode():
    user32 = ctypes.WinDLL('user32')
    SW_MINIMIZE = 2
    hWnd = user32.GetForegroundWindow()

    user32.ShowWindow(hWnd, SW_MINIMIZE)

def snapMapImages(): 
    minimizeVsCode()
    mode = 0
    
    for i in range(distanceX):
        for j in range(distanceY):
            moveToTile(mode)
            time.sleep(20)

            #while True:
                #screenColor = ImageGrab.grab().load()
                #if(screenColor[mapQualityStatusScreenLocationX, mapQualityStatusScreenLocationY] == readyStatusColor):
            saveMapImage()    
                #break

        mode = 2
        moveToTile(mode)
        
        mode = 1 if mode == 0 else 0  

def moveToTile(mode):
    #Normal
    if(mode == 0):
        mouse.drag(initialX, finalY, initialX, initialY, duration=0.25)

    #Reverse
    if(mode == 1):
        mouse.drag(initialX, initialY, initialX, finalY, duration=0.25)

    #Increment
    if(mode == 2):
        mouse.drag(initialX, initialY, finalX, initialY, duration=0.25)

def saveMapImage():
    mouse.move(saveButtonX, saveButtonY)
    mouse.click('left')
    
    time.sleep(0.5)

    global imageIndex
    imageIndex = imageIndex + 1
    
    pyautogui.write('Tile' + str(imageIndex))

    time.sleep(0.5)

    mouse.move(saveX, saveY)
    mouse.click('left')

    time.sleep(20)

snapMapImages()