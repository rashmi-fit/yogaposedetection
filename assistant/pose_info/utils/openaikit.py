"""
OPENAI Class in a packaged way
"""
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from assistant.controllers import get_logger
from assistant.controllers.constants import constants
import tiktoken
from tenacity import (
   retry,
   stop_after_attempt,
   wait_random_exponential,
)  # for exponential backoff

load_dotenv()
API_KEY =os.getenv('OPENAI_KEY')
# logger = get_logger.get_logger_object(__name__, constants.LOGPATH, constants.LOGFILE)
class OpenAIKit:
   def __init__(self):
       self.client = OpenAI(api_key=API_KEY)
    #    self.model_list = constants.GPT_MODEL_LIST
   def count_tokens(self,text,model="gpt-3.5-turbo"):
       if text is None:
           num_tokens=0
       else:
           encoding = tiktoken.encoding_for_model(model)
           num_tokens=len(encoding.encode(text))
       return num_tokens
   @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
   def get_chat_completion(self,messages,model="gpt-3.5-turbo-16k",temperature=0.7, max_tokens=1000):
    #    if model not in self.model_list:
    #        raise Exception (f"[Error]:Invalid GPT model ('{model}'), Only provide the model from the list : {self.model_list}")
       try:
           result = self.client.chat.completions.create(
               model=model,
               messages=messages,
               temperature=temperature,
               max_tokens=max_tokens)
           return result
       except Exception as err:
           raise
