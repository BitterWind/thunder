from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    maxScore = Column(Integer, default=0)
    room_id = Column(Integer, ForeignKey('rooms.id'))  # 新增关联字段
    # 添加关系
    room = relationship("Room", back_populates="users", foreign_keys=[room_id])
    ready_status = Column(Boolean, default=False)  # 新增准备状态字段

    position = Column(JSON)  # 添加 position 字段
    keyMouse = Column(JSON)  # 添加 keyMouse 字段
    mouse = Column(JSON)  # 添加 mouse 字段

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "maxScore": self.maxScore
        }