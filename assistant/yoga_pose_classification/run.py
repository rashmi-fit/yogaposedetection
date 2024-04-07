"""
Flask App for Yoga Pose Identification
"""
# import assistant
import json
import traceback
from flask import Flask, request, jsonify,Response, stream_with_context
import assistant
# from assistant.yoga_pose_classification.utils import helper_functions
from assistant.yoga_pose_classification.utils import pytorch_trainer
from assistant.controllers.constants import constants
from assistant.controllers.helpers import HELPER
from assistant.controllers import get_logger
import imageio as iio
# from tensorflow.keras.preprocessing import image
import numpy as np
# import scipy
# from PIL import ImageFile
import warnings
from werkzeug.utils import secure_filename

import os
from PIL import Image
import torch
warnings.filterwarnings('ignore')

# ImageFile.LOAD_TRUNCATED_IMAGES=True
helpers_obj = HELPER(log_folder=constants.YOGA_POSE_LOGS_PATH,log_filename=constants.YOGA_POSE_LOGS_FILENAME)
logger = get_logger.get_logger_object(__name__, constants.YOGA_POSE_LOGS_PATH, constants.YOGA_POSE_LOGS_FILENAME)

app = Flask(__name__)

#--------------------------------#
# GLOBAL VARIABLE
dataset_path = os.path.join(constants.YOGA_POSE_ROOT_DIR, constants.YOGA_IMAGE_DIR)
batch_size =  32
img_size = (224,224)
epochs = 30
validation_split = 0.20
# ----------------------------------------------#
train_loader, test_loader, num_classes, classes, transformer = pytorch_trainer.create_data_loaders(dataset_path,img_size,batch_size,validation_split)
#--------------------------------#



def load_image(image_path):

    filename = secure_filename(image_path.filename)
    temp_folder = os.path.join(constants.YOGA_POSE_ROOT_DIR, 'temp')
    os.makedirs(temp_folder,exist_ok=True)
    temp_path = os.path.join(temp_folder, filename)
    image_path.save(temp_path)
    print(f'image is saved temporaily at :{temp_path}')
    img = Image.open(temp_path)
    return img


def request_checker(route):

    if route == "predict":
        # Check if the 'image' key is present in the request files
        if "image" in request.files:
            # Retrieve the input file
            input_file = request.files['image']
            if not input_file:
                raise ValueError("Missing 'image' file in form-data")
        else:
            raise ValueError("Missing 'image' key in form-data")

        # Perform image-specific processing on the input file
        # input_file = iio.imread(input_file)
        input_file = load_image(input_file)

        model_name = request.args.get("model_name")
        if not model_name:
            raise ValueError("Missing 'model_name' arg in params")

        return model_name,input_file
    elif route == "eval":
        model_name = request.args.get("model_name")
        if not model_name:
            raise ValueError("Missing 'model_name' arg in params")

        return model_name

    else:
        raise Exception ("Invalid API Route")



@app.route("/datasummary", methods=["GET"])
def datasummary():
    try:
        api_response = helper_functions.analyze_folder(dataset_path)

        api_response = jsonify(api_response)

    except Exception as e:
        api_response = helpers_obj.error_handling(e)

    return api_response

@app.route("/get_model_list", methods=["POST","GET"])
def get_model_list():
    try:
        folder_path =os.path.join(constants.YOGA_POSE_ROOT_DIR,constants.YOGA_POSE_MODEL_LOC)
        files = [x for x in os.listdir(folder_path) if '.pth' in x]
        api_response = {"models":files,"status_code":200}

    except Exception as e:
        api_response = helpers_obj.error_handling(e)

    return api_response

@app.route("/eval", methods=["POST","GET"])
def eval():
    print('-----------EVALUATION----------')
    try:
        folder_path = os.path.join(constants.YOGA_POSE_ROOT_DIR,constants.YOGA_POSE_MODEL_LOC)
        model_name = request_checker(route="eval")

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Load the saved model
        loaded_model = pytorch_trainer.load_model_weight(num_classes)
        loaded_model.eval()
        loaded_model.load_state_dict(torch.load(f'{folder_path}/{model_name}'))
        loaded_model.to(device)

        msg = pytorch_trainer.eval_model(test_loader,loaded_model,num_classes)


        api_response = {"Test Score":msg,
                        "status_code":200}
        print('---------SUCCESS---------')
    except Exception as e:
        api_response = helpers_obj.error_handling(e)
        print('---------ERROR---------')
    print('---------END---------')
    return api_response


@app.route("/predict", methods=["POST","GET"])
def predict():
    print('-----------PREDICTION----------')
    try:
        folder_path = os.path.join(constants.YOGA_POSE_ROOT_DIR,constants.YOGA_POSE_MODEL_LOC)
        model_name, input_image = request_checker(route="predict")

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Load the saved model
        loaded_model = pytorch_trainer.load_model_weight(num_classes)
        loaded_model.eval()
        loaded_model.load_state_dict(torch.load(f'{folder_path}/{model_name}'))
        loaded_model.to(device)

        Predicted_class = pytorch_trainer.predict_class(input_image,loaded_model,transformer,classes)

        api_response = {"prediction":Predicted_class,
                        # "probability":probs,
                        "status_code":200}
        print('---------SUCCESS---------')
    except Exception as e:
        api_response = helpers_obj.error_handling(e)
        print('---------ERROR---------')
    print('---------END---------')
    return api_response
##############################################
if __name__ == "__main__":
    app.run(debug =True,host=constants.YOGA_POSE_APP_HOST,port=constants.YOGA_POSE_APP_PORT)
##############################################
