"""
Test Code Writer Agent

Responsible for generating actual JUnit test code based on test strategies.
Uses Claude via AWS Bedrock to generate high-quality test implementations.
"""

from typing import Dict, List, Any


class TestWriter:
    """Agent for generating JUnit test code from test strategies."""
    
    def generate_test_code(self, test_strategies: Dict[str, Any], parsed_info: Dict[str, Any]) -> str:
        """
        Generate complete JUnit test class code.
        
        Args:
            test_strategies: Dictionary from TestStrategy containing test plans
            parsed_info: Dictionary from JavaParser containing class structure
            
        Returns:
            Complete JUnit test class as string
        """
        test_class = self._build_test_class_structure(test_strategies, parsed_info)
        return test_class
    
    def _build_test_class_structure(self, strategies: Dict[str, Any], parsed_info: Dict[str, Any]) -> str:
        """Build the complete test class structure."""
        class_name = strategies["test_class_name"]
        package = parsed_info["package"]
        
        # Build imports
        imports = self._generate_imports(strategies, parsed_info)
        
        # Build class header
        class_header = f"public class {class_name} {{"
        
        # Build setup methods
        setup_code = self._generate_setup_code(strategies)
        
        # Build test methods
        test_methods = self._generate_test_methods(strategies["test_methods"])
        
        # Combine all parts
        full_class = f"""package {package};

{imports}

{class_header}
{setup_code}
{test_methods}
}}"""
        
        return full_class
    
    def _generate_imports(self, strategies: Dict[str, Any], parsed_info: Dict[str, Any]) -> str:
        """Generate import statements for the test class."""
        imports = [
            "import org.junit.jupiter.api.Test;",
            "import org.junit.jupiter.api.BeforeEach;",
            "import org.junit.jupiter.api.Assertions.*;",
            "import static org.mockito.Mockito.*;",
            f"import {parsed_info['package']}.{parsed_info['class_name']};"
        ]
        
        # Add additional imports based on mock requirements
        if "database" in strategies.get("mock_requirements", []):
            imports.append("import org.mockito.Mock;")
        
        return "\n".join(imports)
    
    def _generate_setup_code(self, strategies: Dict[str, Any]) -> str:
        """Generate @BeforeEach setup method."""
        setup_requirements = strategies.get("setup_requirements", [])
        
        if not setup_requirements:
            return ""
        
        setup_code = """
    @BeforeEach
    void setUp() {
        // Initialize test objects and dependencies
"""
        
        if "object_initialization" in setup_requirements:
            setup_code += "        // TODO: Initialize class under test\n"
        
        if "database_setup" in setup_requirements:
            setup_code += "        // TODO: Set up database mocks/test data\n"
        
        if "file_system_setup" in setup_requirements:
            setup_code += "        // TODO: Set up file system test environment\n"
        
        setup_code += "    }\n"
        
        return setup_code
    
    def _generate_test_methods(self, test_methods: List[Dict[str, Any]]) -> str:
        """Generate individual test methods."""
        methods = []
        
        for test_method in test_methods:
            method_code = self._generate_single_test_method(test_method)
            methods.append(method_code)
        
        return "\n".join(methods)
    
    def _generate_single_test_method(self, test_method: Dict[str, Any]) -> str:
        """Generate a single test method."""
        test_name = test_method["test_name"]
        description = test_method["description"]
        test_type = test_method["test_type"]
        
        print(f"  Generating test: {test_name}")
        
        # Use Claude to generate the actual test implementation
        prompt = self._build_test_generation_prompt(test_method)
        test_implementation = self._generate_test_implementation(prompt)
        
        method_code = f"""
    @Test
    void {test_name}() {{
        // {description}
{test_implementation}
    }}"""
        
        return method_code
    
    def _build_test_generation_prompt(self, test_method: Dict[str, Any]) -> str:
        """Build prompt for Claude to generate test implementation."""
        prompt = f"""
Generate only the Java method body code for this test case:

Test: {test_method['test_name']}
Type: {test_method['test_type']}
Description: {test_method['description']}

Requirements:
1. Return ONLY Java code statements (no @Test annotation, no method signature, no explanations)
2. Use proper indentation (8 spaces)
3. Include Arrange-Act-Assert comments
4. Use Calculator class methods like calculator.add(), calculator.divide(), etc.
5. Use JUnit 5 assertions: assertEquals(), assertThrows(), assertTrue()

Example format:
        // Arrange
        Calculator calculator = new Calculator();
        int a = 5;
        int b = 3;
        
        // Act
        int result = calculator.add(a, b);
        
        // Assert
        assertEquals(8, result);
"""
        return prompt
    
    def _generate_test_implementation(self, prompt: str) -> str:
        """
        Generate test implementation using Claude via AWS Bedrock.
        """
        import boto3
        import json
        import time
        
        try:
            from config import AWS_REGION, CLAUDE_MODEL_ID, MAX_TOKENS, API_DELAY_SECONDS
            
            print("    → Generating test implementation with Claude...", end=" ", flush=True)
            bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
            
            response = bedrock.invoke_model(
                modelId=CLAUDE_MODEL_ID,
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': MAX_TOKENS,
                    'messages': [{'role': 'user', 'content': prompt}]
                })
            )
            
            response_body = json.loads(response['body'].read())
            print("✓")
            
            # Add delay to avoid throttling
            time.sleep(API_DELAY_SECONDS)
            
            # Clean up the response to remove markdown formatting
            raw_response = response_body['content'][0]['text']
            cleaned_response = self._clean_response(raw_response)
            
            return cleaned_response
            
        except Exception as e:
            # Fallback to template if Bedrock fails
            print(f"✗ (using template)")
            print(f"    Warning: Bedrock API failed - {e}")
            return """        // Arrange
        // TODO: Set up test data and dependencies
        
        // Act
        // TODO: Call the method under test
        
        // Assert
        // TODO: Verify expected behavior
        // Example: assertEquals(expected, actual);"""
    
    def _clean_response(self, response: str) -> str:
        """Clean Claude's response to remove markdown formatting and extract only Java code."""
        import re
        from config import INDENTATION_SPACES
        
        # Remove markdown code blocks
        response = re.sub(r'```java\s*\n', '', response)
        response = re.sub(r'```\s*$', '', response, flags=re.MULTILINE)
        response = re.sub(r'^```.*$', '', response, flags=re.MULTILINE)
        
        # Remove ALL explanation text and intro phrases (more aggressive)
        patterns_to_remove = [
            r'Here is the Java method body code.*?:',
            r'Here\'s the Java method body code.*?:',
            r'Here is the.*?implementation.*?:',
            r'Here\'s the.*?implementation.*?:',
            r'The following is the.*?:',
            r'Below is the.*?:',
            r'\n\s*Explanation:.*$',
            r'\n\s*This test.*$',
            r'\n\s*In this.*$',
            r'\n\s*Note:.*$',
            r'\n\s*The.*?method.*$',
        ]
        
        for pattern in patterns_to_remove:
            response = re.sub(pattern, '', response, flags=re.DOTALL)
        
        # Remove duplicate method signatures and annotations
        response = re.sub(r'@Test\s*\n\s*void\s+test\w+\(\)\s*\{', '', response)
        response = re.sub(r'@BeforeEach\s*\n\s*void\s+setUp\(\)\s*\{[^}]*\}', '', response)
        
        # Remove any remaining markdown formatting
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)  # Remove bold
        response = re.sub(r'\*(.*?)\*', r'\1', response)      # Remove italic
        
        # Fix malformed statements
        response = re.sub(r'^Arrange:\s*$', f'{INDENTATION_SPACES}// Arrange', response, flags=re.MULTILINE)
        response = re.sub(r'^Act:\s*$', f'{INDENTATION_SPACES}// Act', response, flags=re.MULTILINE)
        response = re.sub(r'^Assert:\s*$', f'{INDENTATION_SPACES}// Assert', response, flags=re.MULTILINE)
        
        # Remove standalone opening braces and other non-Java lines
        response = re.sub(r'^\s*\{\s*$', '', response, flags=re.MULTILINE)
        response = re.sub(r'^[^/\s].*?[^;{}]\s*$', '', response, flags=re.MULTILINE)  # Remove non-Java sentences
        
        # Clean up and ensure proper Java formatting
        lines = response.split('\n')
        cleaned_lines = []
        java_keywords = ['import', 'package', 'public', 'private', 'protected', 'static', 'final', 'class', 
                        'interface', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 
                        'continue', 'return', 'try', 'catch', 'finally', 'throw', 'throws', 'new', 
                        'this', 'super', 'null', 'true', 'false', 'void', 'int', 'double', 'boolean',
                        'String', 'List', 'Map', 'Set', 'assertEquals', 'assertTrue', 'assertFalse',
                        'assertThrows', 'assertNotNull', 'assertNull', 'Calculator', '//', '/*', '*/',
                        'Arrange', 'Act', 'Assert']
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                cleaned_lines.append(line)  # Keep empty lines for formatting
                continue
                
            # Keep lines that are clearly Java code
            if (stripped.startswith('//') or 
                stripped.endswith(';') or 
                stripped.endswith('{') or 
                stripped.endswith('}') or
                any(keyword in stripped for keyword in java_keywords) or
                '=' in stripped or
                '(' in stripped):
                
                # Ensure proper indentation
                if stripped and not line.startswith(INDENTATION_SPACES):
                    line = INDENTATION_SPACES + stripped
                cleaned_lines.append(line)
        
        # Remove leading/trailing empty lines
        while cleaned_lines and not cleaned_lines[0].strip():
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()
            
        return '\n'.join(cleaned_lines)