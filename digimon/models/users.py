from sqlmodel import SQLModel, Field, Relationship
import bcrypt
from typing import Optional, List
import datetime

class BaseUser(SQLModel):
    email: str
    username: str
    first_name: str
    last_name: str

class User(BaseUser):
    id: int
    last_login_date: Optional[datetime.datetime] = None
    register_date: Optional[datetime.datetime] = None

class UserCreate(BaseUser):
    password: str

class DBUser(BaseUser, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    register_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    last_login_date: Optional[datetime.datetime] = None
    
    

    async def set_password(self, plain_password: str):
        self.password = await self.get_encrypted_password(plain_password)

    async def get_encrypted_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))
