from PIL import ImageGrab
import mouse
import pyautogui
import ctypes
import time

EYE_SIGHT = 4.2
distanceX, distanceY = 4, 4
currentProgressX, currentProgressY = 0, 0
initialX, initialY = 13, 138
finalX, finalY = 1919, 910
saveImageX, saveImageY = 378, 103
saveButtonX, saveButtonY = 393, 106
saveX, saveY = 752, 673
readyStatusColor = (99, 145, 178)
savingStatusColor = (239, 235, 231)
mapReadyStatusLocationX, mapReadyStatusLocationY = 1896, 996 
saveStatusLocationX, saveStatusLocationY = 919, 599
imageIndex = 0
refreshTime = 30
saveTime = 60

def minimizeVsCode():
    user32 = ctypes.WinDLL('user32')
    SW_MINIMIZE = 2
    hWnd = user32.GetForegroundWindow()

    user32.ShowWindow(hWnd, SW_MINIMIZE)

def snapMapImages(): 
    minimizeVsCode()
    mode = False
    
    for i in range(distanceX):
        for j in range(distanceY):
            saveMapImage() 
            moveToTile(mode)
            time.sleep(1)

        saveMapImage() 
        moveToTile(mode, True)
        time.sleep(1)
        
        mode = not mode

def moveToTile(reverse, increment=False):
    #Increment
    if(increment):
        mouse.drag(finalX, initialY, initialX, initialY, duration=3)
    else:
        #Normal
        if(reverse):
            mouse.drag(initialX, initialY, initialX, finalY, duration=3)
        #Reverse
        else:
            mouse.drag(initialX, finalY, initialX, initialY, duration=3)
            

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

    time.sleep(1)

    while True:
        screenColor = ImageGrab.grab().load()
        if not(screenColor[saveStatusLocationX, saveStatusLocationY] == savingStatusColor):    
            break
        
    time.sleep(1)
    
snapMapImages()