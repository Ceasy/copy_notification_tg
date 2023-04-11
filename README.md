# Copy Notification Telegram

This Python script copies files and folders to a specified destination and sends a notification to a Telegram chat when a file or folder is successfully copied. It features a simple graphical interface that allows users to select files and folders for copying, choose a destination, and start the copying process.

## Features

- Copy multiple files and folders
- Send notifications to Telegram on successful copying
- Progress bar for tracking the progress of individual file copying
- Cancel button to stop the copying process

## Installation

### Prerequisites

- Python 3.6 or higher
- `tkinter` for the graphical interface
- `aiogram` for interacting with the Telegram API
- `cryptography` for encrypting sensitive data (optional, but recommended)

### Steps

1. Clone this repository or download the source code as a ZIP archive and extract it.

2. Install the required Python packages:

```bash
pip install aiogram cryptography 
```
3. Replace the following variables in the main script (main.py) with your encrypted bot token, chat ID, and encryption key:

```bash
key = b'your_key_here'
encrypted_bot_token = b'your_encrypted_bot_token_here'
encrypted_chat_id = b'your_encrypted_chat_id_here'
```

Follow the instructions in the "Encrypting sensitive data" section below to obtain these values.

4. Run the script:

```bash
python main.py
```

5. Use the graphical interface to select files and folders, set a destination, and start the copying process.


## Encrypting sensitive data

To keep your bot token and chat ID secure, you can use the cryptography library to encrypt them before including them in your script. See the instructions provided in the previous answer for more information.

## Converting the script to an executable

If you want to convert your script into an executable, you can use tools like `PyInstaller` or `cx_Freeze`. Keep in mind that the encrypted sensitive data will be included in the executable, which could be reverse-engineered by a determined attacker. While encrypting the data adds a layer of security, it is not foolproof.
- Чтобы пофиксить ошибку `pkg_resources.DistributionNotFound: The 'magic_filter' distribution was not found and is required by the application` при конвертации в 'exe' с помошью 'Auto-py-to-exe' необходимо:
1. В 'Advanced' в поле '--copy-metadata' указать "magic_filter".
