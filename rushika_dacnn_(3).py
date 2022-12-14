# -*- coding: utf-8 -*-
"""RUSHIKA-DACNN (3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j-gScAJajWcAmozcQwe2uZTuQwTWTxHD
"""

import tensorflow as tf
#import tensorflow_datasets as tfds
import numpy as np
import os
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from skimage import io
import zipfile

#https://www.gcptutorials.com/post/load-mnist-data-with-tensorflow-datsets
# train_dataset,info = tfds.load('horses_or_humans', with_info = True, split='train', shuffle_files=True)
# val_dataset,val_info = tfds.load('horses_or_humans', with_info = True, split='test', shuffle_files=True)

# train_dataset = train_dataset.take(300)
# val_dataset = val_dataset.take(60)

#Getting data from location
!wget --no-check-certificate \
    https://storage.googleapis.com/laurencemoroney-blog.appspot.com/horse-or-human.zip \
    -O /content/horse-or-human.zip

!wget --no-check-certificate \
    https://storage.googleapis.com/laurencemoroney-blog.appspot.com/validation-horse-or-human.zip \
    -O /content/validation-horse-or-human.zip

from google.colab import drive
drive.mount('/content/drive')

#Data which we got is in zip format. so, we are doing UNZIP.
local_zip = '/content/horse-or-human.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/horse-or-human')
local_zip = '/content/validation-horse-or-human.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/validation-horse-or-human')
zip_ref.close()



Train_Horses = r'/content/horse-or-human/horses/'
Train_Humans = r'/content/horse-or-human/humans/'
Validation_Horses = r'/content/validation-horse-or-human/horses/'
Validation_Humans = r'/content/validation-horse-or-human/humans/'

#https://pynative.com/python-count-number-of-files-in-a-directory/
Train_Horses_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/horse-or-human/horses'):
    Train_Horses_Images += len(Images)
print('Training Images Horses:', Train_Horses_Images)

#https://pynative.com/python-count-number-of-files-in-a-directory/
Train_Humans_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/horse-or-human/humans'):
    Train_Humans_Images += len(Images)
print('Training Images Humans:', Train_Humans_Images)

#https://pynative.com/python-count-number-of-files-in-a-directory/
Validation_Horses_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/validation-horse-or-human/horses'):
    Validation_Horses_Images += len(Images)
print('Validation Images Horse:', Validation_Horses_Images)

#https://pynative.com/python-count-number-of-files-in-a-directory/
Validation_Humans_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/validation-horse-or-human/humans'):
    Validation_Humans_Images += len(Images)
print('Validation Images Human:', Validation_Humans_Images)

Horses_Train_Images = []
Humans_Train_Images = []
Horses_Test_Images = []
Humans_Test_Images = []

Horses_Train_Images_Path = os.listdir(Train_Horses)
Humans_Train_Images_Path = os.listdir(Train_Humans)
Horses_Validation_Images_Path = os.listdir(Validation_Horses)
Humans_Validation_Images_Path = os.listdir(Validation_Humans)

for i, name_image in enumerate(Horses_Train_Images_Path):    
    if (name_image.split('.')[1] == 'png'):        
        pic = io.imread(Train_Horses + name_image)        
        pic = Image.fromarray(pic)        
        pic = pic.resize((224,224)) 
        Horses_Train_Images.append(np.array(pic))


for i, name_image in enumerate(Humans_Train_Images_Path):    
    if (name_image.split('.')[1] == 'png'):        
        pic = io.imread(Train_Humans + name_image)        
        pic = Image.fromarray(pic)        
        pic = pic.resize((224,224)) 
        Humans_Train_Images.append(np.array(pic))

for i, name_image in enumerate(Horses_Validation_Images_Path):    
    if (name_image.split('.')[1] == 'png'):        
        pic = io.imread(Validation_Horses + name_image)        
        pic = Image.fromarray(pic)        
        pic = pic.resize((224,224)) 
        Horses_Test_Images.append(np.array(pic))

for i, name_image in enumerate(Humans_Validation_Images_Path):    
    if (name_image.split('.')[1] == 'png'):        
        pic = io.imread(Validation_Humans + name_image)        
        pic = Image.fromarray(pic)        
        pic = pic.resize((224,224)) 
        Humans_Test_Images.append(np.array(pic))


Horses_Train_Images_Array = np.array(Horses_Train_Images)
Humans_Train_Images_Array = np.array(Humans_Train_Images)
Horses_Test_Images_Array = np.array(Horses_Test_Images)
Humans_Test_Images_Array = np.array(Humans_Test_Images)

#Showing up random images in Training horse images 
plt.imshow(Horses_Train_Images_Array[100])

#Showing up random images in Training horse images 
plt.imshow(Humans_Train_Images_Array[25])

plt.imshow(Horses_Test_Images_Array[0])

plt.imshow(Humans_Test_Images_Array[50])

"""**Data set Size Before Augmentation**"""

print("Horses Train Images Array:",len(Horses_Train_Images_Array))
print("Humans Train Images Array:",len(Humans_Train_Images_Array))
print("Horses Test Images Array:",len(Horses_Test_Images_Array))
print("Humans Test Images Array:",len(Humans_Test_Images_Array))

"""**Augmentation Techniques applied to Dataset**"""

#https://www.analyticsvidhya.com/blog/2021/06/offline-data-augmentation-for-multiple-images/
train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

"""**Making New folder to Store the Train Horses Augmented Images**"""

#https://stackoverflow.com/questions/65926475/how-to-create-a-folder-in-my-google-drive-through-google-colab-code
import os

#creating new folder to store the augmented images 
os.makedirs('/content/New_Train_Horses')

#https://www.analyticsvidhya.com/blog/2021/06/offline-data-augmentation-for-multiple-images/
i = 0
for batch in train_datagen.flow(Horses_Train_Images_Array, batch_size=128,
                          save_to_dir= r'/content/New_Train_Horses',
                          save_prefix='Horsesnew',
                          save_format='png'):    
    i += 1    
    if i > 128:        
        break

"""**After Augmentation Train Horses Images Count**"""

Augmented_Train_Horses_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/New_Train_Horses'):
    Augmented_Train_Horses_Images += len(Images)
print('Augmented Training Images Horses:', Augmented_Train_Horses_Images)

os.makedirs('/content/New_Test_Horses')

validation_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

i = 0
for batch in validation_datagen.flow(Horses_Test_Images_Array, batch_size=128,
                          save_to_dir= r'/content/New_Test_Horses',
                          save_prefix='Horsesnew',
                          save_format='png'):    
    i += 1    
    if i > 128:        
        break

Augmented_Test_Horses_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/New_Test_Horses'):
    Augmented_Test_Horses_Images += len(Images)
print('Augmented Training Images Horses:', Augmented_Test_Horses_Images)

os.makedirs('/content/New_Train_Humans')
i = 0
for batch in validation_datagen.flow(Humans_Train_Images_Array, batch_size=128,
                          save_to_dir= r'/content/New_Train_Humans',
                          save_prefix='Horsesnew',
                          save_format='png'):    
    i += 1    
    if i > 128:        
        break
Augmented_Train_Humans_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/New_Train_Humans'):
    Augmented_Train_Humans_Images += len(Images)
print('Augmented Training Images Humans:', Augmented_Train_Humans_Images)

os.makedirs('/content/New_Test_Humans')
i = 0
for batch in validation_datagen.flow(Humans_Test_Images_Array, batch_size=128,
                          save_to_dir= r'/content/New_Test_Humans',
                          save_prefix='Horsesnew',
                          save_format='png'):    
    i += 1    
    if i > 128:        
        break
Augmented_Test_Humans_Images = 0
for root_dir, cur_dir, Images in os.walk(r'/content/New_Test_Humans'):
    Augmented_Test_Humans_Images += len(Images)
print('Augmented Training Images Humans:', Augmented_Test_Humans_Images)

#https://valueml.com/image-classification-using-convolution-neural-network-cnn-in-python/
model=tf.keras.models.Sequential([
                                  tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(300, 300, 3)),
                                  tf.keras.layers.MaxPooling2D(2,2),
                                  tf.keras.layers.Conv2D(32,(3,3),activation='relu'),
                                  tf.keras.layers.MaxPooling2D(2,2),
                                  tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                                  tf.keras.layers.MaxPooling2D(2,2),
                                  tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                                  tf.keras.layers.MaxPooling2D(2,2),
                                  tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
                                  tf.keras.layers.MaxPooling2D(2,2),
                                  tf.keras.layers.Flatten(),
                                  tf.keras.layers.Dense(512,activation='relu'),
                                  tf.keras.layers.Dense(1,activation='sigmoid')])

from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen=ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')
                                
validation_datagen=ImageDataGenerator(
      rescale=1./255,
      rotation_range=40,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')

train_generator=train_datagen.flow_from_directory(
    '/content/horse-or-human',
    target_size=(300,300),
    batch_size=128,
    class_mode='binary'
)
validation_generator=validation_datagen.flow_from_directory(
    '/content/validation-horse-or-human',
    target_size=(300,300),
     batch_size=128,
     class_mode='binary'
    
)

train_datagen1=ImageDataGenerator()
validation_datagen1=ImageDataGenerator()

train_generator1=train_datagen1.flow_from_directory(
    '/content/horse-or-human',
    target_size=(300,300),
    batch_size=128,
    class_mode='binary'
)
validation_generator1=validation_datagen1.flow_from_directory(
    '/content/validation-horse-or-human',
    target_size=(300,300),
     batch_size=128,
     class_mode='binary'
    
)

from tensorflow.keras.optimizers import RMSprop
model.compile(loss="binary_crossentropy", optimizer=RMSprop(learning_rate=0.001), metrics=['accuracy'])
history = model.fit(train_generator1, epochs=5, validation_data=validation_generator1)

# summarize history for accuracy
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

history1 = model.fit(train_generator, epochs=10, validation_data=validation_generator)

# summarize history for accuracy
plt.plot(history1.history['loss'])
plt.plot(history1.history['val_loss'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# summarize history for accuracy
plt.plot(history1.history['accuracy'])
plt.plot(history1.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

"""**CNN Using Augmentor Library**"""

# https://github.com/mdbloice/Augmentor/blob/master/notebooks/Augmentor_Keras.ipynb
# Importing Augmentor
import Augmentor

# Creating Pipeline to Augmentor Library
Augmentor_CNN = Augmentor.Pipeline("/content/horse-or-human")

# By applying status function to the Augmentor pipeline we can find how many operations are made to the pipeline
Augmentor_CNN.status()

# We are performing eight operations to the pipeline

Augmentor_CNN.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
Augmentor_CNN.zoom(probability=0.3, min_factor=1.1, max_factor=1.6)
Augmentor_CNN.flip_left_right(probability=0.4)
Augmentor_CNN.flip_top_bottom(probability=0.8)
Augmentor_CNN.rotate90(probability=0.1)
Augmentor_CNN.random_distortion(probability=0.2, grid_height=2, grid_width=2, magnitude=4)
Augmentor_CNN.rotate180(probability=0.4)
Augmentor_CNN.rotate270(probability=0.4)
# Giving samples to generate
Augmentor_CNN.sample(500)
# Finding status of the pipeline how many operations are done to the pipeline
Augmentor_CNN.status()





