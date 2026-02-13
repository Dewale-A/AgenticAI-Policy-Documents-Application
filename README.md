# 🔍 AgenticAI Policy Documents Application

A production-ready **multi-agent AI system** for automated policy compliance analysis and reporting. Built with [CrewAI](https://crewai.com), this system demonstrates how autonomous AI agents can collaborate to ingest, analyze, and report on policy documents.

## 🎯 Overview

This system automates compliance assessment using 3 specialized AI agents that work together sequentially, mimicking a real compliance team's workflow:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENTIC POLICY COMPLIANCE SYSTEM                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   📁 DOCUMENTS              🔍 ANALYSIS              📋 REPORTING          │
│   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐        │
│   │  Ingestion  │─────────▶│  Compliance │─────────▶│   Report    │        │
│   │    Agent    │          │   Analyst   │          │   Writer    │        │
│   └─────────────┘          └─────────────┘          └─────────────┘        │
│         │                        │                        │                 │
│         ▼                        ▼                        ▼                 │
│   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐        │
│   │  • Read     │          │  • Gap      │          │  • Executive│        │
│   │    PDFs     │          │    Analysis │          │    Summary  │        │
│   │  • Parse    │          │  • Risk     │          │  • Detailed │        │
│   │    DOCX     │          │    Scoring  │          │    Findings │        │
│   │  • Extract  │          │  • Reg      │          │  • Action   │        │
│   │    Content  │          │    Mapping  │          │    Items    │        │
│   └─────────────┘          └─────────────┘          └─────────────┘        │
│                                                                             │
│                          ┌─────────────────┐                               │
│                          │    OUTPUT       │                               │
│                          │  ✓ Markdown     │                               │
│                          │  ✓ PDF Export   │                               │
│                          │  ✓ Gap Matrix   │                               │
│                          └─────────────────┘                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🤖 Agent Roles

| Agent | Role | Tools |
|-------|------|-------|
| **Ingestion Agent** | Document Specialist | `document_reader`, `document_search` |
| **Analysis Agent** | Compliance Analyst | `document_search` |
| **Report Agent** | Report Writer | — |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key (or Anthropic)

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
# Edit .env and add your OPENAI_API_KEY
```

### Running the System

```bash
# List available documents
ls policy_documents/

# Run full analysis on all documents
python main.py

# Focus on specific regulatory area
python main.py --areas "GDPR,SOX"

# Generate executive summary only
python main.py --report executive

# Export to PDF
python main.py --pdf
```

## 📁 Project Structure

```
AgenticAI-Policy-Documents-Application/
├── main.py                 # Entry point with CLI
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── policy_documents/      # Input policy documents
│   ├── sample_data_governance_policy.md
│   └── sample_risk_management_policy.md
├── output/                # Generated reports
├── src/
│   ├── agents/
│   │   └── policy_agents.py    # Agent definitions
│   ├── tasks/
│   │   └── policy_tasks.py     # Task definitions
│   ├── tools/
│   │   └── document_tools.py   # Document processing tools
│   ├── config/
│   │   └── settings.py         # Configuration
│   ├── utils/
│   │   └── export.py           # PDF export utilities
│   └── crew.py                 # Crew orchestration
└── tests/                      # Unit tests
```

## 📊 Sample Documents

The system includes 2 sample policies demonstrating different compliance areas:

| Document | Type | Coverage |
|----------|------|----------|
| Data Governance Policy | Governance | GDPR, data classification, retention |
| Risk Management Policy | Risk | Enterprise risk, controls, monitoring |

Add your own PDF, DOCX, TXT, or MD files to `policy_documents/` for analysis.

## ⚙️ Configuration

Key settings in `.env`:

```bash
OPENAI_API_KEY=sk-...              # Required (or ANTHROPIC_API_KEY)
OPENAI_MODEL=gpt-4o-mini           # Model selection
DEFAULT_LLM_PROVIDER=openai        # openai or anthropic
POLICY_DOCS_DIR=./policy_documents # Input directory
OUTPUT_DIR=./output                # Output directory
```

## 📋 Output Report

Reports are generated in Markdown and include:

- **Executive Summary**: Overall compliance posture
- **Gap Analysis**: Missing or incomplete policies
- **Regulatory Mapping**: Policy-to-regulation coverage
- **Risk Assessment**: Prioritized findings by severity
- **Recommendations**: Actionable remediation steps

## 🔧 Extending the System

### Adding Custom Tools
```python
from crewai.tools import BaseTool

class RegulationLookupTool(BaseTool):
    name: str = "regulation_lookup"
    description: str = "Look up specific regulatory requirements"
    
    def _run(self, regulation: str) -> str:
        # Implementation
        return result
```

### Supported Document Formats
- PDF (requires `pypdf`)
- DOCX (requires `python-docx`)
- TXT, MD (native)

## 📈 Future Enhancements

- [ ] Vector database for large document sets
- [ ] Regulatory framework templates (GDPR, SOX, HIPAA)
- [ ] Real-time policy monitoring
- [ ] Web interface dashboard
- [ ] Automated policy update detection
- [ ] Integration with GRC platforms

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author

**Dewale A** - Data & AI Governance Professional
- GitHub: [@Dewale-A](https://github.com/Dewale-A)
- LinkedIn: [Connect](https://linkedin.com/in/dewale-a)

---

*Built as part of a portfolio demonstrating autonomous multi-agent systems for financial services.*
