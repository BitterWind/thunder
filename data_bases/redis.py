import redis

def get_redis():
    """获取 Redis 连接实例"""
    return redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )