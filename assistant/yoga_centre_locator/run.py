from flask import Flask, jsonify, render_template, request
from assistant.controllers.constants import constants
from assistant.pose_info.utils.openaikit import OpenAIKit
from assistant.pose_info.utils.message_builder import MSGBUILDER
from assistant.controllers.helpers import HELPER
from assistant.controllers import get_logger

# from controllers import helpers
logger = get_logger.get_logger_object(__name__,constants.LOCATOR_LOGS_PATH, constants.LOCATOR_LOGS_FILENAME)


helpers_obj = HELPER(log_folder=constants.LOCATOR_LOGS_PATH,log_filename=constants.LOCATOR_LOGS_FILENAME)

prompt_data = helpers_obj.file_handler(filepath=f"{constants.LOCATOR_ROOT_DIR}/yoga_centre_locator.yaml")
system_msg = prompt_data["SYSTEM_PROMPT"]
# Initialize Flask app
app = Flask(__name__)


@app.route('/locator', methods=['POST'])
def locator():
    try:
        # logger.info("in CHAT")
        data = request.get_json()
        pose = data.get('location')
        messages =  MSGBUILDER(system_msg).construct_msg(pose)
        llm = OpenAIKit()
        model = "gpt-4-turbo-preview"
        res = llm.get_chat_completion(messages=messages,model=model)
        output = res.choices[0].message.content
        api_response = jsonify({"assistant": output, "status_code":200})

    except Exception as e:
        api_response = helpers_obj.error_handling(e)

    return api_response


if __name__ == '__main__':
    app.run(debug=True,host=constants.LOCATOR_APP_HOST, port=constants.LOCATOR_APP_PORT)
