import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime


class DBService:
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection("agent_logs")

    @classmethod
    async def log_interaction(cls, prompt, agent_message):
        await cls.collection.insert_one(
            {"role": "user", "content": str(prompt), "timestamp": datetime.utcnow()}
        )
        await cls.collection.insert_one(
            {
                "role": "assistant",
                "content": str(agent_message),
                "timestamp": datetime.utcnow(),
            }
        )

    @classmethod
    async def get_recent_history(cls, limit=5):
        
        cursor = cls.collection.find().sort("timestamp", -1).limit(limit * 2)
        history = []
        async for doc in cursor:
            history.append(
                {"role": doc.get("role", "user"), "content": doc.get("content", "")}
            )
      
        return history[::-1]
