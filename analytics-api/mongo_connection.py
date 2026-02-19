from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.getenv('MONGO_DB', 'alarms_db')


def get_db():
    mongo_client = AsyncIOMotorClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
    db = mongo_client['alarms_db']
    return db
