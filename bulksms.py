import requests
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def send_sms(sender: str, msg_content: str, recipients: list, token: str):
    payload = {
        "sender": sender,
        "message": msg_content,
        "recipients": [{"msisdn": str(recipient)} for recipient in recipients],
    }

    try:
        resp = requests.post(
            "https://gatewayapi.com/rest/mtsms",
            json=payload,
            auth=(token, ""),
        )
        resp.raise_for_status()
        result_label.config(text=f"SMS sent successfully to {len(recipients)} recipients.")
        print(resp.json())

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error sending SMS: {e}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def unlock_sender():
    code = code_entry.get()
    # Implement code validation logic here
    if validate_code(code):
        unlock_sender_id()
    else:
        result_label.config(text="Invalid code. Cannot unlock sender ID.")

def validate_code(code):
    # Implement code validation logic here (e.g., check with your server)
    # Return True if the code is valid, otherwise return False
    # You may use requests to communicate with your server
    return code == "your_server_generated_code"

def unlock_sender_id():
    # Implement sender ID unlocking logic here
    # This could involve enabling the ability to set any sender ID for a limited number of SMS
    # You may also update the available sender IDs accordingly
    result_label.config(text="Sender ID unlocked. You can now choose any sender ID.")

def select_sender(event):
    selected_sender = sender_choice.get()
    if selected_sender == "Custom":
        sender_entry.config(state="normal")
    else:
        sender_entry.delete(0, tk.END)
        sender_entry.insert(0, selected_sender)
        sender_entry.config(state="disabled")

def send_button_clicked():
    # Get values from entry widgets
    sender = sender_entry.get()
    message = message_entry.get()
    token = token_entry.get()
    recipients_str = recipients_entry.get().split()
    file_path = file_entry.get()

    # Extract non-empty recipients from entry widget
    recipients = [int(num.strip()) for num in recipients_str if num.strip()]

    # Extract non-empty recipients from file
    if file_path:
        with open(file_path, "r") as file:
            recipients.extend([int(line.strip()) for line in file if line.strip()])

    # Call the send_sms function
    send_sms(sender, message, recipients, token)

# GUI setup
root = tk.Tk()
root.title("SMS ROFFA DEVELOPERS")

# Sender
sender_label = ttk.Label(root, text="Sender:")
sender_label.grid(row=0, column=0, padx=5, pady=5)

# Sender Choice
sender_choices = ["+31653658985 - NL", "+32 482 45 56 42 BE", "+49 211 1234567 DE", "Custom"]
sender_choice = ttk.Combobox(root, values=sender_choices, state="readonly")
sender_choice.set(sender_choices[0])
sender_choice.grid(row=0, column=1, padx=5, pady=5)
sender_choice.bind("<<ComboboxSelected>>", select_sender)

# Custom Sender Entry
sender_entry = ttk.Entry(root)
sender_entry.grid(row=0, column=2, padx=5, pady=5)

# Message
message_label = ttk.Label(root, text="Message:")
message_label.grid(row=1, column=0, padx=5, pady=5)
message_entry = ttk.Entry(root)
message_entry.grid(row=1, column=1, padx=5, pady=5)

# Recipients
recipients_label = ttk.Label(root, text="Recipients:")
recipients_label.grid(row=2, column=0, padx=5, pady=5)
recipients_entry = ttk.Entry(root)
recipients_entry.grid(row=2, column=1, padx=5, pady=5)

# File
file_label = ttk.Label(root, text="File (optional):")
file_label.grid(row=3, column=0, padx=5, pady=5)
file_entry = ttk.Entry(root)
file_entry.grid(row=3, column=1, padx=5, pady=5)
browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=3, column=2, padx=5, pady=5)

# Code Entry
code_label = ttk.Label(root, text="Unlock Code:")
code_label.grid(row=4, column=0, padx=5, pady=5)
code_entry = ttk.Entry(root)
code_entry.grid(row=4, column=1, padx=5, pady=5)

# Unlock Button
unlock_button = ttk.Button(root, text="Unlock Sender ID", command=unlock_sender)
unlock_button.grid(row=4, column=2, padx=5, pady=5)

# Token
token_label = ttk.Label(root, text="GatewayAPI Token:")
token_label.grid(row=5, column=0, padx=5, pady=5)
token_entry = ttk.Entry(root)
token_entry.grid(row=5, column=1, padx=5, pady=5)

# Send Button
send_button = ttk.Button(root, text="Send SMS", command=send_button_clicked)
send_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result Label
result_label = ttk.Label(root, text="")
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
