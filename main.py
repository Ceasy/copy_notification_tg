import os
import shutil
# import configparser
import tkinter as tk
from tkinter import ttk, filedialog
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from threading import Thread
from cryptography.fernet import Fernet
import asyncio


async def send_telegram_message(bot, chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)


def run_asyncio_coroutine(coroutine):
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coroutine)
        loop.close()

    thread = Thread(target=run)
    thread.start()


def copy_files(src, dest_folder, progress_var, progress_bar, cancel_var):
    if os.path.isdir(src):
        dest = os.path.join(dest_folder, os.path.basename(src))
        shutil.copytree(src, dest)
    else:
        dest = os.path.join(dest_folder, os.path.basename(src))
        total_size = os.path.getsize(src)
        copied_bytes = 0

        with open(src, "rb") as src_file:
            with open(dest, "wb") as dest_file:
                buf = src_file.read(1024 * 1024)
                while buf and not cancel_var.get():
                    dest_file.write(buf)
                    copied_bytes += len(buf)
                    progress_var.set((copied_bytes / total_size) * 100)
                    progress_bar.update_idletasks()
                    buf = src_file.read(1024 * 1024)


async def copy_and_notify(src, dest_folder, progress_var, bot, chat_id, progress_bar, cancel_var):
    copy_files(src, dest_folder, progress_var, progress_bar, cancel_var)
    await send_telegram_message(bot, chat_id, f"Successfully copied: {src}")


async def start_copy(entries, bot, chat_id, progress_var, cancel_var, start_button, cancel_button, progress_bar, file_info_var):
    src_paths = entries[0].get().split(',')
    dest_folder = entries[1].get()

    if src_paths and dest_folder:
        progress_var.set(0)
        progress_bar.config(maximum=100)
        start_button.config(state=tk.DISABLED)
        cancel_button.config(state=tk.NORMAL)

        for src in src_paths:
            if not cancel_var.get():
                file_info_var.set(f"Copying {src_paths.index(src) + 1} of {len(src_paths)}")
                await copy_and_notify(src, dest_folder, progress_var, bot, chat_id, progress_bar, cancel_var)

        cancel_var.set(0)
        start_button.config(state=tk.NORMAL)
        cancel_button.config(state=tk.DISABLED)
    else:
        print("Both source and destination fields must be filled.")


def create_form(root, progress_var, cancel_var, bot, chat_id):
    fields = ['Source Files/Folders', 'Destination Folder']
    entries = []

    for field in fields:
        row = ttk.Frame(root)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label = ttk.Label(row, text=field, anchor=tk.W)
        label.pack(side=tk.LEFT)
        entry = ttk.Entry(row)
        entry.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        entries.append(entry)

        if field == 'Source Files/Folders':
            button = ttk.Button(row, text="Select Files", command=lambda entry=entry: select_files(entry))
            button.pack(side=tk.RIGHT)
        elif field == 'Destination Folder':
            button = ttk.Button(row, text="Browse", command=lambda entry=entry: select_directory(entry))
            button.pack(side=tk.RIGHT)

    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, mode="determinate")
    progress_bar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    file_info_var = tk.StringVar()
    file_info_label = ttk.Label(root, textvariable=file_info_var)
    file_info_label.pack(side=tk.TOP, padx=5, pady=5)

    buttons = ttk.Frame(root)
    buttons.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    start_button = ttk.Button(buttons, text="Start", command=lambda: run_asyncio_coroutine(
        on_start_click(entries, bot, chat_id, progress_var, cancel_var, start_button, cancel_button, progress_bar,
                       file_info_var)))
    start_button.pack(side=tk.LEFT)

    cancel_button = ttk.Button(buttons, text="Cancel", state=tk.DISABLED, command=lambda: cancel_var.set(1))
    cancel_button.pack(side=tk.LEFT)

    return entries, start_button, cancel_button, progress_bar, file_info_var


def select_files(entry):
    file_list = filedialog.askopenfilenames()
    entry.delete(0, tk.END)
    entry.insert(0, ','.join(file_list))


def select_directory(entry):
    folder_name = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_name)


async def on_start_click(entries, bot, chat_id, progress_var, cancel_var, start_button, cancel_button, progress_bar, file_info_var):
    await start_copy(entries, bot, chat_id, progress_var, cancel_var, start_button, cancel_button, progress_bar, file_info_var)



def main():
    # config = configparser.ConfigParser()
    # config.read("config.ini")

    # token_bot = config.get("Telegram", "token_bot")
    # chat_id = int(config.get("Telegram", "chat_id"))

    key = b'your_key_here'
    encrypted_bot_token = b'your_encrypted_bot_token_here'
    encrypted_chat_id = b'your_encrypted_chat_id_here'

    cipher_suite = Fernet(key)
    token_bot = cipher_suite.decrypt(encrypted_bot_token).decode()
    chat_id = int(cipher_suite.decrypt(encrypted_chat_id).decode())

    root = tk.Tk()
    root.title("Copy Notification Telegram")

    progress_var = tk.DoubleVar()
    cancel_var = tk.IntVar()

    bot = Bot(token=token_bot)

    entries, start_button, cancel_button, progress_bar, file_info_var = create_form(root, progress_var, cancel_var, bot,
                                                                                    chat_id)
    root.mainloop()


if __name__ == "__main__":
    main()

