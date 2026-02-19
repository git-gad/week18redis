import redis
import json
import os


FILE_PATH = 'border_alerts.json'


r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, decode_responses=True)


with open(FILE_PATH, 'r') as f:
    data = json.load(f)
    
    for alarm in data:
        if (alarm['weapons_count'] > 0) or (alarm['distance_from_fence_m'] <= 50) or (alarm['people_count'] >= 8) or (alarm['vehicle_type'] == 'truck'):
            alarm['priority'] = 'URGENT'
            r.lpush('urgent_queue', json.dumps(alarm))

        elif (alarm['distance_from_fence_m'] <= 150) and (alarm['people_count'] >= 4):
            alarm['priority'] = 'URGENT'
            r.lpush('urgent_queue', json.dumps(alarm))

        elif (alarm['vehicle_type'] == 'jeep') and (alarm['people_count'] >= 3):
            alarm['priority'] = 'URGENT'
            r.lpush('urgent_queue', json.dumps(alarm))

        else:
            alarm['priority'] = 'NORMAL'
            r.lpush('normal_queue', json.dumps(alarm))

    
        
        