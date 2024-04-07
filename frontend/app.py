
import streamlit as st
import openai
import numpy as np
from pymongo import MongoClient
import requests
import datetime
import time
import base64

st.set_page_config(page_title="Wellness Corner", layout="wide")

#####################

# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
    <img src="https://img.freepik.com/premium-photo/wide-banner-with-many-random-square-hexagons-charcoal-dark-black-color_105589-1820.jpg" alt="Banner Image">
</div>
<style>
    .banner {
        width: 160%; /* Adjust the width as needed */
        max-width: 950px; /* Limit the maximum width */
        height: 200px;
        overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""


# st.components.v1.html(custom_html)

st.markdown(custom_html, unsafe_allow_html=True)

####################
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer{
    visibility:visible;
    }
</style>
"""

# predict_api_url = "http://34.68.34.160:5000/predict?model_name=image_classifier_model_20240206_102019.pth"
# predict_api_url = "http://35.222.235.81:5000/predict?model_name=image_classifier_model_20240206_102019.pth"

predict_api_url = "http://127.0.0.1:5000/predict?model_name=image_classifier_model_20240206_102019.pth"
booking_api_url = "http://127.0.0.1:5050/chat"
pose_info_url = "http://127.0.0.1:5010/pose_info"
client_url = "mongodb://127.0.0.1:27017/"
locator_url = "http://127.0.0.1:5030/locator"


def connect_to_database():
    client = MongoClient(client_url)
    db = client.yoga_db
    # db = client.admin

    collections = {
        "slots_collection": db.slots,
        "learn_and_grow_collection": db.learn_and_grow,
        "feedback_collection" : db.feedback,
        "user_booking_collection" : db.user_booking
    }
    return collections

def get_collections():
    collections = connect_to_database()
    slots_collection = collections["slots_collection"]
    learn_and_grow_collection = collections["learn_and_grow_collection"]
    feedback_collection = collections["feedback_collection"]
    user_booking_collection = collections["user_booking_collection"]
    # print("MongoDB connected successfully!!")
    return slots_collection, learn_and_grow_collection, feedback_collection,user_booking_collection


def save_feedback(helpful, suggestions):
    feedback_collection = get_collections()[2]
    feedback_data = {"helpful": helpful, "suggestions": suggestions, "feedback_date" : datetime.datetime.now() }
    feedback_collection.insert_one(feedback_data)

def main():
    st.sidebar.title("Wellness Corner")
    logo_path = "frontend/modules/logo/logo.png"
    # st.image(logo_path, use_column_width=True)
    st.sidebar.image(logo_path, use_column_width=True)

# About Us Section
    st.sidebar.title("About Us")
    # st.title("Wellness Corner")
    st.sidebar.write("We are a world leading research, educational and professional publisher. Visit our main website for more information.")

# Title Section


    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(hide_menu, unsafe_allow_html=True)

    options = {
        "Detect Your Yoga Pose": "🧘‍♂️",
        "Session Booking": "📅",
        "Learn and Grow": "📚",
        "Feedback": "📝"
    }

    selected_button = st.sidebar.selectbox("Go to", list(options.keys()), format_func=lambda x: f"{options[x]} {x}")

    if selected_button == "Detect Your Yoga Pose":
        st.write("Welcome to Detect Your Yoga Pose!")
        display_detect_yoga_pose()

    elif selected_button == "Session Booking":
        st.write("Welcome to Session Booking!")
        book_session()

    elif selected_button == "Learn and Grow":
        display_learn_and_grow()

    elif selected_button == "Feedback":
        display_feedback()

def display_detect_yoga_pose():
        uploaded_file = st.file_uploader("Upload Your Yoga image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.write("")
            st.write("Detecting pose...")
            detected_pose = predict_and_display_pose(uploaded_file)
            if detected_pose is not None:
                more_info = st.radio("Do you want to know more about the pose?", ("Yes", "No"), index=None)
                if more_info == "Yes":
                    pose_data = {"pose": detected_pose}
                    response = requests.post(pose_info_url, json=pose_data)
                    if response.status_code == 200:
                        pose_info = response.json()
                        if "assistant" in pose_info:
                            assistant_response = pose_info["assistant"]
                            st.write("**Pose Details:**")
                            st.write(assistant_response)
                        else:
                            st.write("No assistant response found in the API result.")
                    else:
                        st.write("Failed to retrieve pose information. Please try again later.")

def display_learn_and_grow():
        st.write("Welcome to Learn and Grow!")
        learn_and_grow_collection = get_collections()[1]
        display_categories_from_db(learn_and_grow_collection)


def display_feedback():
    st.subheader("Feedback Form")
    st.write("Appreciate your time for feedback!")
    helpful = st.radio("Does SpringerNature wellness corner helpful?", ["Yes", "No"])
    suggestions = st.text_area("Do you have any other suggestions for us?")
    if st.button("Submit Feedback"):
        save_feedback(helpful, suggestions)
        st.success("Thank you for your feedback!")


def display_categories_from_db(learn_and_grow_collection):
    categories = ["Practice", "Meditation", "Anatomy", "Wellbeing", "Philosophy", "Recipes"]
    selected_option = st.radio("Choose a category to explore:", categories, key="category_radio", index=None)
    learn_and_grow_collection = get_collections()[1]

    st.write("")

    if selected_option is not None:
        st.subheader(f"{selected_option} :")
        contents = learn_and_grow_collection.find({"category": selected_option})
        count = sum(1 for _ in contents)

        if count > 0:
            contents = learn_and_grow_collection.find({"category": selected_option})
            for content in contents:
                st.write("**Title:**", content["title"])
                st.write("**Description:**", content["description"])
                if "related_articles" in content:
                    st.write("**Related Articles:**")
                    for article in content["related_articles"]:
                        st.write(f"<a href='{article['link']}'>{article['title']}</a>", unsafe_allow_html=True)
                st.write("")
        else:
            st.write("No content found for this category.")


def book_session():
    session_type = st.radio("Which type of session would you like to book?", ("Online", "Offline"), index=None)

    if session_type == "Online":
        user_contact = st.text_input("Enter your emailid")
        user_input = st.text_input("Enter your query")

        if st.button("Book Session"):
            with st.spinner('Booking session...'):
                st.caption(':blue[**Booking Bot:**]')
                container = st.container(border=True)
                booking_data = {"user_input": user_input, "user_contact": user_contact}
                response = requests.post(booking_api_url, json=booking_data)
                if response.status_code == 200:
                    container.write(response.json().get("assistant", ""))
                else:
                    st.write("Failed to book session. Please try again later.")

    elif session_type == "Offline":
            location = st.text_input("Enter your area or postal code")
            if st.button("Find Session"):
                with st.spinner('Finding session...'):
                    st.caption(':blue[**Locator Bot:**]')
                    container = st.container(border=True)

                    response = requests.post(locator_url, json={"location": location})
                    if response.status_code == 200:
                        container.write(response.json().get("assistant", ""))
                    else:
                        st.write("Failed to find session. Please try again later.")


def predict_and_display_pose(image_file):
    files = {"image": image_file}
    response = requests.post(predict_api_url, files=files)
    if response.status_code == 200:
        result = response.json()
        if "prediction" in result:
            predicted_pose = result["prediction"]
            st.success("Pose detected: {}".format(predicted_pose))
            return predicted_pose
        else:
            st.error("Prediction not found in response.")
            return None
    else:
        st.error("Error occurred during pose detection.")
        st.write(response.text)
        return None



# Run the Streamlit app
if __name__ == "__main__":
    main()
footer = "&copy; 2024 SpringerNature"
st.markdown(f'<footer style="position: fixed; bottom: 0; right: 0; padding: 10px;">{footer}</footer>', unsafe_allow_html=True)

support_icon = "🛠️"
support_text = "Support"
st.sidebar.markdown(f'<a href="https://support.springernature.com/en/support/home" style="text-decoration: none;">{support_icon} {support_text}</a>', unsafe_allow_html=True)
