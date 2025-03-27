from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.room import Room
from database import SessionLocal


async def room_cleanup():
    """房间自动清理任务"""
    db: Session = SessionLocal()
    try:
        # 清理超过1小时未活动的等待中房间
        inactive_time = datetime.now() - timedelta(hours=1)
        expired_rooms = db.query(Room).filter(
            Room.status == "preparing",
            Room.last_activity < inactive_time
        ).all()

        # 清理空房间（超过30分钟的空房间）
        empty_rooms = db.query(Room).filter(
            Room.current_players == 0,
            Room.created_at < datetime.now() - timedelta(minutes=30)
        ).all()

        # 合并要删除的房间
        rooms_to_delete = expired_rooms + empty_rooms

        for room in rooms_to_delete:
            db.delete(room)

        db.commit()
        print(f"已清理 {len(rooms_to_delete)} 个过期房间")

    except Exception as e:
        db.rollback()
        print(f"房间清理失败: {str(e)}")
    finally:
        db.close()