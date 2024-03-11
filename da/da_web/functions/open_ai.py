from openai import OpenAI
import openai
from django.conf import settings
import json

def chat_with_gpt(prompt):
    """
    Initiates a chat with the GPT-3.5 model using a specified prompt.
    The chat completion simulates a poetic assistant specializing in creative explanations.

    Parameters:
    - prompt (str): The user's input to which the model will respond.

    Returns:
    - The chat model's response as a string.
    """
    # Create the chat completion with specified roles and content
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message

# Main function for running the chat in a loop until user exits
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        
        response = chat_with_gpt(user_input)
        print("Chatbot: ",response)
    
# Function to simulate a conversation with OpenAI's model given a user's input
def open_ai_conversation(user_input):
    """
    Simulates a conversation where the model acts as a judge for grading public speaker's elevator pitches.

    Parameters:
    - user_input (str): The user's input or question to the model.

    Returns:
    - The model's response as a string, providing feedback and suggestions.
    """
    # Set your OpenAI API key
    OpenAI.api_key = settings.OPENAI_API_KEY

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a judge for grading public speaker's elevator pitch. You give them positive and negative feedback. Look for words that need to be changed. give a suggestion on what the user should say."},
            
            # {"role": "system", "content": "You are a homeowner named Emily, who hears a knock at the door. you open up the door and see the person at the door looks like a salesman."},
            {"role": "user", "content": user_input}
        ]
    )
    content = completion
    print(content.choices[0].message.content)
    content = content.choices[0].message.content
    return content


# Get the OpenAI API key from the environment variables
def open_ai_conversation_ex () :
    # openai_api_key works
    # print(settings.OPENAI_API_KEY) 
    
    # Set your OpenAI API key
    OpenAI.api_key = settings.OPENAI_API_KEY

    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )
    print(completion.choices[0].message)

# def generate_response(prompt):
#     try:
#         # Generate response from the GPT-4 model
#         response = openai.Completion.create(
#             engine="text-davinci-003",  # GPT-4 model
#             prompt=prompt,
#             max_tokens=50  # Maximum number of tokens in the response
#         )
        
#         return response.choices[0].text.strip()

#     except Exception as e:
#         print("Error:", e)
#         return None

# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ")
        
#         if user_input.lower() == 'exit':
#             print("Goodbye!")
#             break
        
#         # Generate response from GPT-4
#         response = generate_response(user_input)
        
#         if response:
#             print("AI: ", response)
#         else:
#             print("Failed to generate response.")
