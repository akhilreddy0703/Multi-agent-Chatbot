# src/services/user_service.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.config.settings import settings
from src.models.user import User, UserInDB
from motor.motor_asyncio import AsyncIOMotorClient

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.database_url)
        self.db = self.client.get_database()
        self.users_collection = self.db.get_collection("users")

    async def create_user(self, user: User):
        user_dict = user.dict()
        user_dict["hashed_password"] = self.get_password_hash(user_dict["password"])
        del user_dict["password"]
        await self.users_collection.insert_one(user_dict)
        return user

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return False
        return user

    async def get_user(self, username: str):
        user_dict = await self.users_collection.find_one({"username": username})
        if user_dict:
            return UserInDB(**user_dict)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

user_service = UserService()