from django.http import JsonResponse
from da_web.models import ConversationLog
import json
import os

def solar_recognition_function(user_input):
    # Get the directory path of the JSON files
    json_folder = os.path.join(os.path.dirname(__file__), 'json')

    # Load positive and negative phrases for solar sales
    with open(os.path.join(json_folder, 'positive_phrases.json'), 'r') as file:
        solar_positive_phrases = json.load(file)['solar_sales_phrases']
    with open(os.path.join(json_folder, 'negative_phrases.json'), 'r') as file:
        solar_negative_phrases = json.load(file)['solar_negative_phrases']

    # Check user input against positive and negative phrases for solar sales
    solar_positive_points = sum(1 for phrase in solar_positive_phrases if phrase in user_input.lower())
    solar_negative_points = sum(1 for phrase in solar_negative_phrases if phrase in user_input.lower())

    # Calculate total score for solar sales
    solar_score = solar_positive_points - solar_negative_points

    return solar_score

def pest_control_recognition_function(user_input):
    # Get the directory path of the JSON files
    json_folder = os.path.join(os.path.dirname(__file__), 'json')

    # Load positive and negative phrases for pest control sales
    with open(os.path.join(json_folder, 'positive_phrases.json'), 'r') as file:
        pest_control_positive_phrases = json.load(file)['pest_control_sales_phrases']
    with open(os.path.join(json_folder, 'negative_phrases.json'), 'r') as file:
        pest_control_negative_phrases = json.load(file)['pest_control_negative_phrases']

    # Check user input against positive and negative phrases for pest control sales
    pest_control_positive_points = sum(1 for phrase in pest_control_positive_phrases if phrase in user_input.lower())
    pest_control_negative_points = sum(1 for phrase in pest_control_negative_phrases if phrase in user_input.lower())

    # Calculate total score for pest control sales
    pest_control_score = pest_control_positive_points - pest_control_negative_points

    return pest_control_score



def evaluate_user_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        # Call recognition function
        score = solar_recognition_function(user_input)

        # Update user's score
        # Example: assuming you have a User model with a score field
        # user = request.user  # Assuming user is authenticated
        # user.score += score
        # user.save()

        # Return score as JSON response
        return JsonResponse({'score': score})

    return JsonResponse({'error': 'Invalid request method'})

def log_conversation(speaker, message):
    ConversationLog.objects.create(speaker=speaker, message=message)

def solar_recognition_function(user_input):
    # Perform recognition based on user input
    # ...
    # Log conversation
    log_conversation("user", user_input)
    # Generate AI response
    # ...

def homeowner_ai(user_input):
    # AI logic as homeowner
    # ...
    # Log conversation
    log_conversation("homeowner", ai_response)
    # Return AI response
    # ...