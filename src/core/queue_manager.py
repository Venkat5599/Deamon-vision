"""
Async queue manager for inter-module communication.
Supports both asyncio.Queue and Redis Streams.
"""
import asyncio
from typing import Any, Optional, Dict
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class QueueManager:
    """Manages async queues for pipeline communication."""
    
    def __init__(self, backend: str = "asyncio", redis_url: Optional[str] = None, max_size: int = 100):
        """
        Initialize queue manager.
        
        Args:
            backend: "asyncio" or "redis"
            redis_url: Redis connection URL (required if backend="redis")
            max_size: Maximum queue size
        """
        self.backend = backend
        self.redis_url = redis_url
        self.max_size = max_size
        self.queues: Dict[str, asyncio.Queue] = {}
        self.redis_client = None
        
        if backend == "redis" and redis_url:
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection."""
        try:
            import redis.asyncio as aioredis
            self.redis_client = aioredis.from_url(self.redis_url, decode_responses=True)
            logger.info(f"Redis queue backend initialized: {self.redis_url}")
        except ImportError:
            logger.warning("Redis not available, falling back to asyncio.Queue")
            self.backend = "asyncio"
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.backend = "asyncio"
    
    def create_queue(self, name: str) -> asyncio.Queue:
        """
        Create a new queue.
        
        Args:
            name: Queue name
        
        Returns:
            asyncio.Queue instance
        """
        if name not in self.queues:
            self.queues[name] = asyncio.Queue(maxsize=self.max_size)
            logger.info(f"Created queue: {name} (backend={self.backend})")
        return self.queues[name]
    
    async def put(self, queue_name: str, item: Any, timeout: Optional[float] = None):
        """
        Put item into queue.
        
        Args:
            queue_name: Queue name
            item: Item to put
            timeout: Optional timeout in seconds
        """
        if self.backend == "asyncio":
            queue = self.queues.get(queue_name)
            if queue is None:
                queue = self.create_queue(queue_name)
            
            try:
                if timeout:
                    await asyncio.wait_for(queue.put(item), timeout=timeout)
                else:
                    await queue.put(item)
            except asyncio.TimeoutError:
                logger.warning(f"Queue {queue_name} put timeout")
            except asyncio.QueueFull:
                logger.warning(f"Queue {queue_name} is full, dropping oldest item")
                try:
                    queue.get_nowait()
                    await queue.put(item)
                except:
                    pass
        
        elif self.backend == "redis" and self.redis_client:
            try:
                # Serialize item
                data = json.dumps(item, default=str)
                await self.redis_client.xadd(
                    queue_name,
                    {"data": data},
                    maxlen=self.max_size
                )
            except Exception as e:
                logger.error(f"Redis put error: {e}")
    
    async def get(self, queue_name: str, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Get item from queue.
        
        Args:
            queue_name: Queue name
            timeout: Optional timeout in seconds
        
        Returns:
            Item from queue or None
        """
        if self.backend == "asyncio":
            queue = self.queues.get(queue_name)
            if queue is None:
                return None
            
            try:
                if timeout:
                    return await asyncio.wait_for(queue.get(), timeout=timeout)
                else:
                    return await queue.get()
            except asyncio.TimeoutError:
                return None
        
        elif self.backend == "redis" and self.redis_client:
            try:
                # Read from stream
                messages = await self.redis_client.xread(
                    {queue_name: "0"},
                    count=1,
                    block=int(timeout * 1000) if timeout else 0
                )
                
                if messages:
                    stream_name, message_list = messages[0]
                    if message_list:
                        msg_id, msg_data = message_list[0]
                        data = json.loads(msg_data["data"])
                        # Delete message after reading
                        await self.redis_client.xdel(queue_name, msg_id)
                        return data
                
                return None
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None
    
    async def get_nowait(self, queue_name: str) -> Optional[Any]:
        """
        Get item from queue without waiting.
        
        Args:
            queue_name: Queue name
        
        Returns:
            Item from queue or None
        """
        if self.backend == "asyncio":
            queue = self.queues.get(queue_name)
            if queue is None:
                return None
            
            try:
                return queue.get_nowait()
            except asyncio.QueueEmpty:
                return None
        
        return await self.get(queue_name, timeout=0.001)
    
    def qsize(self, queue_name: str) -> int:
        """
        Get queue size.
        
        Args:
            queue_name: Queue name
        
        Returns:
            Queue size
        """
        if self.backend == "asyncio":
            queue = self.queues.get(queue_name)
            return queue.qsize() if queue else 0
        
        return 0  # Redis stream length requires async call
    
    async def clear(self, queue_name: str):
        """
        Clear all items from queue.
        
        Args:
            queue_name: Queue name
        """
        if self.backend == "asyncio":
            queue = self.queues.get(queue_name)
            if queue:
                while not queue.empty():
                    try:
                        queue.get_nowait()
                    except asyncio.QueueEmpty:
                        break
        
        elif self.backend == "redis" and self.redis_client:
            try:
                await self.redis_client.delete(queue_name)
            except Exception as e:
                logger.error(f"Redis clear error: {e}")
    
    async def close(self):
        """Close all connections."""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis connection closed")
