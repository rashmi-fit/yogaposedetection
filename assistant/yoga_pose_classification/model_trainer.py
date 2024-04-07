import json
import tensorflow as tf
print(tf.__version__)
import traceback
from assistant.yoga_pose_classification.utils import helper_functions,tf_trainer
from assistant.controllers.constants import constants
import scipy
import os
# from tensorflow.compat.v1 import get_default_graph
from PIL import ImageFile
from datetime import datetime
ImageFile.LOAD_TRUNCATED_IMAGES=True

#global var
dataset_path = os.path.join(constants.YOGA_POSE_ROOT_DIR, constants.YOGA_IMAGE_DIR)
batch_size =  32
img_size=(224,224)

epochs = 1
validation_split  =  0.20

# Load and preprocess the data
train_generator, validation_generator = tf_trainer.load_and_preprocess_data(dataset_path, img_size, batch_size, validation_split)
# Create the model
num_classes = len(train_generator.class_indices)
model = tf_trainer.create_model(input_shape=(img_size[0], img_size[1], 3), num_classes=num_classes)

# # Train the model
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=validation_generator
)
# Save the model
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
model.save(f'{constants.YOGA_POSE_MODEL_LOC}/image_classifier_model_{current_datetime}.h5')
with open(f'{constants.YOGA_POSE_MODEL_LOC}/image_classifier_model_{current_datetime}.json', 'w') as f:
    json.dump(train_generator.class_indices, f)
