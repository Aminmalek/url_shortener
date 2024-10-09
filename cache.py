import redis
import os

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = os.getenv('REDIS_PORT', 6379)

cache = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
