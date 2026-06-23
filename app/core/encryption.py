from cryptography.fernet import Fernet
import os
from app.core.config import settings

# In a real production app, this key would be stored in an environment variable or a secret manager
# For the sake of this implementation, we will manage it via a simple file or env var.
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "SGVsbG9Xb3JsZFNlY3VyaXR5S2V5MTIzNDU2Nzg5MA==") # Example Base64 key
# The key must be 32 url-safe base64-encoded bytes.
# If the env var is not set, we use a fallback for dev purposes.
# In practice, use: Fernet.generate_key()

class DataEncryption:
    def __init__(self):
        try:
            self.cipher = Fernet(ENCRYPTION_KEY.encode())
        except Exception:
            # Fallback to a fixed key if the provided one is invalid for development
            fallback_key = Fernet.generate_key()
            self.cipher = Fernet(fallback_key)

    def encrypt(self, data: str) -> str:
        if data is None:
            return None
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        if encrypted_data is None:
            return None
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return "Decryption Error"

encryption_service = DataEncryption()
