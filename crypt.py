from cryptography.fernet import Fernet

# Generate a key and use it to create a Fernet object
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt your bot token and chat ID
bot_token = "your_bot_token_here"
chat_id = "your_chat_id_here"

encrypted_bot_token = cipher_suite.encrypt(bot_token.encode())
encrypted_chat_id = cipher_suite.encrypt(chat_id.encode())

print("Key:", key)
print("Encrypted bot token:", encrypted_bot_token)
print("Encrypted chat ID:", encrypted_chat_id)
