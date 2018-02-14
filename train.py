import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, AveragePooling2D
from keras import backend as K
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
import numpy as np
from PIL import Image

CHARS = {'4': 2, '5': 3, 'D': 11, 'B': 9, 'R': 22, 'F': 13, '9': 7, 'A': 8, '3': 1, 'V': 26, 'U': 25, '6': 4, 'J': 16, 'T': 24, 'X': 28, 'M': 18, '2': 0, 'Y': 29, 'H': 15, 'G': 14, 'C': 10, '7': 5, 'Q': 21, 'N': 19, '8': 6, 'W': 27, 'S': 23, 'K': 17, 'E': 12, 'P': 20, 'Z': 30}

index = [0] * 31
for k,v in CHARS.items():
    index[v] = k



img_rows, img_cols = 30, 54
if K.image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)


batch_size = 20
num_classes = len(index)
epochs = 10

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    # shear_range=0.2,
    # zoom_range=0.2,
    # horizontal_flip=True
)
test_daragen = ImageDataGenerator(
    rescale=1. / 255
)

train_generator = train_datagen.flow_from_directory(
    'train',
    target_size=(img_rows, img_cols),
    batch_size=batch_size,
    class_mode='categorical',
    color_mode='grayscale',
    # classes=CHARS
)
test_generator = train_datagen.flow_from_directory(
    'validate',
    target_size=(img_rows, img_cols),
    batch_size=batch_size,
    class_mode='categorical',
    color_mode='grayscale',
    # classes=CHARS
)
print('data loaded')

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.75))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.RMSprop(), metrics=['accuracy'])

model.fit_generator(
    train_generator,
    steps_per_epoch=len(train_generator) // batch_size,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=len(test_generator) // batch_size
)
print(train_generator.class_indices)
print(test_generator.class_indices)

model.save('first_try.h5')
