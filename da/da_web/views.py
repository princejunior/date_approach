# views.py
from datetime import timezone,datetime
import os
import json
import csv
import difflib

import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .functions.recognition_functions import solar_recognition_function, homeowner_ai
from .functions.open_ai import open_ai_conversation, open_ai_conversation_ex
# from .functions.speech_to_text import speech_to_text
from .functions.text_to_speech import text_to_speech
import speech_recognition as sr

def speech_to_text():
    # Create a recognizer object
    r = sr.Recognizer()
    
    # Use the microphone as source for input
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.2)
        
        # Listen for the user's input
        audio = r.listen(source)
        
        # Using Google to recognize audio
        try:
            text = r.recognize_google(audio)
            return text
        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))
            return None
        except sr.UnknownValueError:
            print("Unknown error occurred")
            return None

def convert_speech_to_text(request):
    
    if request.method == 'POST':
        # Extract the text from the POST request
        data = request.POST
        text = data.get('text', '')
        # print(text)
        if text:
            # Write the converted text to a file
            output_text(text)
            
            # Render the template with the text
            return render(request, 'pages/speech_to_text.html', {'text': text})
        else:
            return JsonResponse({'error': 'Failed to convert speech to text'})
    else:
        return render(request, 'pages/speech_to_text.html')
    
def output_text(text):
    try:
        with open("da_web/output.txt", "r+") as f:
            lines = f.readlines()
            # Check if the last line matches the current text (to avoid duplicates)
            if lines and text + "\n" == lines[-1]:
                print("Duplicate text detected, skipping write.")
                return  # Skip writing the text if it's a duplicate
            
            # If it's not a duplicate, append the text
            f.write(text + "\n")
    except FileNotFoundError:
        # Handle the case where the file does not exist by creating it and writing the text
        with open("output.txt", "w") as f:
            f.write(text + "\n")
# def output_text(text):
#     with open("output.txt", "a") as f:
#         f.write(text + "\n")

# def __main__():
#     keywords_to_search = ["company", "employer", "work for"]
#     matching_messages = search_keywords(keywords_to_search)
#     for message in matching_messages:
#         print("Timestamp:", message["timestamp"])
#         print("Role:", message["role"])
#         print("Message:", message["message"])
#         print()
#     return

# Define the ChatCompletionMessage class
class ChatCompletionMessage:
    def __init__(self, message):
        self.message = message

    def to_json(self):
        # Convert the object attributes to a JSON-serializable dictionary
        # return {'message': self.message}
        return self.message
    

def simulate_conversation(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Get AI response using OpenAI conversation
        ai_response = open_ai_conversation(user_input)

        # Check if AI response is valid
        if ai_response is not None:
            # Create a ChatCompletionMessage object
            completion_message = ChatCompletionMessage(ai_response)

            # Serialize the object to JSON using the custom method
            json_data = completion_message.to_json()

            # Log user input and AI response
            log_conversation(role="user", message=user_input)
            log_conversation(role="ai_model", message=json_data)

            # Return AI response as JSON
            return JsonResponse({'ai_response': ai_response})

        else:
            # If AI response is invalid, return an error response
            return JsonResponse({'error': 'Invalid AI response'}, status=400)
    
    # If request method is not POST, render the template without context
    return render(request, 'pages/simulate_conversation.html', {})

def load_conversations(request):
    with open('conversation_data/conversation_log.json') as file:
        conversation_log = json.load(file)
    # print(conversation_log)
    return render(request, 'pages/load_conversations.html', {'conversation_log': conversation_log})

def log_conversation(role, message):
    # Create the conversation_data directory if it doesn't exist
    conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
    if not os.path.exists(conversation_data_dir):
        os.makedirs(conversation_data_dir)
    
    # Construct the file path for the conversation log JSON file
    file_name = 'conversation_log.json'
    file_path = os.path.join(conversation_data_dir, file_name)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a new entry for the user's input or AI response
    log_entry = {"timestamp": timestamp, "role": role, "message": message}

    # Load existing data from the file or initialize as an empty list
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, mode='r') as file:
            data = json.load(file)
    else:
        data = []

    # Append the new log entry to the data
    data.append(log_entry)

    # Write the updated data back to the file
    with open(file_path, mode='w') as file:
        json.dump(data, file, indent=4)
    # Explicitly close the file
    file.close()


# Create your views here.
def home(request):
    # Create the conversation_data directory if it doesn't exist
    conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
    if not os.path.exists(conversation_data_dir):
        os.makedirs(conversation_data_dir)
    
    # Construct the file path for the conversation log JSON file
    file_name = 'conversation_log.json'
    file_path = os.path.join(conversation_data_dir, file_name)

    # Load existing data from the file or initialize as an empty list
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, mode='r') as file:
            data = json.load(file)
    else:
        data = []

    # Write the updated data back to the file
    with open(file_path, mode='w') as file:
        json.dump(data, file, indent=4)
    # Explicitly close the file
    file.close()
    df = pd.DataFrame(data)
    # print(df) 
    
    return render(request, 'pages/home.html')

# Functions for the homepage
def ai_response():
    return
def text_to_speech ():
    return
def word_value(): 
    return

def feedback(request):
    return render(request, 'pages/home.html')


def word_recognition(user_input):
    door_to_door_sales_credential_phrases = [
        "I'm working for"
        "I'm here representing",
        "I'm from the company",
        "I'm working on behalf of",
        "I'm a sales representative for",
        "I'm with the door-to-door sales team at",
        "I'm bringing you an offer from",
        "I'm visiting homes today on behalf of",
        "I'm part of the door-to-door sales crew for",
        "I'm here on behalf of the",
        "I'm a door-to-door sales agent for"
    ] 

    # Compare user_input with phrases and find the best match
    matcher = difflib.get_close_matches(user_input, door_to_door_sales_credential_phrases, n=1, cutoff=0.5)
    
    if matcher:
        return matcher[0]
    else:
        return "No matching phrase found."

# Example usage:
# user_input = input("Enter your statement: ")
# recognition_result = word_recognition(user_input)
# print("Recognition Result:", recognition_result)

def display_json_data(request):
    # Create the conversation_data directory if it doesn't exist
    conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
    if not os.path.exists(conversation_data_dir):
        os.makedirs(conversation_data_dir)
    
    # Construct the file path for the conversation log JSON file
    file_name = 'conversation_log.json'
    file_path = os.path.join(conversation_data_dir, file_name)
    # Read the JSON file and load the data
    with open(file_path) as f:
        data = json.load(f)

    # Separate user and AI model messages
    user_messages = [item["message"] for item in data if item["role"] == "user"]
    ai_model_messages = [item["message"] for item in data if item["role"] == "ai_model"]

    # Combine user and AI model messages into pairs
    messages = list(zip(user_messages, ai_model_messages))

    # Close the file
    f.close()

    # Pass the messages list to the template
    return render(request, 'pages/display_json.html', {'messages': messages})


def filter_user_messages(request):
    # Create the conversation_data directory if it doesn't exist
    conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
    if not os.path.exists(conversation_data_dir):
        os.makedirs(conversation_data_dir)
    
    # Construct the file path for the conversation log JSON file
    file_name = 'conversation_log.json'
    file_path = os.path.join(conversation_data_dir, file_name)
    
    # Check if the file exists to avoid FileNotFoundError
    if not os.path.exists(file_path):
        # Handle the case where the file does not exist
        print("The file does not exist.")
        return render(request, 'pages/error.html', {'error': 'The conversation log file does not exist.'})
    
    try:
        # Attempt to load JSON data from file into a pandas DataFrame
        df = pd.read_json(file_path, lines=True)  # Use lines=True if the file is newline-delimited JSON
    except ValueError:
        # If pd.read_json fails, fall back to manual loading and parsing
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)  # For standard JSON; for newline-delimited, use json.loads(file.read())
            except json.JSONDecodeError:
                # Handle JSON decoding error
                return render(request, 'pages/error.html', {'error': 'Invalid JSON format in the file.'})
        df = pd.DataFrame(data)
    
    # Filter rows where 'role' is 'user'
    user_df = df[df['role'] == 'user']
    
    # Display only the user data
    return render(request, 'pages/user_messages.html', {'messages': user_df})


# # display_json_data WORKS!!!
# def display_json_data(request):
#      # Create the conversation_data directory if it doesn't exist
#     conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
#     if not os.path.exists(conversation_data_dir):
#         os.makedirs(conversation_data_dir)
    
#     # Construct the file path for the conversation log JSON file
#     file_name = 'conversation_log.json'
#     file_path = os.path.join(conversation_data_dir, file_name)
#     # Read the JSON file and load the data
#     with open(file_path) as f:
#         data = json.load(f)
    
#     # Convert the data to a pandas DataFrame
#     df = pd.DataFrame(data)
#     # print(df)
#     f.close()
#     # Convert the DataFrame to HTML
#     html_table = df.to_html()
#     # Pass the DataFrame to the template
#     # return render(request, 'pages/display_json.html', {'json_data': df.to_html()})
#     return render(request, 'pages/display_json.html', {'html_table': html_table})


def search_keywords(keywords):
    # Create the conversation_data directory if it doesn't exist
    conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
    if not os.path.exists(conversation_data_dir):
        print("Conversation data directory doesn't exist.")
        return []

    # Construct the file path for the conversation log JSON file
    file_name = 'conversation_log.json'
    file_path = os.path.join(conversation_data_dir, file_name)

    if not os.path.exists(file_path):
        print("Conversation log file doesn't exist.")
        return []

    # Load data from the JSON file
    with open(file_path, mode='r') as file:
        data = json.load(file)

    # Search for keywords in the log entries
    matching_messages = []
    for entry in data:
        message = entry.get("message", "")
        if any(keyword.lower() in message.lower() for keyword in keywords):
            matching_messages.append(entry)

    return matching_messages


# THIS WORKS
# def log_conversation(user_input):
#     # Create the conversation_data directory if it doesn't exist
#     conversation_data_dir = os.path.join(settings.BASE_DIR, 'da_web', 'conversation_data')
#     if not os.path.exists(conversation_data_dir):
#         os.makedirs(conversation_data_dir)

#     # Construct the file path for the conversation log JSON file
#     file_name = 'conversation_log.json'
#     file_path = os.path.join(conversation_data_dir, file_name)

#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Create a new entry for the user's input
#     log_entry = {"timestamp": timestamp, "role": "user", "message": user_input}

#     # Load existing data from the file or initialize as an empty list
#     if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
#         with open(file_path, mode='r') as file:
#             data = json.load(file)
#     else:
#         data = []

#     # Append the new log entry to the data
#     data.append(log_entry)

#     # Write the updated data back to the file
#     with open(file_path, mode='w') as file:
#         json.dump(data, file, indent=4)