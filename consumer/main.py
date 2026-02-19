import redis
import json
import os
from datetime import datetime, timezone
from mongo_connection import get_db


mongodb = get_db()
collection = mongodb['alarms']

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, decode_responses=True)


while True:
    try:
        queue, data = r.brpop(['urgent_queue', 'normal_queue'], timeout=10)

        if data:
            alarm = json.loads(data)
            alarm['time_insertion'] = datetime.now(timezone.utc)
            result = collection.insert_one(alarm)
    except Exception as e:
        print(f'some error: {e}')


    
    
    

  