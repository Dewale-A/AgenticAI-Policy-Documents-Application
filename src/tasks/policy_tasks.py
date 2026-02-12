"""Policy document processing tasks using CrewAI."""

from crewai import Task, Agent


def create_ingestion_task(agent: Agent, document_focus: str = None) -> Task:
    """
    Create the document ingestion task.
    
    Args:
        agent: The ingestion agent to perform this task
        document_focus: Optional specific document or topic to focus on
    """
    focus_instruction = ""
    if document_focus:
        focus_instruction = f"\n\nFocus specifically on: {document_focus}"
    
    return Task(
        description=f"""
        Perform a comprehensive ingestion and extraction of all policy documents.
        
        Your tasks:
        1. First, list all available policy documents using the document_reader tool
        2. Read each document thoroughly using the document_reader tool
        3. For each document, identify and extract:
           - Document title, version, and effective date
           - Document purpose and scope
           - Key policy statements and requirements
           - Defined roles and responsibilities
           - Compliance obligations and controls
           - Referenced regulations or standards
           - Review/update requirements
        4. Note any cross-references between documents
        5. Flag any areas that are unclear or potentially incomplete
        {focus_instruction}
        
        Organize your findings in a structured format that facilitates analysis.
        """,
        expected_output="""
        A comprehensive structured extraction containing:
        1. Document inventory with metadata
        2. Key policy requirements organized by theme
        3. Compliance controls and obligations
        4. Roles and responsibilities matrix
        5. Cross-reference map between documents
        6. Initial observations and potential gaps
        """,
        agent=agent,
    )


def create_analysis_task(agent: Agent, ingestion_task: Task, focus_areas: list = None) -> Task:
    """
    Create the policy analysis task.
    
    Args:
        agent: The analysis agent to perform this task
        ingestion_task: The preceding ingestion task (for context)
        focus_areas: Optional list of specific areas to analyze
    """
    focus_instruction = ""
    if focus_areas:
        areas = ", ".join(focus_areas)
        focus_instruction = f"\n\nPay special attention to these focus areas: {areas}"
    
    return Task(
        description=f"""
        Analyze the extracted policy content to assess compliance posture and identify gaps.
        
        Using the ingestion results, perform the following analysis:
        
        1. **Regulatory Mapping**
           - Map policies to relevant regulatory frameworks (GDPR, SOX, Basel, etc.)
           - Identify which requirements are addressed by existing policies
           - Note any regulatory requirements without corresponding policies
        
        2. **Gap Analysis**
           - Identify missing policies or incomplete coverage
           - Find inconsistencies between related policies
           - Highlight outdated policies requiring review
           - Note areas where policy language is ambiguous
        
        3. **Risk Assessment**
           - Assess compliance risk for each gap identified
           - Prioritize gaps by potential business impact
           - Consider regulatory enforcement trends
        
        4. **Control Effectiveness**
           - Evaluate whether stated controls are adequate
           - Identify controls that may be difficult to implement
           - Note missing monitoring or enforcement mechanisms
        {focus_instruction}
        
        Provide evidence-based findings with specific references to document sections.
        """,
        expected_output="""
        A detailed analysis report containing:
        1. Regulatory mapping matrix
        2. Prioritized gap inventory with risk ratings
        3. Control effectiveness assessment
        4. Compliance risk heat map
        5. Evidence and citations for all findings
        """,
        agent=agent,
        context=[ingestion_task],
    )


def create_report_task(agent: Agent, analysis_task: Task, report_type: str = "full") -> Task:
    """
    Create the report generation task.
    
    Args:
        agent: The report agent to perform this task
        analysis_task: The preceding analysis task (for context)
        report_type: Type of report - "executive", "detailed", or "full"
    """
    report_instructions = {
        "executive": """
        Create an executive summary (1-2 pages) that includes:
        - Overall compliance posture assessment
        - Top 3-5 priority items requiring attention
        - High-level recommendations
        - Resource/timeline estimates for remediation
        """,
        "detailed": """
        Create a detailed technical report that includes:
        - Comprehensive findings with evidence
        - Detailed gap descriptions and root causes
        - Specific remediation steps for each finding
        - Implementation guidance and best practices
        """,
        "full": """
        Create a comprehensive compliance report with both executive and detailed sections:
        
        EXECUTIVE SUMMARY:
        - Overall compliance score/rating
        - Key findings summary
        - Strategic recommendations
        - Resource requirements
        
        DETAILED FINDINGS:
        - Complete gap analysis with evidence
        - Regulatory mapping details
        - Control assessment results
        - Prioritized remediation roadmap
        
        APPENDICES:
        - Document inventory
        - Regulatory reference guide
        - Glossary of terms
        """
    }
    
    return Task(
        description=f"""
        Generate a professional compliance report based on the policy analysis.
        
        {report_instructions.get(report_type, report_instructions["full"])}
        
        Ensure the report:
        - Uses clear, professional language
        - Provides actionable recommendations
        - Includes specific citations and evidence
        - Is appropriate for both technical and non-technical audiences
        - Follows compliance reporting best practices
        """,
        expected_output="""
        A professional, well-structured compliance report in markdown format that:
        1. Can be shared with executive leadership
        2. Provides clear next steps for compliance teams
        3. Documents the current state with evidence
        4. Offers a path to improved compliance posture
        """,
        agent=agent,
        context=[analysis_task],
        output_file="output/compliance_report.md",
    )
