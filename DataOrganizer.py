import os

BATCH_SIZE = 2048
COLLECTION_PATH = 'dataset\\collection'
TRAINING_PATH = 'dataset\\training'

classDirectories = os.listdir(COLLECTION_PATH)

for directory in classDirectories:
    rawImageDirectoryPath = f'{COLLECTION_PATH}\\{directory}'
    rawMaskDirectoryPath = f'{COLLECTION_PATH}\\{directory}\\segmentation'
    trainingImageDirectoryPath = f'{TRAINING_PATH}\\{directory}\\train_images'
    trainingMaskDirectoryPath = f'{TRAINING_PATH}\\{directory}\\train_masks'
    validationImageDirectoryPath = f'{TRAINING_PATH}\\{directory}\\val_images'
    validationMasksDirectoryPath = f'{TRAINING_PATH}\\{directory}\\val_masks'

    rawImages = os.listdir(rawImageDirectoryPath)
    rawMasks = os.listdir(rawMaskDirectoryPath)

    
    


