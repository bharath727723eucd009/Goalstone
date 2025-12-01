"""Test cases for messaging and workflow systems."""
import pytest
import asyncio
from ..tools.messaging import MessageBroker, AgentCommunicator
from ..tools.workflow_engine import WorkflowEngine, Workflow, WorkflowTask

@pytest.mark.asyncio
async def test_message_broker():
    """Test message broker functionality."""
    broker = MessageBroker()
    await broker.start()
    
    received_messages = []
    
    def message_handler(message_envelope):
        received_messages.append(message_envelope)
    
    # Subscribe to topic
    broker.subscribe("test_topic", message_handler)
    
    # Publish message
    await broker.publish("test_topic", {"data": "test"}, "sender_1")
    
    # Wait for message processing
    await asyncio.sleep(0.1)
    
    assert len(received_messages) == 1
    assert received_messages[0]["message"]["data"] == "test"
    assert received_messages[0]["sender_id"] == "sender_1"
    
    await broker.stop()

@pytest.mark.asyncio
async def test_agent_communicator():
    """Test agent communication."""
    broker = MessageBroker()
    await broker.start()
    
    comm1 = AgentCommunicator("agent_1", broker)
    comm2 = AgentCommunicator("agent_2", broker)
    
    received_messages = []
    
    def message_handler(message_envelope):
        received_messages.append(message_envelope)
    
    comm2.subscribe_to_messages(message_handler)
    
    # Send message
    await comm1.send_message("agent_2", {"type": "greeting", "data": "hello"})
    
    # Wait for message processing
    await asyncio.sleep(0.1)
    
    assert len(received_messages) == 1
    assert received_messages[0]["message"]["type"] == "greeting"
    
    await broker.stop()

@pytest.mark.asyncio
async def test_workflow_engine():
    """Test workflow engine with mock coordinator."""
    
    class MockAgent:
        async def process_task(self, task):
            return {"status": "success", "data": f"processed_{task['type']}"}
    
    class MockCoordinator:
        def __init__(self):
            self.agents = {
                "test_agent": MockAgent()
            }
        
        async def process_task(self, task):
            return {"status": "success", "data": "coordinator_processed"}
    
    coordinator = MockCoordinator()
    engine = WorkflowEngine(coordinator)
    
    # Create simple workflow
    tasks = [
        WorkflowTask("task_1", "test_agent", {"type": "test_task_1"}),
        WorkflowTask("task_2", "test_agent", {"type": "test_task_2"}, dependencies=["task_1"])
    ]
    
    workflow = Workflow("test_workflow", "Test Workflow", tasks)
    
    # Execute workflow
    result = await engine.execute_workflow(workflow)
    
    assert result["status"] == "completed"
    assert "task_1" in result["results"]
    assert "task_2" in result["results"]
    assert result["results"]["task_1"]["status"] == "success"