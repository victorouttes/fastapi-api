from pwdlib import PasswordHash

class SecurityHandler:
    def __init__(self) -> None:
        self.__context = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.__context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self.__context.verify(password, password_hash)

security_handler = SecurityHandler()
