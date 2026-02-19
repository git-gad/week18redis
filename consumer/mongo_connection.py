import os
from motor.motor_asyncio import AsyncIOMotorClient


def get_db():
    mongo_client = AsyncIOMotorClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
    db = mongo_client['alarms_db']
    return db
