import os
import random
import shutil

BATCH_SIZE = 2048
COLLECTION_PATH = 'dataset\\collection'
TRAINING_PATH = 'dataset\\training'

classDirectories = os.listdir(COLLECTION_PATH)

for directory in classDirectories:
    rawImageDirectoryPath = f'{COLLECTION_PATH}\\{directory}'
    rawMaskDirectoryPath = f'{COLLECTION_PATH}\\{directory}\\segmentation'

    rawImages = os.listdir(rawImageDirectoryPath)
    rawImages.pop(rawImages.index('segmentation'))
    random.shuffle(rawImages)
    
    for i in range(0, len(rawImages), BATCH_SIZE):
        batchIndex = len(os.listdir(f'{TRAINING_PATH}\\{directory}\\Batches'))
        trainingImageDirectoryPath = f'{TRAINING_PATH}\\{directory}\\Batches\\batch_{batchIndex + 1}\\train_images'
        trainingMasksDirectoryPath = f'{TRAINING_PATH}\\{directory}\\Batches\\batch_{batchIndex + 1}\\train_masks'
        print(i)
        
        os.makedirs(trainingImageDirectoryPath)
        os.makedirs(trainingMasksDirectoryPath)
        
        
        for j in range(i, i + BATCH_SIZE):
            srcImageFilePath = f'{rawImageDirectoryPath}\\{rawImages[j]}'
            srcMaskFilePath = f'{rawMaskDirectoryPath}\\{rawImages[j]}'
            destImageFilePath = f'{trainingImageDirectoryPath}\\{rawImages[j]}'
            destMaskFilePath = f'{trainingMasksDirectoryPath}\\{rawImages[j]}'

            try:
                shutil.copy2(srcImageFilePath, destImageFilePath)
                shutil.copy2(srcMaskFilePath, destMaskFilePath)
            except: pass                

    
    


