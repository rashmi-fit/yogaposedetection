Create a virtual enviornment
### python3 -m venv venv

### .\venv\Scripts\activate

To install flask
### pip install flask

To run file
### python3 -m flask run

### stop the application by Control +C


To install tensorflow
### pip3 install tensorflow

To install numpy
### pip3 install numpy

To install tflearn
### pip3 install tflearn

Verify the version
### pip3 show tensorflow

Create virtual env either through pip or through python3
### pipenv shell or python3 -m venv venv


To run a file inside yoga pose, be in the users directory (eg : rashmeemayee.mohapatra) and type below in terminal
###  python -m  assistant.yoga_pose_classification.run

Copy the local url (eg : http://127.0.0.1:5060)

open post man for yoga sequencing and hit it and hit all the urls and then show it


control +c to exit it

To run the flask frontend

### python -m  frontend.run

This will run the session_booking_chatbot flask app @port: 5050
## nohup python -m assistant.session_booking_assistant.run > session_booking_assistant.log 2>&1 &

 This will run the yoga_pose_classification flask app @port: 5060

##  nohup python -m assistant.yoga_pose_classification.run > yoga_pose_classification.log 2>&1 &

To run the tests file execute below

## python -m unittest discover -s tests

next thing :
- implement login page
- implement session booking page from db
