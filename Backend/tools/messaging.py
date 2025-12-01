"""Asynchronous messaging system for agent communication."""
import asyncio
import json
from typing import Dict, Any, Callable, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class MessageBroker:
    """In-memory message broker for agent communication."""
    
    def __init__(self):
        self.subscribers = {}
        self.message_queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Start the message broker."""
        self.running = True
        asyncio.create_task(self._process_messages())
        logger.info("Message broker started")
    
    async def stop(self):
        """Stop the message broker."""
        self.running = False
        logger.info("Message broker stopped")
    
    async def publish(self, topic: str, message: Dict[str, Any], sender_id: str = None):
        """Publish a message to a topic."""
        message_envelope = {
            "topic": topic,
            "message": message,
            "sender_id": sender_id,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{topic}_{datetime.now().timestamp()}"
        }
        
        await self.message_queue.put(message_envelope)
        logger.info("Message published", topic=topic, sender_id=sender_id)
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic with a callback function."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        
        self.subscribers[topic].append(callback)
        logger.info("Subscribed to topic", topic=topic)
    
    def unsubscribe(self, topic: str, callback: Callable):
        """Unsubscribe from a topic."""
        if topic in self.subscribers:
            self.subscribers[topic].remove(callback)
            logger.info("Unsubscribed from topic", topic=topic)
    
    async def _process_messages(self):
        """Process messages from the queue."""
        while self.running:
            try:
                message_envelope = await asyncio.wait_for(
                    self.message_queue.get(), timeout=1.0
                )
                
                topic = message_envelope["topic"]
                if topic in self.subscribers:
                    for callback in self.subscribers[topic]:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(message_envelope)
                            else:
                                callback(message_envelope)
                        except Exception as e:
                            logger.error("Callback error", topic=topic, error=str(e))
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error("Message processing error", error=str(e))

class AgentCommunicator:
    """Handles communication between agents."""
    
    def __init__(self, agent_id: str, message_broker: MessageBroker):
        self.agent_id = agent_id
        self.broker = message_broker
        self.logger = logger.bind(agent_id=agent_id)
    
    async def send_message(self, target_agent: str, message: Dict[str, Any]):
        """Send a message to another agent."""
        topic = f"agent.{target_agent}"
        await self.broker.publish(topic, message, self.agent_id)
        self.logger.info("Message sent", target=target_agent)
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast a message to all agents."""
        await self.broker.publish("agent.broadcast", message, self.agent_id)
        self.logger.info("Message broadcasted")
    
    def subscribe_to_messages(self, callback: Callable):
        """Subscribe to messages for this agent."""
        topic = f"agent.{self.agent_id}"
        self.broker.subscribe(topic, callback)
        
        # Also subscribe to broadcast messages
        self.broker.subscribe("agent.broadcast", callback)
        
        self.logger.info("Subscribed to agent messages")
    
    async def request_response(self, target_agent: str, request: Dict[str, Any], 
                             timeout: float = 30.0) -> Optional[Dict[str, Any]]:
        """Send a request and wait for a response."""
        request_id = f"req_{datetime.now().timestamp()}"
        request["request_id"] = request_id
        request["response_topic"] = f"response.{self.agent_id}.{request_id}"
        
        response_received = asyncio.Event()
        response_data = {}
        
        def response_handler(message_envelope):
            nonlocal response_data
            response_data = message_envelope["message"]
            response_received.set()
        
        # Subscribe to response topic
        response_topic = request["response_topic"]
        self.broker.subscribe(response_topic, response_handler)
        
        try:
            # Send request
            await self.send_message(target_agent, request)
            
            # Wait for response
            await asyncio.wait_for(response_received.wait(), timeout=timeout)
            return response_data
            
        except asyncio.TimeoutError:
            self.logger.error("Request timeout", target=target_agent, request_id=request_id)
            return None
        finally:
            # Cleanup subscription
            self.broker.unsubscribe(response_topic, response_handler)

# Global message broker instance
message_broker = MessageBroker()