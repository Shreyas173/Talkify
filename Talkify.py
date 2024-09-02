import tkinter as tk
import pyttsx3
import speech_recognition as sr

def text_to_speech():
    text = text_entry.get("1.0", "end-1c")
    if text:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

def update_timer(seconds_left):
    if seconds_left > 0:
        timer_label.config(text=f"Speak in {seconds_left} seconds...")
        window.after(1000, update_timer, seconds_left - 1)
    else:
        timer_label.config(text="Speak now!")
        window.after(100, start_speech_to_text_process)  # Start recording after an additional 2-second delay

def start_speech_to_text():
    status_label.config(text="Preparing to listen...")
    update_timer(2)  # Start the countdown from 3 seconds

def start_speech_to_text_process():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            status_label.config(text="Recognized!")
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, text)
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio")
        except sr.RequestError:
            status_label.config(text="Speech recognition service error")

# Initialize the GUI window
window = tk.Tk()
window.title("Text to Speech and Speech to Text")

# Center the window
window_width = 600
window_height = 300

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position x, y
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Text entry box
text_entry = tk.Text(window, height=5, width=50)
text_entry.pack(pady=10)

# Text to Speech Button
tts_button = tk.Button(window, text="Convert Text to Speech", command=text_to_speech)
tts_button.pack(pady=5)

# Speech to Text Button
stt_button = tk.Button(window, text="Convert Speech to Text", command=start_speech_to_text)
stt_button.pack(pady=5)

# Status Label
status_label = tk.Label(window, text="")
status_label.pack(pady=10)

# Timer Label
timer_label = tk.Label(window, text="")
timer_label.pack(pady=10)

# Start the GUI loop
window.mainloop()
