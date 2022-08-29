# database.py

import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college_bazaar
