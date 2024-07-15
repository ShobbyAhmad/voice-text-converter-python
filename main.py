import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import speech_recognition as sr
import pygame
from io import BytesIO
from googletrans import Translator

class BhashaTranslatorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Bhasha Translator")
        self.window.geometry("500x400")
        self.window.configure(bg="#F5F5F5")

        self.translator = Translator()

        self.create_widgets()

        # Initialize Pygame mixer
        pygame.mixer.init()

    def create_widgets(self):
        input_label = tk.Label(self.window, text="Enter Text:", font=('Helvetica', 14, 'bold'), bg="#F5F5F5", fg="#333333")
        input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.input_text_entry = tk.Entry(self.window, width=40, font=('Arial', 12))
        self.input_text_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        language_label = tk.Label(self.window, text="Select Language:", font=('Helvetica', 14, 'bold'), bg="#F5F5F5", fg="#333333")
        language_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.language_combobox = ttk.Combobox(self.window, values=['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Marathi', 'Bengali', 'Gujarati','Urdu',], font=('Arial', 12))
        self.language_combobox.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        text_to_speech_button = tk.Button(self.window, text="Text to Speech", command=self.text_to_speech, font=('Helvetica', 14, 'bold'), bg='#4CAF50', fg='white', relief=tk.GROOVE)
        text_to_speech_button.grid(row=2, column=0, pady=20, padx=(10, 5), sticky="we")

        speech_to_text_button = tk.Button(self.window, text="Speech to Text", command=self.speech_to_text, font=('Helvetica', 14, 'bold'), bg='#FF9800', fg='white', relief=tk.GROOVE)
        speech_to_text_button.grid(row=2, column=1, pady=20, padx=(5, 10), sticky="we")

        self.result_label = tk.Label(self.window, text="", wraplength=400, justify='left', anchor='w', font=('Arial', 12), bg="#F5F5F5", fg="#333333")
        self.result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def text_to_speech(self):
        input_text = self.input_text_entry.get()
        language = self.get_language_code()

        if not input_text or not language:
            self.result_label.config(text="Please enter text and select a language.")
            return

        translation = self.translate_text(input_text, language)

        tts = gTTS(text=translation, lang=language, slow=False)

        # Play the generated audio using Pygame mixer
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()

    def speech_to_text(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something:")
            try:
                audio = recognizer.listen(source, timeout=5)  # Timeout set to 5 seconds
                text = recognizer.recognize_google(audio)
                language = self.get_language_code()
                translation = self.translate_text(text, language)
                self.result_label.config(text=f"Recognized Text: {text}\nTranslated Text: {translation}")
            except sr.UnknownValueError:
                self.result_label.config(text="Could not understand audio")
            except sr.RequestError as e:
                self.result_label.config(text=f"Error requesting results from Google Speech Recognition service: {e}")
            except sr.WaitTimeoutError:
                self.result_label.config(text="Speech recognition timed out. Please try again.")

    def translate_text(self, text, language):
        translation = self.translator.translate(text, dest=language)
        return translation.text

    def get_language_code(self):
        language_mapping = {'English': 'en', 'Hindi': 'hi', 'Tamil': 'ta', 'Telugu': 'te', 'Kannada': 'kn', 'Marathi': 'mr', 'Bengali': 'bn', 'Gujarati': 'gu','Urdu': 'ur',}
        selected_language = self.language_combobox.get()
        return language_mapping.get(selected_language, '')

    def run(self):
        self.center_window()
        self.window.mainloop()

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 500
        window_height = 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

if __name__ == "__main__":
    app = BhashaTranslatorApp()
    app.run()
