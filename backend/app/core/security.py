from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import hashlib

class EncryptionService:
    """Service for encrypting and decrypting sensitive financial data"""
    
    def __init__(self):
        # Generate a proper Fernet key from the settings key
        key = hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(key))
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not data:
            return data
        encrypted = self.fernet.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return encrypted_data
        decrypted = self.fernet.decrypt(encrypted_data.encode())
        return decrypted.decode()

# Global encryption service instance
encryption_service = EncryptionService()
