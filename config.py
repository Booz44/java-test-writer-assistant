"""
Configuration settings for Java Test Writer Assistant
"""

# AWS Bedrock Configuration
AWS_REGION = "ap-southeast-2"
CLAUDE_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
MAX_TOKENS = 1000
API_DELAY_SECONDS = 10

# Project Settings
DEFAULT_OUTPUT_DIR = "outputs"
SAMPLE_INPUT_DIR = "sample_inputs"

# Test Generation Settings
INDENTATION_SPACES = "        "  # 8 spaces for method body
TIMEOUT_SECONDS = 300