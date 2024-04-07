import streamlit as st
import openai
import cv2
import numpy as np
from pymongo import MongoClient
import requests


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.yoga_db
feedback_collection = db.feedback
learn_and_grow_collection = db.learn_and_grow

# Function to open the chatbot using OpenAI GPT-4
def open_chatbot(user_input, section):
    if section == "Learn and Grow":
        search_result = perform_search(user_input)
        st.markdown(f'<p class="bot-reply">Bot: {search_result}</p>', unsafe_allow_html=True)
        st.text("Bot: " + search_result)
    else:

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )

        # Display the response from the chatbot
        if response['choices']:
            bot_response = response['choices'][0]['text'].strip()
            st.markdown(f'<p class="bot-reply">Bot: {bot_response}</p>', unsafe_allow_html=True)
            st.text("Bot: " + bot_response)
        else:
            st.text("Bot: Error in processing your request. Please try again.")

# Function to perform a simple search for the Learn and Grow section

def perform_search(query):
    # Retrieve content dynamically from the MongoDB collection
    result = learn_and_grow_collection.find_one({"title": query.lower()})

    if result:
        return result.get("content", "Sorry, I couldn't find information on that topic.")
    else:
        return "Sorry, I couldn't find information on that topic."

# Function to detect yoga pose from an uploaded image
def detect_yoga_pose(image):
    # Your pose detection code here (using OpenCV and a pre-trained model)

    # Placeholder code -
    detected_pose = "Warrior II Pose"
    return detected_pose

# Function to save feedback in MongoDB
def save_feedback(helpful, suggestions):
    feedback_data = {"helpful": helpful, "suggestions": suggestions}
    feedback_collection.insert_one(feedback_data)

# Streamlit App

# User input for the chatbot
def user_interaction(selected_button):
    if selected_button == "Session Booking":
        user_contact = st.text_input("Enter your emailid:", "")
    else:
        user_contact = ""  # Set user_contact to empty string for other sections

    user_input = st.text_input(f"Enter your query for ({selected_button}):", "")

    if st.button("Send"):
        if selected_button == "Session Booking":
            # Handle session booking interaction
            book_session(user_input, user_contact)
        else:
            # For other sections, interact with the chatbot
            open_chatbot(user_input, selected_button)



def book_session(user_input, user_contact):
    # Make a request to the booking API
    # booking_api_url = "http://34.172.2.68:5050/chat"  # Replace with your actual API URL
    booking_api_url = "http://127.0.0.1:5050/chat"  # Replace with your actual API URL

    booking_data = {"user_contact": user_contact, "user_input": user_input } # , "section": "Session Booking"}

    try:
        response = requests.post(booking_api_url, json=booking_data)
        if response.status_code == 200:
            # Display the response from the booking API
            st.text("Booking Bot: " + response.json().get("assistant", ""))
        else:
            st.text(f"Booking Bot: Error {response.status_code} in processing your request.")
    except Exception as e:
        st.text(f"Booking Bot: Error in processing your request. {str(e)}")
