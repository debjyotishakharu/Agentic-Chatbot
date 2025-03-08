import tkinter as tk
from tkinter import scrolledtext
import threading
from agenticchatbotlocal import *

def send_message():
    user_input = user_entry.get()
    if user_input.strip():
        chat_area.insert(tk.END, f"You: {user_input}\n", "user")
        user_entry.delete(0, tk.END)
        
        response = agenticchatbot(user_input, threadid="12345")
        chat_area.insert(tk.END, f"Jay: {response}\n", "bot")
        chat_area.yview(tk.END)
        # speak_response(response)

def voice_input():
    user_input = recognize_speech()
    if user_input:
        user_entry.delete(0, tk.END)
        user_entry.insert(tk.END, user_input)
        send_message()

def process_input(event=None):
    send_message()

# Create UI
root = tk.Tk()
root.title("Jay - AI Assistant")
root.geometry("500x600")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_area.pack(pady=10)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")

user_entry = tk.Entry(root, font=("Arial", 12), width=40)
user_entry.pack(pady=5)
user_entry.bind("<Return>", process_input)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

voice_button = tk.Button(root, text="🎙️ Speak", command=lambda: threading.Thread(target=voice_input).start())
voice_button.pack(pady=5)

root.mainloop()