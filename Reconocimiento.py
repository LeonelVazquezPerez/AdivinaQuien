import time

import speech_recognition as sr

def recAudio():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # write audio to a RAW file
    with open("microaudio.wav", "wb") as f:
        f.write(audio.get_wav_data())

    return "microaudio.raw"

def getAudio():
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile("/home/leonelvazquez/Escritorio/APLICACIONESRED/AdivinaQuien/recibido.wav") as source:
        audio = r.record(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + result )
        time.sleep(1)
        return result
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Irreconocible"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
