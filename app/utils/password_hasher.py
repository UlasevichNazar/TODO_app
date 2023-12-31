from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    @staticmethod
    def verify_password(plain_password, hasher_password):
        return pwd_context.verify(plain_password, hasher_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
