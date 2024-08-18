from sqlmodel import SQLModel
import datetime

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    issued_at: datetime.datetime
    user_id: int
