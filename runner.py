#!/usr/bin/env python3
"""
Java Test Writer Assistant Runner

Main orchestration script that coordinates all agents to generate JUnit tests
from Java source code using Claude via AWS Bedrock.
"""

import argparse
import os
import sys
from pathlib import Path

from agents.java_parser import JavaParser
from agents.test_strategy import TestStrategy
from agents.test_writer import TestWriter


class TestGeneratorOrchestrator:
    """Main orchestrator for the test generation pipeline."""
    
    def __init__(self):
        self.java_parser = JavaParser()
        self.test_strategy = TestStrategy()
        self.test_writer = TestWriter()
    
    def generate_tests(self, input_file: str, output_dir: str = "outputs") -> str:
        """
        Generate JUnit tests for a Java source file.
        
        Args:
            input_file: Path to Java source file
            output_dir: Directory to write generated test file
            
        Returns:
            Path to generated test file
        """
        print(f"Processing Java file: {input_file}")
        
        # Step 1: Parse Java source code
        print("Step 1: Parsing Java source code...")
        with open(input_file, 'r') as f:
            java_content = f.read()
        
        parsed_info = self.java_parser.parse_java_file(java_content)
        print(f"Found class: {parsed_info['class_name']}")
        print(f"Found {len(parsed_info['methods'])} methods")
        
        # Step 2: Generate test strategies
        print("Step 2: Generating test strategies...")
        test_strategies = self.test_strategy.generate_test_strategies(parsed_info)
        print(f"Generated {len(test_strategies['test_methods'])} test cases")
        
        # Step 3: Generate test code
        print("Step 3: Generating JUnit test code...")
        test_code = self.test_writer.generate_test_code(test_strategies, parsed_info)
        
        # Step 4: Write output file
        output_path = self._write_test_file(test_code, test_strategies['test_class_name'], output_dir)
        print(f"Generated test file: {output_path}")
        
        return output_path
    
    def _write_test_file(self, test_code: str, test_class_name: str, output_dir: str) -> str:
        """Write generated test code to file."""
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{test_class_name}.java")
        
        with open(output_file, 'w') as f:
            f.write(test_code)
        
        return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate JUnit tests from Java source code using AI"
    )
    parser.add_argument(
        "input_file",
        help="Path to Java source file"
    )
    parser.add_argument(
        "-o", "--output",
        default="outputs",
        help="Output directory for generated tests (default: outputs)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not args.input_file.endswith('.java'):
        print(f"Error: Input file must be a Java source file (.java)", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Initialize orchestrator and generate tests
        orchestrator = TestGeneratorOrchestrator()
        output_file = orchestrator.generate_tests(args.input_file, args.output)
        
        print(f"\n✅ Successfully generated test file: {output_file}")
        print("\nNext steps:")
        print("1. Review the generated test code")
        print("2. Add specific test data and assertions")
        print("3. Configure AWS Bedrock credentials for AI-enhanced test generation")
        
    except Exception as e:
        print(f"Error generating tests: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()