from fastapi import FastAPI, HTTPException, Depends
from mongo_connection import get_db
from redis_connection import redis_client
import json
from bson import ObjectId


CACHE_TTL_SEC = 15
COLLECTION = 'alarms'


app = FastAPI()
  

@app.get('/alarm/{alarm_id}')
async def get_alarm_by_id(alarm_id: str, db=Depends(get_db)):
    cache_key = f'alarm:{alarm_id}'
    cached = redis_client.get(cache_key)
    
    if cached:
        alarm = json.loads(cached)
        return {'alarm': alarm}
    
    collection = db[COLLECTION]
    doc = await collection.find_one({'_id': ObjectId(alarm_id)}, {'_id': 0})
    
    if not doc:
        raise HTTPException(status_code=404, detail='alarm not found')

    try: 
        redis_client.setex(cache_key, CACHE_TTL_SEC, json.dumps(doc, default=str))
    except Exception as e:
        print(f'could not save alarm to cache: {e}')
         
    return {'alarm': doc}


@app.get('/analytics/alerts-by-border-and-priority')
async def get_dangerous_zones(db=Depends(get_db)):
    collection = db[COLLECTION]
    
    pipeline = [
        {
            '$group': {
                '_id': '$border',
                'count': {'$sum': 1}
            }
        },
        {
            '$project': {
                '_id': 0,
                'border': '$_id',
                'count': 1
            }
        }
    ]

    cursor = collection.aggregate(pipeline)
    results = await cursor.to_list()

    return results


@app.get('/analytics/top-urgent-zones')
async def get_top_urgent_zones(db=Depends(get_db)):
    collection = db[COLLECTION]
    
    pipeline = [
        {
            "$match": {
                "priority": "URGENT"
            }
        },
        {
            "$group": {
                "_id": "$zone", 
                "urgent_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "urgent_count": -1
            }
        },
        {
            "$limit": 5
        },
        {
            "$project": {
                "_id": 0,
                "zone": "$_id",
                "urgent_count": 1
            }
        }
    ]

    cursor = collection.aggregate(pipeline)
    results = await cursor.to_list()

    return results


@app.get('/analytics/distance-distribution')
def get_distance_distribution():
    pass


@app.get('/analytics/low-visibility-high-activity')
def get_some_data():
    pass


@app.get('/analytics/hot-zones')
def get_hot_zones():
    pass
