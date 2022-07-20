import numpy as np
import pandas

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator   
from keras import utils as image

S_classifier = Sequential()
S_classifier.add(Conv2D(32, (3,3), input_shape=(150, 150, 3), activation='relu'))
S_classifier.add(MaxPooling2D(pool_size=(2,2)))
S_classifier.add(Flatten())
S_classifier.add(Dense(units=128, activation='relu'))
S_classifier.add(Dense(units=1, activation='sigmoid'))
S_classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory("dataset/training/", target_size=(150,150), batch_size=2, class_mode='binary')
test_set = test_datagen.flow_from_directory("dataset/test/", target_size=(150,150), batch_size=2, class_mode='binary')

S_classifier.fit(training_set, steps_per_epoch=len(training_set), epochs=10, validation_data=test_set, validation_steps=len(test_set))

test_image = image.load_img('dataset/predict/roof1.png')
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = S_classifier.predict(test_image)
print(result)