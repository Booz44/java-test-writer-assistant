"""
Test Strategy Agent

Responsible for analyzing parsed Java code and determining the most appropriate
testing strategies and scenarios for each method and class.
"""

from typing import Dict, List, Any


class TestStrategy:
    """Agent for determining test strategies based on parsed Java code."""
    
    def generate_test_strategies(self, parsed_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate test strategies for parsed Java code.
        
        Args:
            parsed_info: Dictionary from JavaParser containing class structure
            
        Returns:
            Dictionary containing test strategies:
            - test_class_name: Name for the test class
            - test_methods: List of test method strategies
            - setup_requirements: Any setup needed for tests
            - mock_requirements: Dependencies that need mocking
        """
        test_strategies = {
            "test_class_name": f"{parsed_info['class_name']}Test",
            "test_methods": self._generate_method_strategies(parsed_info["methods"]),
            "setup_requirements": self._analyze_setup_requirements(parsed_info),
            "mock_requirements": self._analyze_mock_requirements(parsed_info)
        }
        
        return test_strategies
    
    def _generate_method_strategies(self, methods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate test strategies for each method."""
        strategies = []
        
        for method in methods:
            if method["visibility"] == "public":
                method_strategies = self._create_method_test_cases(method)
                strategies.extend(method_strategies)
        
        return strategies
    
    def _create_method_test_cases(self, method: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create specific test cases for a method."""
        test_cases = []
        method_name = method["name"]
        return_type = method["return_type"]
        
        # Happy path test
        test_cases.append({
            "test_name": f"test{method_name.capitalize()}HappyPath",
            "test_type": "happy_path",
            "description": f"Test {method_name} with valid inputs",
            "expected_behavior": "Should return expected result"
        })
        
        # Edge case tests based on return type
        if return_type in ["int", "long", "double", "float"]:
            test_cases.append({
                "test_name": f"test{method_name.capitalize()}WithZero",
                "test_type": "edge_case",
                "description": f"Test {method_name} with zero values",
                "expected_behavior": "Should handle zero appropriately"
            })
        
        if return_type == "String":
            test_cases.append({
                "test_name": f"test{method_name.capitalize()}WithNullInput",
                "test_type": "null_case",
                "description": f"Test {method_name} with null input",
                "expected_behavior": "Should handle null input gracefully"
            })
        
        # Exception test if method name suggests it might throw
        if "validate" in method_name.lower() or "check" in method_name.lower():
            test_cases.append({
                "test_name": f"test{method_name.capitalize()}ThrowsException",
                "test_type": "exception",
                "description": f"Test {method_name} throws exception for invalid input",
                "expected_behavior": "Should throw appropriate exception"
            })
        
        return test_cases
    
    def _analyze_setup_requirements(self, parsed_info: Dict[str, Any]) -> List[str]:
        """Analyze what setup is needed for tests."""
        setup_requirements = []
        
        # Check if class has fields that need initialization
        if parsed_info["fields"]:
            setup_requirements.append("object_initialization")
        
        # Check for common patterns that need setup
        imports = parsed_info["imports"]
        if any("Database" in imp or "Connection" in imp for imp in imports):
            setup_requirements.append("database_setup")
        
        if any("File" in imp or "IO" in imp for imp in imports):
            setup_requirements.append("file_system_setup")
        
        return setup_requirements
    
    def _analyze_mock_requirements(self, parsed_info: Dict[str, Any]) -> List[str]:
        """Analyze what dependencies need to be mocked."""
        mock_requirements = []
        
        imports = parsed_info["imports"]
        
        # Common patterns that typically need mocking
        mock_patterns = {
            "http": ["HttpClient", "RestTemplate", "WebClient"],
            "database": ["Repository", "DAO", "EntityManager"],
            "external_service": ["Service", "Client", "API"],
            "file_system": ["FileWriter", "FileReader", "Path"]
        }
        
        for mock_type, patterns in mock_patterns.items():
            if any(any(pattern in imp for pattern in patterns) for imp in imports):
                mock_requirements.append(mock_type)
        
        return mock_requirements