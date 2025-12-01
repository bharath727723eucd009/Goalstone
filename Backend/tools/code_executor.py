"""Safe Python code execution tool for Learning Agent."""
import asyncio
import sys
import io
import contextlib
import ast
import time
from typing import Dict, Any
from ..observability.logger import get_logger

logger = get_logger(__name__)

class CodeExecutor:
    """Safe Python code execution in sandbox."""
    
    def __init__(self):
        self.timeout = 10  # 10 second timeout
        self.max_output_length = 5000
        
        # Allowed modules for safe execution
        self.allowed_modules = {
            'math', 'random', 'datetime', 'json', 'collections',
            'itertools', 'functools', 'operator', 're', 'string'
        }
        
        # Restricted builtins
        self.safe_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
            'getattr', 'hasattr', 'hash', 'hex', 'id', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'map', 'max', 'min',
            'next', 'oct', 'ord', 'pow', 'print', 'range', 'repr',
            'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
            'tuple', 'type', 'zip'
        }
    
    async def execute(self, code: str) -> Dict[str, Any]:
        """Execute Python code safely."""
        try:
            # Validate code syntax
            validation_result = self._validate_code(code)
            if not validation_result["safe"]:
                return {
                    "status": "error",
                    "error": validation_result["error"],
                    "output": "",
                    "execution_time": 0
                }
            
            # Execute code with timeout
            start_time = time.time()
            result = await asyncio.wait_for(
                self._run_code(code),
                timeout=self.timeout
            )
            execution_time = time.time() - start_time
            
            return {
                "status": "success",
                "output": result["output"][:self.max_output_length],
                "error": result["error"],
                "execution_time": execution_time
            }
            
        except asyncio.TimeoutError:
            return {
                "status": "error",
                "error": "Code execution timeout (10s limit)",
                "output": "",
                "execution_time": self.timeout
            }
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "output": "",
                "execution_time": 0
            }
    
    def _validate_code(self, code: str) -> Dict[str, Any]:
        """Validate code for safety."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {"safe": False, "error": f"Syntax error: {str(e)}"}
        
        # Check for dangerous operations
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in self.allowed_modules:
                        return {"safe": False, "error": f"Module '{alias.name}' not allowed"}
            
            elif isinstance(node, ast.ImportFrom):
                if node.module not in self.allowed_modules:
                    return {"safe": False, "error": f"Module '{node.module}' not allowed"}
            
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['exec', 'eval', 'compile', '__import__']:
                        return {"safe": False, "error": f"Function '{node.func.id}' not allowed"}
            
            elif isinstance(node, ast.Attribute):
                if node.attr in ['__globals__', '__locals__', '__dict__', '__class__']:
                    return {"safe": False, "error": f"Attribute '{node.attr}' not allowed"}
        
        return {"safe": True, "error": None}
    
    async def _run_code(self, code: str) -> Dict[str, str]:
        """Run code in restricted environment."""
        def execute_in_thread():
            # Capture stdout and stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            try:
                sys.stdout = stdout_capture
                sys.stderr = stderr_capture
                
                # Create restricted globals
                restricted_globals = {
                    '__builtins__': {name: getattr(__builtins__, name) 
                                   for name in self.safe_builtins 
                                   if hasattr(__builtins__, name)}
                }
                
                # Execute code
                exec(code, restricted_globals, {})
                
                return {
                    "output": stdout_capture.getvalue(),
                    "error": stderr_capture.getvalue()
                }
                
            except Exception as e:
                return {
                    "output": stdout_capture.getvalue(),
                    "error": f"{stderr_capture.getvalue()}\nExecution error: {str(e)}"
                }
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
        
        # Run in thread to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, execute_in_thread)
    
    def get_example_code(self, topic: str) -> str:
        """Get example code for learning topics."""
        examples = {
            "python_basics": '''# Python Basics Example
print("Hello, World!")
numbers = [1, 2, 3, 4, 5]
squared = [x**2 for x in numbers]
print(f"Original: {numbers}")
print(f"Squared: {squared}")
''',
            "data_structures": '''# Data Structures Example
# Dictionary operations
student = {"name": "Alice", "age": 25, "courses": ["Python", "ML"]}
print(f"Student: {student['name']}, Age: {student['age']}")

# List operations
courses = student["courses"]
courses.append("Data Science")
print(f"Updated courses: {courses}")
''',
            "algorithms": '''# Algorithm Example - Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Test the algorithm
numbers = [1, 3, 5, 7, 9, 11, 13, 15]
result = binary_search(numbers, 7)
print(f"Found 7 at index: {result}")
'''
        }
        
        return examples.get(topic, examples["python_basics"])