"""Tests for tool endpoints."""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from ..app import app
from ..tools.search_tool import GoogleSearchTool
from ..tools.code_executor import CodeExecutor

client = TestClient(app)

class TestSearchTool:
    """Test Google Search tool."""
    
    @pytest.fixture
    def search_tool(self):
        return GoogleSearchTool()
    
    @pytest.mark.asyncio
    async def test_search_success(self, search_tool):
        """Test successful search."""
        result = await search_tool.search("python developer jobs")
        
        assert result["status"] == "success"
        assert "query" in result
        assert "results" in result
        assert len(result["results"]) > 0
        assert result["total_results"] > 0
    
    @pytest.mark.asyncio
    async def test_search_mock_fallback(self, search_tool):
        """Test mock search fallback."""
        result = await search_tool.search("software engineer jobs")
        
        assert result["status"] == "success"
        assert result["query"] == "software engineer jobs"
        assert len(result["results"]) >= 3
        
        # Check result structure
        for res in result["results"]:
            assert "title" in res
            assert "link" in res
            assert "snippet" in res
            assert "position" in res

class TestCodeExecutor:
    """Test Python code executor."""
    
    @pytest.fixture
    def code_executor(self):
        return CodeExecutor()
    
    @pytest.mark.asyncio
    async def test_simple_code_execution(self, code_executor):
        """Test simple code execution."""
        code = "print('Hello World')\nresult = 2 + 2\nprint(f'Result: {result}')"
        
        result = await code_executor.execute(code)
        
        assert result["status"] == "success"
        assert "Hello World" in result["output"]
        assert "Result: 4" in result["output"]
        assert result["execution_time"] > 0
    
    @pytest.mark.asyncio
    async def test_code_with_error(self, code_executor):
        """Test code execution with error."""
        code = "print('Start')\nundefined_variable\nprint('End')"
        
        result = await code_executor.execute(code)
        
        assert result["status"] == "success"  # Execution completes but with error
        assert "Start" in result["output"]
        assert "NameError" in result["error"]
    
    @pytest.mark.asyncio
    async def test_unsafe_code_blocked(self, code_executor):
        """Test that unsafe code is blocked."""
        unsafe_codes = [
            "import os",
            "exec('print(1)')",
            "eval('2+2')",
            "__import__('os')"
        ]
        
        for code in unsafe_codes:
            result = await code_executor.execute(code)
            assert result["status"] == "error"
            assert "not allowed" in result["error"]
    
    @pytest.mark.asyncio
    async def test_syntax_error(self, code_executor):
        """Test syntax error handling."""
        code = "print('unclosed string"
        
        result = await code_executor.execute(code)
        
        assert result["status"] == "error"
        assert "Syntax error" in result["error"]
    
    def test_get_example_code(self, code_executor):
        """Test example code generation."""
        examples = ["python_basics", "data_structures", "algorithms"]
        
        for topic in examples:
            code = code_executor.get_example_code(topic)
            assert isinstance(code, str)
            assert len(code) > 0
            assert "print" in code

class TestToolEndpoints:
    """Test tool API endpoints."""
    
    def setup_method(self):
        """Setup test client with auth."""
        # Mock authentication
        self.mock_token = "test_token"
        self.headers = {"Authorization": f"Bearer {self.mock_token}"}
    
    @patch('api.tool_routes.get_current_user')
    def test_search_endpoint(self, mock_auth):
        """Test search endpoint."""
        mock_auth.return_value = "test_user"
        
        payload = {\n            \"query\": \"python developer jobs\",\n            \"num_results\": 3\n        }\n        \n        response = client.post(\n            \"/api/v1/tools/search\",\n            json=payload,\n            headers=self.headers\n        )\n        \n        assert response.status_code == 200\n        data = response.json()\n        assert data[\"status\"] == \"success\"\n        assert \"query\" in data\n        assert \"results\" in data\n        assert \"execution_time\" in data\n    \n    @patch('api.tool_routes.get_current_user')\n    def test_code_execution_endpoint(self, mock_auth):\n        \"\"\"Test code execution endpoint.\"\"\"\n        mock_auth.return_value = \"test_user\"\n        \n        payload = {\n            \"code\": \"print('Hello from test')\\nresult = 5 * 5\\nprint(f'5 * 5 = {result}')\",\n            \"language\": \"python\"\n        }\n        \n        response = client.post(\n            \"/api/v1/tools/execute\",\n            json=payload,\n            headers=self.headers\n        )\n        \n        assert response.status_code == 200\n        data = response.json()\n        assert data[\"status\"] == \"success\"\n        assert \"Hello from test\" in data[\"output\"]\n        assert \"5 * 5 = 25\" in data[\"output\"]\n        assert \"execution_time\" in data\n    \n    @patch('api.tool_routes.get_current_user')\n    def test_unsafe_code_endpoint(self, mock_auth):\n        \"\"\"Test unsafe code rejection.\"\"\"\n        mock_auth.return_value = \"test_user\"\n        \n        payload = {\n            \"code\": \"import os\\nos.system('ls')\",\n            \"language\": \"python\"\n        }\n        \n        response = client.post(\n            \"/api/v1/tools/execute\",\n            json=payload,\n            headers=self.headers\n        )\n        \n        assert response.status_code == 200\n        data = response.json()\n        assert data[\"status\"] == \"error\"\n        assert \"not allowed\" in data[\"error\"]\n    \n    def test_search_health_endpoint(self):\n        \"\"\"Test search tool health endpoint.\"\"\"\n        response = client.get(\"/api/v1/tools/search/health\")\n        \n        assert response.status_code == 200\n        data = response.json()\n        assert data[\"status\"] == \"healthy\"\n        assert data[\"tool\"] == \"google_search\"\n    \n    def test_executor_health_endpoint(self):\n        \"\"\"Test code executor health endpoint.\"\"\"\n        response = client.get(\"/api/v1/tools/execute/health\")\n        \n        assert response.status_code == 200\n        data = response.json()\n        assert data[\"status\"] == \"healthy\"\n        assert data[\"tool\"] == \"python_executor\"\n    \n    def test_unauthorized_access(self):\n        \"\"\"Test unauthorized access to tool endpoints.\"\"\"\n        payload = {\"query\": \"test\"}\n        \n        response = client.post(\"/api/v1/tools/search\", json=payload)\n        assert response.status_code == 403  # Unauthorized\n        \n        payload = {\"code\": \"print('test')\"}\n        response = client.post(\"/api/v1/tools/execute\", json=payload)\n        assert response.status_code == 403  # Unauthorized\n\nclass TestToolIntegration:\n    \"\"\"Test tool integration with agents.\"\"\"\n    \n    @pytest.mark.asyncio\n    async def test_search_tool_integration(self):\n        \"\"\"Test search tool integration with career agent.\"\"\"\n        search_tool = GoogleSearchTool()\n        \n        # Test job search for career agent\n        result = await search_tool.search(\"software engineer remote jobs 2024\")\n        \n        assert result[\"status\"] == \"success\"\n        assert len(result[\"results\"]) > 0\n        \n        # Verify result format for agent consumption\n        for res in result[\"results\"]:\n            assert all(key in res for key in [\"title\", \"link\", \"snippet\"])\n    \n    @pytest.mark.asyncio\n    async def test_code_executor_integration(self):\n        \"\"\"Test code executor integration with learning agent.\"\"\"\n        executor = CodeExecutor()\n        \n        # Test example code execution for learning agent\n        example_code = executor.get_example_code(\"python_basics\")\n        result = await executor.execute(example_code)\n        \n        assert result[\"status\"] == \"success\"\n        assert len(result[\"output\"]) > 0\n        assert result[\"execution_time\"] > 0\n    \n    @pytest.mark.asyncio\n    async def test_parallel_execution_performance(self):\n        \"\"\"Test parallel execution of tools.\"\"\"\n        search_tool = GoogleSearchTool()\n        executor = CodeExecutor()\n        \n        # Run tools in parallel\n        search_task = search_tool.search(\"python jobs\")\n        code_task = executor.execute(\"print('Parallel execution test')\")\n        \n        search_result, code_result = await asyncio.gather(search_task, code_task)\n        \n        assert search_result[\"status\"] == \"success\"\n        assert code_result[\"status\"] == \"success\"\n        assert \"Parallel execution test\" in code_result[\"output\"]