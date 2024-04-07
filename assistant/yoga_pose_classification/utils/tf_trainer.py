# import os
# import random
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras import layers, models
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from assistant.controllers.constants import constants
# from tensorflow.keras.models import load_model

# # Set the path to your dataset
# dataset_path = os.path.join(constants.YOGA_POSE_ROOT_DIR, constants.YOGA_IMAGE_DIR)

# # Define parameters
# batch_size = 32
# img_size = (224, 224)
# # epochs = 10

# # Function to load and preprocess the data
# def load_and_preprocess_data(dataset_path, img_size, batch_size, validation_split):
#     train_datagen = ImageDataGenerator(rescale=1./255, validation_split=validation_split)

#     train_generator = train_datagen.flow_from_directory(
#         dataset_path,
#         target_size=img_size,
#         batch_size=batch_size,
#         class_mode='categorical',
#         subset='training'
#     )

#     validation_generator = train_datagen.flow_from_directory(
#         dataset_path,
#         target_size=img_size,
#         batch_size=batch_size,
#         class_mode='categorical',
#         subset='validation'
#     )

#     return train_generator, validation_generator

# '''
# This function defines and returns a CNN architecture suitable for image classification with the
# specified input shape and number of classes. It uses convolutional and max-pooling layers to
# extract hierarchical features, followed by fully connected layers for classification
# '''
# # Function to create a simple convolutional neural network
# def create_model(input_shape, num_classes):
#     model = models.Sequential()
#     model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(64, (3, 3), activation='relu'))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Conv2D(128, (3, 3), activation='relu'))
#     model.add(layers.MaxPooling2D((2, 2)))
#     model.add(layers.Flatten())
#     model.add(layers.Dense(128, activation='relu'))
#     model.add(layers.Dense(num_classes, activation='softmax'))

#     model.compile(optimizer='adam',
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])

#     return model

# # # Load and preprocess the data
# # train_generator, validation_generator = load_and_preprocess_data(dataset_path, img_size, batch_size)

# # # Create the model
# # num_classes = len(train_generator.class_indices)
# # model = create_model(input_shape=(img_size[0], img_size[1], 3), num_classes=num_classes)

# # # Train the model
# # history = model.fit(
# #     train_generator,
# #     epochs=epochs,
# #     validation_data=validation_generator
# # )

# # # Save the model
# # model.save('image_classifier_model.h5')

# # # Evaluate the model
# # loss, accuracy = model.evaluate(validation_generator)
# # print(f'Validation accuracy: {accuracy * 100:.2f}%')


# def load_keras_model(file_path):
#     """
#     Load a Keras model from a .h5 file.

#     Parameters:
#     - file_path (str): The path to the .h5 file containing the saved model.

#     Returns:
#     - model: The loaded Keras model.
#     """
#     try:
#         model = load_model(file_path)
#         print(f"Model loaded successfully from {file_path}")
#         return model
#     except Exception as e:
#         print(f"Error loading model from {file_path}: {e}")
#         return None
