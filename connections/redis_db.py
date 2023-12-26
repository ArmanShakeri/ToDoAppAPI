import redis

class RedisDB():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisDB, cls).__new__(cls)
            # Initialize the Redis connection here
            cls._instance.redis_connection = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        return cls._instance