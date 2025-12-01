"""MongoDB connection using Motor."""
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings
import structlog

logger = structlog.get_logger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection."""
    mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
    mongodb.database = mongodb.client.ai_life_goals
    logger.info("Connected to MongoDB")

async def close_mongo_connection():
    """Close database connection."""
    mongodb.client.close()
    logger.info("Disconnected from MongoDB")

def get_database():
    """Get database instance."""
    return mongodb.database