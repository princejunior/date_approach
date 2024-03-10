import speech_recognition as sr
import pyttsx3
# Init the recognizer
r = sr.Recognizer()

def speech_to_text(): 
    # loop in case of errors
    while True:
        try: 
            # use the microphone as source for input
            with sr.Microphone() as source2:
                # Prepare recognizer to receive input 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # listens for the user's input
                audio2 = r.listen(source2)
                # using google to recognize audio
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")  

def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()

# while True:
#     text = speech_to_text()
#     output_text(text)
#     print("Wrote Text")

# run tail -f output.txt along with python speech_to_text.py