
import traceback
from assistant.controllers import get_logger
from assistant.controllers.constants import constants
import os
from PIL import Image
import tensorflow as tf
from google.cloud import storage
from google.cloud.exceptions import NotFound
# import tflite_runtime.interpreter as tflite

logger = get_logger.get_logger_object(__name__, constants.YOGA_POSE_LOGS_PATH,constants.YOGA_POSE_LOGS_FILENAME)

def bytes_to_megabytes(bytes_size):
    return round(bytes_size / (1024 * 1024),3)

def analyze_gcs_bucket(bucket_name):
    logger.info(f"bucket_name:{bucket_name}")
    # Create a GCS client
    client = storage.Client()

    # Get the bucket
    try:
        bucket = client.get_bucket(bucket_name)
    except NotFound:
        return {"status_code": 404, "error": "Bucket not found"}

    data = [{"Total Folders": 0}]  # Initialize the data list

    # List all blobs (files and folders) in the bucket
    blobs = list(bucket.list_blobs())
    # blobs = list_blobs(bucket)
    data = {"Total Files":len(blobs)}
    return data
    for folder_name, folder_blobs in blobs.items():
        folder_data = {"Folder": folder_name, "Files": len(folder_blobs), "TotalSizeMB": 0, "MaxFileSizeMB": 0, "MinFileSizeMB": 0}

        # Calculate size metrics for the folder
        folder_data["TotalSizeMB"] = bytes_to_megabytes(sum(b.size for b in folder_blobs))
        folder_data["MaxFileSizeMB"] = bytes_to_megabytes(max(b.size for b in folder_blobs) if folder_blobs else 0)
        folder_data["MinFileSizeMB"] = bytes_to_megabytes(min(b.size for b in folder_blobs) if folder_blobs else 0)

        data.append(folder_data)

    data[0]["Total Folders"] = len(data) - 1  # Update the total folder count
    data.append({"status_code": 200})
    logger.info(f"Input Data Summary is Generated:\n{data}")
    return data

def list_blobs(bucket, prefix=""):
    blobs = {}
    delimiter = "/"
    page_token = None

    while True:
        blobs_iter = bucket.list_blobs(prefix=prefix, delimiter=delimiter, page_token=page_token)

        for blob in blobs_iter:
            if blob.name.endswith(delimiter):
                # Blob represents a "folder"
                subfolder_name = blob.name.rstrip(delimiter)
                blobs.update(list_blobs(bucket, prefix=subfolder_name + "/"))
            else:
                # Blob represents a file
                blobs.setdefault(prefix, []).append(blob)

        page_token = blobs_iter.next_page_token
        if not page_token:
            break

    return blobs
    for blob in blobs:
        print(blob)
        # Check if the blob is a folder (ends with "/")
        if blob.name.endswith("/"):
            folder_name = blob.name.rstrip("/")
            folder_data = {"Folder": folder_name, "Files": 0, "TotalSizeMB": 0, "MaxFileSizeMB": 0, "MinFileSizeMB": 0}

            # Count the number of files in the folder and calculate size metrics
            folder_blobs = [b for b in blobs if b.name.startswith(folder_name) and b.name != folder_name]
            folder_data["Files"] = len(folder_blobs)
            folder_data["TotalSizeMB"] = bytes_to_megabytes(sum(b.size for b in folder_blobs))
            folder_data["MaxFileSizeMB"] = bytes_to_megabytes(max(b.size for b in folder_blobs) if folder_blobs else 0)
            folder_data["MinFileSizeMB"] = bytes_to_megabytes(min(b.size for b in folder_blobs) if folder_blobs else 0)

            data.append(folder_data)

    data[0]["Total Folders"] = len(data) - 1  # Update the total folder count
    data.append({"status_code": 200})
    logger.info(f"Input Data Summary is Generated:\n{data}")
    return data

def analyze_folder(path):
    data = [{"Total Folders":len(os.listdir(path))}]

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            file_count = len(files)
            total_size_bytes = sum(os.path.getsize(os.path.join(folder_path, f)) for f in files)
            max_file_size_bytes = max(os.path.getsize(os.path.join(folder_path, f)) for f in files) if files else 0
            min_file_size_bytes = min(os.path.getsize(os.path.join(folder_path, f)) for f in files) if files else 0

            folder_data = {
                "Folder": folder,
                "Files": file_count,
                "TotalSizeMB": bytes_to_megabytes(total_size_bytes),
                "MaxFileSizeMB": bytes_to_megabytes(max_file_size_bytes),
                "MinFileSizeMB": bytes_to_megabytes(min_file_size_bytes)
            }

            data.append(folder_data)
    data.append({"status_code":200})
    logger.info(f"Input Data Summary is Generated:\n{data}")
    return data


def is_corrupted_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return False
    except  (IOError, SyntaxError, OSError) as e:
        return True
    except tf.errors.OpError:
        return True

def delete_corrupted_images(folder_path):
    data = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_corrupted_image(file_path):
                corrupted_image_info ={
                    "file":file_path
                }
                print(f"Deleting corrupted file: {file_path}")
                os.remove(file_path)
                data.append(corrupted_image_info)
    data.append({"status_code":200})
    return data
