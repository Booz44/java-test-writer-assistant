# 🤖 Java Test Writer Assistant

An AI-powered tool that automatically generates comprehensive JUnit test suites from Java source code using Claude 3 via AWS Bedrock. This project demonstrates advanced prompt engineering, agent-based architecture, and practical AI integration for software development workflows.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)
[![JUnit 5](https://img.shields.io/badge/JUnit-5-green.svg)](https://junit.org/junit5/)
[![Claude 3](https://img.shields.io/badge/Claude-3%20Haiku-purple.svg)](https://www.anthropic.com/claude)

## 🚀 Key Capabilities

### Intelligent Test Generation
- **Automated JUnit 5 test creation** from Java source code
- **Smart test strategies** including happy path, edge cases, and exception scenarios
- **Proper Arrange-Act-Assert patterns** with real assertions
- **Exception testing** with `assertThrows()` for robust error handling
- **Mocking integration** suggestions for complex dependencies

### Advanced AI Integration
- **Claude 3 Haiku** via AWS Bedrock for fast, cost-effective test generation
- **Intelligent prompt engineering** with response cleaning and formatting
- **Rate limiting protection** with configurable delays to prevent API throttling
- **Graceful fallback** to templates when AI services are unavailable
- **Real-time progress feedback** with success/failure indicators

### Enterprise-Ready Architecture
- **Modular agent-based design** following single responsibility principle
- **Externalized configuration** for easy deployment and customization
- **Comprehensive error handling** with detailed logging and recovery
- **Production-quality output** generating compilable Java test code
- **Scalable processing** suitable for large codebases

## 🏗️ Architecture

The project uses a sophisticated agent-based architecture where each component has a specific responsibility:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Java Parser   │───▶│  Test Strategy   │───▶│   Test Writer   │
│     Agent       │    │     Agent        │    │     Agent       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Extract classes │    │ Analyze test     │    │ Generate JUnit  │
│ methods, fields │    │ scenarios &      │    │ code with       │
│ & dependencies  │    │ requirements     │    │ Claude AI       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Agent Responsibilities

1. **JavaParser Agent**: Extracts structural information from Java source code
2. **TestStrategy Agent**: Determines optimal testing approaches and scenarios
3. **TestWriter Agent**: Generates actual JUnit test implementations using Claude AI

## 📋 Prerequisites

- **Python 3.11+**
- **AWS Account** with Bedrock access
- **Claude 3 Haiku model** enabled in AWS Bedrock
- **AWS CLI** configured with appropriate credentials

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/java-test-writer-assistant.git
cd java-test-writer-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials
```bash
# Option 1: Using AWS CLI
aws configure

# Option 2: Using environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=ap-southeast-2
```

### 4. Enable Claude 3 in AWS Bedrock
1. Navigate to AWS Bedrock Console
2. Go to **Model access** in the left sidebar
3. Click **Manage model access**
4. Find **Anthropic** section and enable **Claude 3 Haiku**
5. Submit the access request (usually approved immediately)

### 5. Configure the Application
Edit `config.py` to customize settings:
```python
# AWS Bedrock Configuration
AWS_REGION = "ap-southeast-2"  # Your preferred region
CLAUDE_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
API_DELAY_SECONDS = 10  # Adjust based on your rate limits
```

## 🎯 Usage

### Basic Usage
Generate tests for a Java file:
```bash
python runner.py sample_inputs/Calculator.java
```

### Advanced Options
```bash
# Specify custom output directory
python runner.py sample_inputs/Calculator.java -o my_tests/

# Enable debug mode for detailed logging
python runner.py sample_inputs/Calculator.java --debug

# Get help
python runner.py --help
```

### Example Output
For the provided `Calculator.java` sample, the tool generates comprehensive tests:

```java
@Test
void testAddHappyPath() {
    // Arrange
    Calculator calculator = new Calculator();
    int a = 5;
    int b = 3;
    
    // Act
    int result = calculator.add(a, b);
    
    // Assert
    assertEquals(8, result);
}

@Test
void testDivideWithZero() {
    // Arrange
    Calculator calculator = new Calculator();
    int a = 10;
    int b = 0;
    
    // Act & Assert
    assertThrows(ArithmeticException.class, () -> calculator.divide(a, b));
}
```

## 📁 Project Structure

```
java-test-writer-assistant/
├── agents/                     # Core AI agents
│   ├── __init__.py
│   ├── java_parser.py         # Java source code parsing
│   ├── test_strategy.py       # Test scenario generation
│   └── test_writer.py         # AI-powered test code generation
├── sample_inputs/             # Example Java files
│   └── Calculator.java        # Sample calculator class
├── outputs/                   # Generated test files
│   └── CalculatorTest.java    # Generated test suite
├── config.py                  # Configuration settings
├── runner.py                  # Main orchestration script
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## ⚙️ Configuration Options

### AWS Bedrock Settings
```python
AWS_REGION = "ap-southeast-2"              # AWS region for Bedrock
CLAUDE_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"  # Claude model
MAX_TOKENS = 1000                          # Max tokens per API call
API_DELAY_SECONDS = 10                     # Delay between API calls
```

### Alternative Claude Models
- **Claude 3 Haiku**: Fast and cost-effective (default)
- **Claude 3 Sonnet**: Balanced performance and quality
- **Claude 3.5 Sonnet**: Highest quality, slower and more expensive

Update `CLAUDE_MODEL_ID` in `config.py` to switch models.

## 🎨 Generated Test Features

The AI generates tests with:

- ✅ **Proper JUnit 5 annotations** (`@Test`, `@BeforeEach`)
- ✅ **Comprehensive assertions** (`assertEquals`, `assertTrue`, `assertThrows`)
- ✅ **Exception handling** for error conditions
- ✅ **Edge case testing** (zero values, null inputs, boundary conditions)
- ✅ **Mocking setup** suggestions for complex dependencies
- ✅ **Clean code structure** with proper indentation and formatting
- ✅ **Descriptive test names** following naming conventions

## 🔧 Customization

### Adding Custom Test Strategies
Extend `TestStrategy` agent in `agents/test_strategy.py`:
```python
def _create_custom_test_cases(self, method):
    # Add your custom test case logic
    return custom_test_cases
```

### Modifying AI Prompts
Update prompts in `TestWriter` agent (`agents/test_writer.py`):
```python
def _build_test_generation_prompt(self, test_method):
    # Customize the prompt for specific requirements
    return enhanced_prompt
```

## 📊 Performance & Cost

### Typical Performance
- **Processing Speed**: ~15 test methods in 2.5 minutes (with 10s delays)
- **Success Rate**: >95% with Claude 3 Haiku
- **Cost**: ~$0.01-0.02 per test file (varies by complexity)

### Optimization Tips
- Reduce `API_DELAY_SECONDS` if you have higher rate limits
- Use Claude 3 Haiku for faster, cheaper generation
- Process multiple files in parallel for large codebases

## 🚀 Future Enhancements

- [ ] **Batch processing** for multiple Java files
- [ ] **Spring Boot test support** with `@MockBean` and `@WebMvcTest`
- [ ] **Database testing** with TestContainers integration
- [ ] **IDE plugin** for IntelliJ IDEA and VS Code
- [ ] **Custom test templates** for specific frameworks
- [ ] **Test coverage analysis** and gap identification
- [ ] **Integration with CI/CD pipelines**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- **Issues**: [GitHub Issues](https://github.com/your-username/java-test-writer-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/java-test-writer-assistant/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/java-test-writer-assistant/wiki)

## 🏆 Acknowledgments

- **Anthropic** for Claude 3 AI models
- **AWS Bedrock** for AI model hosting and inference
- **JUnit 5** team for the excellent testing framework
- **Python community** for robust libraries and tools

---

**Built with ❤️ for the developer community to accelerate test-driven development through AI automation.**