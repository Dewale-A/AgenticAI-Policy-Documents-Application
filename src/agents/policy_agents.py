"""Policy document processing agents using CrewAI."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from src.config.settings import (
    DEFAULT_LLM_PROVIDER,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    OPENAI_MODEL,
    ANTHROPIC_MODEL,
)
from src.tools.document_tools import DocumentReaderTool, DocumentSearchTool


def get_llm():
    """Get the configured LLM based on settings."""
    if DEFAULT_LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        return ChatAnthropic(
            model=ANTHROPIC_MODEL,
            api_key=ANTHROPIC_API_KEY,
            temperature=0.1,
        )
    elif OPENAI_API_KEY:
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.1,
        )
    else:
        raise ValueError("No valid LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.")


def create_ingestion_agent() -> Agent:
    """
    Create the Document Ingestion Agent.
    
    This agent is responsible for:
    - Discovering and reading policy documents
    - Extracting key information from documents
    - Identifying document structure and sections
    - Preparing content for analysis
    """
    return Agent(
        role="Policy Document Ingestion Specialist",
        goal="""Thoroughly read and extract all relevant information from policy documents.
        Identify key sections, requirements, controls, and compliance obligations.
        Organize extracted information in a structured format for analysis.""",
        backstory="""You are an expert document analyst with years of experience in 
        financial services and regulatory compliance. You have a keen eye for detail 
        and can quickly identify important policy requirements, controls, and obligations.
        You understand regulatory frameworks like GDPR, SOX, Basel III, and industry 
        standards for data governance and risk management.""",
        tools=[DocumentReaderTool(), DocumentSearchTool()],
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_analysis_agent() -> Agent:
    """
    Create the Policy Analysis Agent.
    
    This agent is responsible for:
    - Analyzing extracted policy content
    - Identifying gaps and inconsistencies
    - Mapping policies to regulatory requirements
    - Assessing compliance posture
    """
    return Agent(
        role="Policy Compliance Analyst",
        goal="""Analyze policy documents to identify compliance requirements, gaps, 
        and areas of concern. Map policies to relevant regulatory frameworks and 
        assess organizational compliance posture.""",
        backstory="""You are a senior compliance analyst with deep expertise in 
        financial regulations, data governance, and enterprise risk management. 
        You have helped numerous organizations navigate complex regulatory landscapes 
        and implement effective compliance programs. You understand both the letter 
        and spirit of regulations and can identify potential risks before they 
        become issues.""",
        tools=[DocumentSearchTool()],
        llm=get_llm(),
        verbose=True,
        allow_delegation=True,
    )


def create_report_agent() -> Agent:
    """
    Create the Report Generation Agent.
    
    This agent is responsible for:
    - Synthesizing analysis findings
    - Creating executive summaries
    - Generating detailed compliance reports
    - Providing actionable recommendations
    """
    return Agent(
        role="Compliance Report Writer",
        goal="""Create clear, comprehensive, and actionable compliance reports 
        based on policy analysis. Provide executive summaries for leadership and 
        detailed findings for implementation teams.""",
        backstory="""You are a skilled technical writer with expertise in 
        compliance reporting and executive communications. You can distill 
        complex regulatory analysis into clear, actionable insights. Your reports 
        are known for being thorough yet accessible, helping organizations 
        understand their compliance posture and next steps.""",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )
