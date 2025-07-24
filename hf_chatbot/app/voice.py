import speech_recognition as sr

def listen_to_voice(wake_word="alexa"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for voice input... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("⚠️ Timeout: No speech detected.")
            return ""

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"🔊 Recognized: {text}")
        if text.startswith(wake_word.lower()):
            command = text[len(wake_word):].strip()
            print(f"✅ Wake word detected. Extracted command: {command}")
            return command
        else:
            print("❌ Wake word not detected.")
            return ""
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Request error from Google Speech Recognition service; {e}")
        return ""
