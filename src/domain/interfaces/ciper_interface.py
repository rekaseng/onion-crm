from abc import ABC, abstractmethod


class CipherInterface(ABC):
    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, encrypted_message: str) -> str:
        pass