import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties (optional)
    engine.setProperty('rate', 200)  # Speed percent (can go over 100)
    engine.setProperty('volume', 1.0)  # Volume 0-1
    
    # Convert text to speech
    engine.say(text)
    
    # Wait for the speech to finish
    engine.runAndWait()
    
    # Print current speaking rate
    rate = engine.getProperty('rate')
    print("Current speaking rate:", rate)
    
    # Saving voice to a file
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

def main():
# if __name__ == "__main__":
    while True:
        input_text = input("Enter the text you want to convert to speech (or 'exit' to quit): ")
        if input_text.lower() == 'exit':
            break
        text_to_speech(input_text)
