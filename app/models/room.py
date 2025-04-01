from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from database import Base
from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    #mode = Column(String)
    password = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    current_players = Column(Integer)
    max_players = Column(Integer, default=4)
    status = Column(Enum("waiting", "ready", "in_game", name="room_status"), default="waiting")
    creator = relationship("User", foreign_keys=[creator_id])
    users = relationship("User",
                         back_populates="room",
                         foreign_keys="User.room_id",  # 指定反向关系外键
                         cascade="all, delete-orphan")
    countdown_timer = Column(Integer)  # 新增倒计时字段

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            #"mode": self.mode,
            "password": self.password,
            "creator_id": self.creator_id,
            "current_players": self.current_players,
            "max_players": self.max_players,
            "status": self.status
        }