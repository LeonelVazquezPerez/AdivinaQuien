#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

def traducirAudio():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # write audio to a RAW file
    with open("microaudio.raw", "wb") as f:
        f.write(audio.get_raw_data())

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + result )
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Irreconocible"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

