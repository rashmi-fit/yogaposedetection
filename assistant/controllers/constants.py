"""
Defining the constants
"""
from dataclasses import dataclass
import os
@dataclass(frozen=True)
class ConstantNamespace:
    """
    Defining the constants
    """
    #######################################################
    # ----------------- SESSION BOOKING ----------------- #
    #######################################################
    SESSION_BOOKING_ROOT_DIR = "assistant/session_booking_assistant" # make sure this is correct
    SESSION_BOOKING_LOGS_PATH = os.path.join(SESSION_BOOKING_ROOT_DIR, "logs")
    SESSION_BOOKING_LOGS_FILENAME = SESSION_BOOKING_ROOT_DIR.split("/")[1]
    SESSION_BOOKING_THREAD_FILE = os.path.join(SESSION_BOOKING_ROOT_DIR , "thread_data.json")
    SESSION_BOOKING_APP_HOST = "0.0.0.0"
    SESSION_BOOKING_APP_PORT = 5050
    # SESSION_BOOKING_DBNAME = "admin"#"yoga_db"
    SESSION_BOOKING_DBNAME = "yoga_db"
    SESSION_BOOKING_SLOT_COLLECTIONNAME = "slots"
    SESSION_BOOKING_USERINFO_COLLECTIONNAME = "user_booking"

    #######################################################
    # ----------------- YOGA POSE DETECTION----------------- #
    #######################################################
    YOGA_POSE_ROOT_DIR = "assistant/yoga_pose_classification" # make sure this is correct
    YOGA_IMAGE_DIR = "image_dataset/Yoga/Input"
    YOGA_POSE_LOGS_PATH = os.path.join(YOGA_POSE_ROOT_DIR, "logs")
    YOGA_POSE_LOGS_FILENAME = YOGA_POSE_ROOT_DIR.split("/")[1]
    YOGA_POSE_APP_HOST = "0.0.0.0"
    YOGA_POSE_APP_PORT = 5000
    YOGA_POSE_MODEL_LOC = "model/trained_models"
    #######################################################
    # ----------------- YOGA POSE INFO CHATGPT----------------- #
    #######################################################
    YOGA_POSE_INFO_ROOT_DIR = "assistant/pose_info" # make sure this is correct
    # YOGA_IMAGE_DIR = "image_dataset/Yoga/Input"
    YOGA_POSE_INFO_LOGS_PATH = os.path.join(YOGA_POSE_INFO_ROOT_DIR, "logs")
    YOGA_POSE_INFO_LOGS_FILENAME = YOGA_POSE_INFO_ROOT_DIR.split("/")[1]
    YOGA_POSE_INFO_APP_HOST = "0.0.0.0"
    YOGA_POSE_INFO_APP_PORT = 5010
    # YOGA_POSE_MODEL_LOC = "model/trained_models"
    #######################################################
    # ----------------- DB HANDLER----------------- #
    #######################################################
    DB_ROOT_DIR = "assistant/database_handler" # make sure this is correct
    # YOGA_IMAGE_DIR = "image_dataset/Yoga/Input"
    DB_LOGS_PATH = os.path.join(DB_ROOT_DIR, "logs")
    DB_LOGS_FILENAME = DB_ROOT_DIR.split("/")[1]
    DB_APP_HOST = "0.0.0.0"
    DB_APP_PORT = 5020
    # YOGA_POSE_MODEL_LOC = "model/trained_models"
    #######################################################
    # ----------------- YOGA LOCATOR CHATGPT----------------- #
    #######################################################
    LOCATOR_ROOT_DIR = "assistant/yoga_centre_locator" # make sure this is correct
    # YOGA_IMAGE_DIR = "image_dataset/Yoga/Input"
    LOCATOR_LOGS_PATH = os.path.join(LOCATOR_ROOT_DIR, "logs")
    LOCATOR_LOGS_FILENAME = LOCATOR_ROOT_DIR.split("/")[1]
    LOCATOR_APP_HOST = "0.0.0.0"
    LOCATOR_APP_PORT = 5030
    # YOGA_POSE_MODEL_LOC = "model/trained_models"

# Create an instance of the ConstantNamespace class
constants = ConstantNamespace()
