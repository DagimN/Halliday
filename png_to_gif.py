import os
from tkinter import filedialog as fd
from PIL import Image

directories = ["dataset/Building/val_masks"]

for directory in directories:
    for file in os.listdir(directory):
        filePath = f'{directory}\\{file}'
        im = Image.open(filePath)
        im.save(filePath.replace('.gif', '.png'))
        im.close()
