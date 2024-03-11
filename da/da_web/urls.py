from django.urls import path
from . import views

urlpatterns = [
    # Home page route - displays the home page of the application
    path('home/', views.home, name='home'),

    # Default route - simulates a conversation, can be accessed directly via the root URL
    path('', views.simulate_conversation, name='simulate_conversation'),

    # Explicit route for simulating a conversation - mirrors the functionality of the default route
    path('simulate-conversation/', views.simulate_conversation, name='simulate_conversation'),

    # Route for loading and displaying previously saved conversations from a JSON file
    path('load_conversations/', views.load_conversations, name='load_conversations'),

    # Route for submitting feedback - currently named 'simulate_conversation' but might need renaming for clarity
    path('feedback/', views.feedback, name='feedback'),  # Updated the 'name' to match the view function purpose

    # Route for searching keywords within the saved conversations
    path('search-keywords/', views.search_keywords, name='search_keywords'),  # Added trailing slash for consistency

    # Route for converting speech to text, providing an interface for speech-to-text conversion
    path('speech_to_text/', views.convert_speech_to_text, name='speech_to_text'),  # Added trailing slash for consistency

    # Route for displaying JSON data - typically, this would display conversation logs or other JSON-formatted information
    path('display/', views.display_json_data, name='display_json_data'),  # Corrected spacing in the 'name' parameter

    # Route for filtering and displaying user messages from the conversation logs
    path('user_messages/', views.filter_user_messages, name='user_messages'),  # Added trailing slash for consistency
]
