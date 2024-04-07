from flask import Flask, jsonify, render_template, request
from assistant.controllers.constants import constants
from assistant.controllers.helpers import HELPER
from assistant.controllers import get_logger
from assistant.database_handler.mongodb import MongoDBHandler

# from controllers import helpers
logger = get_logger.get_logger_object(__name__,constants.DB_LOGS_PATH, constants.DB_LOGS_FILENAME)


helpers_obj = HELPER(log_folder=constants.DB_LOGS_PATH,log_filename=constants.DB_LOGS_FILENAME)

prompt_data = helpers_obj.file_handler(filepath=f"{constants.YOGA_POSE_INFO_ROOT_DIR}/pose_prompt.yaml")
# system_msg = prompt_data["SYSTEM_PROMPT"]
# Initialize Flask app
app = Flask(__name__)


@app.route('/insert', methods=['POST'])
def insert():
    try:
        logger.info("in DB INSERT ROUTE")
        # ------------------------------ #
        data = request.get_json()
        db_name = data.get('db_name')
        collection_name = data.get('collection_name')
        file_name = data.get('file_name')

        overwrite=request.args.get('overwrite') or False
        if type(overwrite) is not bool:
            overwrite = helpers_obj.check_boolean_param(overwrite)
        # ------------------------------ #
        data = helpers_obj.file_handler(filepath=f"{constants.DB_ROOT_DIR}/data/{file_name}")
        db = MongoDBHandler(database_name=db_name, collection_name=collection_name)
        if overwrite:
            try:
                # remove collection
                db.collection.drop()
                logger.info(f"Collection: '{collection_name}' is removed from DB : '{db_name}'")
                print(f"Collection: '{collection_name}' is removed from DB : '{db_name}'")
            except:
                pass
        db.insert_data(data,True)
        msg = f"Data of length : {len(data)} is inserted into the collection '{collection_name}' of DB:'{db_name}' {'with overwrite' if overwrite else 'without overwrite'}"
        # ------------------------------ #
        api_response = jsonify({"assistant": msg,"status_code":200})

    except Exception as e:
        api_response = helpers_obj.error_handling(e)

    return api_response


if __name__ == '__main__':
    app.run(debug=True,host=constants.DB_APP_HOST, port=constants.DB_APP_PORT)