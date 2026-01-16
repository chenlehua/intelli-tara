"""
Redis cache service for performance optimization.
"""
import json
from typing import Any, Optional
from datetime import timedelta
import redis.asyncio as redis

from app.core.config import get_settings

settings = get_settings()


class CacheService:
    """Redis cache service for caching API responses and computed data."""
    
    def __init__(self):
        self._client: Optional[redis.Redis] = None
    
    async def get_client(self) -> redis.Redis:
        """Get or create Redis client."""
        if self._client is None:
            self._client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if hasattr(settings, 'REDIS_PASSWORD') and settings.REDIS_PASSWORD else None,
                decode_responses=True,
            )
        return self._client
    
    async def close(self):
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        client = await self.get_client()
        try:
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        expire_timedelta: Optional[timedelta] = None,
    ):
        """Set value in cache."""
        client = await self.get_client()
        try:
            serialized = json.dumps(value, default=str)
            if expire_timedelta:
                expire = int(expire_timedelta.total_seconds())
            if expire:
                await client.setex(key, expire, serialized)
            else:
                await client.set(key, serialized)
        except Exception:
            pass  # Fail silently for cache operations
    
    async def delete(self, key: str):
        """Delete key from cache."""
        client = await self.get_client()
        try:
            await client.delete(key)
        except Exception:
            pass
    
    async def delete_pattern(self, pattern: str):
        """Delete keys matching pattern."""
        client = await self.get_client()
        try:
            cursor = 0
            while True:
                cursor, keys = await client.scan(cursor, match=pattern)
                if keys:
                    await client.delete(*keys)
                if cursor == 0:
                    break
        except Exception:
            pass
    
    # Cache key generators
    @staticmethod
    def project_key(project_id: int) -> str:
        """Generate cache key for project."""
        return f"project:{project_id}"
    
    @staticmethod
    def project_assets_key(project_id: int, page: int = 1) -> str:
        """Generate cache key for project assets."""
        return f"project:{project_id}:assets:page:{page}"
    
    @staticmethod
    def project_threats_key(project_id: int, page: int = 1) -> str:
        """Generate cache key for project threats."""
        return f"project:{project_id}:threats:page:{page}"
    
    @staticmethod
    def project_stats_key() -> str:
        """Generate cache key for project statistics."""
        return "stats:projects"
    
    @staticmethod
    def knowledge_key(category: str) -> str:
        """Generate cache key for knowledge base data."""
        return f"knowledge:{category}"


# Global cache instance
cache_service = CacheService()


# Cache decorator
def cached(
    key_func,
    expire: int = 300,  # 5 minutes default
):
    """Decorator for caching function results."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = key_func(*args, **kwargs)
            
            # Try to get from cache
            cached_value = await cache_service.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await cache_service.set(cache_key, result, expire=expire)
            
            return result
        return wrapper
    return decorator
