from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    maxScore = Column(Integer, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "maxScore": self.maxScore
        }