"""
Java Parser Agent

Responsible for parsing Java source code and extracting relevant information
for test generation, including methods, classes, dependencies, and structure.
"""

import re
from typing import Dict, List, Any


class JavaParser:
    """Agent for parsing Java source code and extracting testable components."""
    
    def parse_java_file(self, file_content: str) -> Dict[str, Any]:
        """
        Parse Java source code and extract relevant information.
        
        Args:
            file_content: Raw Java source code as string
            
        Returns:
            Dictionary containing parsed information:
            - class_name: Name of the main class
            - package: Package declaration
            - imports: List of import statements
            - methods: List of method information
            - fields: List of class fields
        """
        parsed_info = {
            "class_name": self._extract_class_name(file_content),
            "package": self._extract_package(file_content),
            "imports": self._extract_imports(file_content),
            "methods": self._extract_methods(file_content),
            "fields": self._extract_fields(file_content)
        }
        
        return parsed_info
    
    def _extract_class_name(self, content: str) -> str:
        """Extract the main class name from Java source."""
        class_pattern = r'public\s+class\s+(\w+)'
        match = re.search(class_pattern, content)
        return match.group(1) if match else "UnknownClass"
    
    def _extract_package(self, content: str) -> str:
        """Extract package declaration."""
        package_pattern = r'package\s+([\w.]+);'
        match = re.search(package_pattern, content)
        return match.group(1) if match else ""
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract all import statements."""
        import_pattern = r'import\s+([\w.*]+);'
        return re.findall(import_pattern, content)
    
    def _extract_methods(self, content: str) -> List[Dict[str, Any]]:
        """Extract method signatures and basic information."""
        method_pattern = r'(public|private|protected)\s+(\w+)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}'
        methods = []
        
        for match in re.finditer(method_pattern, content, re.DOTALL):
            visibility, return_type, method_name = match.groups()
            methods.append({
                "name": method_name,
                "visibility": visibility,
                "return_type": return_type,
                "signature": match.group(0).split('{')[0].strip()
            })
        
        return methods
    
    def _extract_fields(self, content: str) -> List[Dict[str, str]]:
        """Extract class fields/variables."""
        field_pattern = r'(private|public|protected)\s+(\w+)\s+(\w+);'
        fields = []
        
        for match in re.finditer(field_pattern, content):
            visibility, field_type, field_name = match.groups()
            fields.append({
                "name": field_name,
                "type": field_type,
                "visibility": visibility
            })
        
        return fields