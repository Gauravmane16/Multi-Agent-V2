# Code Assistant App

A Streamlit-based application that helps developers analyze, optimize, review, and compare code using AI agents powered by OpenAI's GPT models.

## Features

- **Code Optimization**: Improve code efficiency and readability
- **Code Review**: Get feedback on bugs, security issues, and best practices
- **Code Comparison**: Compare two code files and analyze differences

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Gauravmane16/Multi-Agent-V2.git
cd code-assistant-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Configuration

1. Get your OpenAI API key:
   - Sign up at [OpenAI Platform](https://platform.openai.com/signup)
   - Navigate to API Keys section
   - Create a new secret key
   - Add billing information (new accounts get free credits)

2. Enter your API key in the app's sidebar when prompted

## Dependencies

```text
streamlit>=1.22.0
langchain>=0.0.267
openai>=0.27.8
chromadb>=0.4.6
python-dotenv>=1.0.0
difflib>=3.7.0
tiktoken>=0.4.0
langchain-openai>=0.0.2
```

## Features in Detail

### Code Optimization
- Analyzes code structure and patterns
- Suggests performance improvements
- Recommends better coding practices

### Code Review
- Identifies potential bugs
- Checks for security vulnerabilities
- Suggests code style improvements

### Code Comparison
- Side-by-side diff view
- Highlights changes between versions
- Analyzes impact of modifications

## License

Copyright © 2025 Gaurav Mane. All rights reserved.

## Author

Gaurav Mane