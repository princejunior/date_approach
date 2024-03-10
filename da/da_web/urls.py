from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.simulate_conversation, name='simulate_conversation'),
    path('simulate-conversation/', views.simulate_conversation, name='simulate_conversation'),
    path('load_conversations/', views.load_conversations, name='load_conversations'),
    path('feedback/', views.simulate_conversation, name='simulate_conversation'),
    path('search-keywords', views.search_keywords, name='search-keywords'),
    path('speech_to_text', views.convert_speech_to_text, name='speech_to_text'),
    path('display', views. display_json_data, name=' display_json_data'),
    
   
]