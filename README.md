# 🔍 Policy Documents Agentic AI Application

An autonomous multi-agent system for ingesting, analyzing, and reporting on policy documents for compliance assessment. Built with [CrewAI](https://crewai.com) and powered by OpenAI/Anthropic LLMs.

## 🎯 Overview

This proof-of-concept demonstrates how autonomous AI agents can work together to:
1. **Ingest** policy documents (PDF, DOCX, TXT, MD)
2. **Analyze** compliance posture and identify gaps
3. **Generate** professional compliance reports

### Use Cases
- Regulatory compliance assessment
- Policy gap analysis
- Pre-audit preparation
- Data governance reviews
- Risk management analysis

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CrewAI Orchestration                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Ingestion   │───▶│   Analysis   │───▶│    Report    │      │
│  │    Agent     │    │    Agent     │    │    Agent     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Document   │    │     Gap      │    │  Compliance  │      │
│  │  Extraction  │    │   Analysis   │    │    Report    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Agents

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Ingestion Agent** | Document Specialist | Read documents, extract key information, identify structure |
| **Analysis Agent** | Compliance Analyst | Map to regulations, identify gaps, assess risk |
| **Report Agent** | Report Writer | Synthesize findings, create actionable reports |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key or Anthropic API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Dewale-A/AgenticAI-Policy-Documents-Application.git
cd AgenticAI-Policy-Documents-Application

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys
```

### Add Policy Documents

Place your policy documents in the `policy_documents/` directory:
```bash
policy_documents/
├── data_governance_policy.pdf
├── risk_management_policy.docx
├── information_security_policy.txt
└── ...
```

Supported formats: PDF, DOCX, DOC, TXT, MD

### Run Analysis

```bash
# Run full analysis
python main.py

# Focus on specific topic
python main.py --focus "data governance"

# Focus on specific regulations
python main.py --areas "GDPR,SOX"

# Generate executive summary only
python main.py --report executive
```

## 📋 Output

Reports are saved to `output/compliance_report.md` and include:

- **Executive Summary**: High-level compliance posture
- **Gap Analysis**: Detailed findings with risk ratings
- **Regulatory Mapping**: Policy-to-regulation mapping
- **Recommendations**: Prioritized action items

## 📁 Project Structure

```
AgenticAI-Policy-Documents-Application/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── src/
│   ├── agents/            # CrewAI agent definitions
│   │   └── policy_agents.py
│   ├── tasks/             # CrewAI task definitions
│   │   └── policy_tasks.py
│   ├── tools/             # Custom tools
│   │   └── document_tools.py
│   ├── config/            # Configuration
│   │   └── settings.py
│   └── crew.py            # Crew orchestration
├── policy_documents/      # Input documents
└── output/                # Generated reports
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `DEFAULT_LLM_PROVIDER` | LLM to use (openai/anthropic) | openai |
| `OPENAI_MODEL` | OpenAI model name | gpt-4-turbo-preview |
| `ANTHROPIC_MODEL` | Anthropic model name | claude-3-sonnet-20240229 |
| `POLICY_DOCS_DIR` | Documents directory | ./policy_documents |
| `OUTPUT_DIR` | Output directory | ./output |

## 🔮 Roadmap

- [ ] Add support for more document formats (HTML, XML)
- [ ] Implement vector database for large document sets
- [ ] Add regulatory framework templates (GDPR, SOX, Basel)
- [ ] Create web interface
- [ ] Add scheduled monitoring capabilities
- [ ] Export to PDF/PowerPoint formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Wale Aderonmu** - [GitHub](https://github.com/Dewale-A)

---

Built with ❤️ using [CrewAI](https://crewai.com) | Part of the journey to mastering autonomous multi-agent systems
