import os
from redis import Redis


REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)