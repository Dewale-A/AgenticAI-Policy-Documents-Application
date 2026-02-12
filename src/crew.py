"""Main Crew definition for Policy Document Analysis."""

from crewai import Crew, Process

from src.agents.policy_agents import (
    create_ingestion_agent,
    create_analysis_agent,
    create_report_agent,
)
from src.tasks.policy_tasks import (
    create_ingestion_task,
    create_analysis_task,
    create_report_task,
)


def create_policy_analysis_crew(
    document_focus: str = None,
    focus_areas: list = None,
    report_type: str = "full",
) -> Crew:
    """
    Create the Policy Analysis Crew with all agents and tasks.
    
    Args:
        document_focus: Optional specific document or topic to focus on
        focus_areas: Optional list of regulatory areas to focus on
        report_type: Type of report to generate ("executive", "detailed", "full")
    
    Returns:
        Configured Crew ready to execute
    """
    # Create agents
    ingestion_agent = create_ingestion_agent()
    analysis_agent = create_analysis_agent()
    report_agent = create_report_agent()
    
    # Create tasks
    ingestion_task = create_ingestion_task(ingestion_agent, document_focus)
    analysis_task = create_analysis_task(analysis_agent, ingestion_task, focus_areas)
    report_task = create_report_task(report_agent, analysis_task, report_type)
    
    # Create and return the crew
    crew = Crew(
        agents=[ingestion_agent, analysis_agent, report_agent],
        tasks=[ingestion_task, analysis_task, report_task],
        process=Process.sequential,  # Tasks run in order
        verbose=True,
    )
    
    return crew


def run_policy_analysis(
    document_focus: str = None,
    focus_areas: list = None,
    report_type: str = "full",
) -> str:
    """
    Run the complete policy analysis workflow.
    
    Args:
        document_focus: Optional specific document or topic to focus on
        focus_areas: Optional list of regulatory areas to focus on
        report_type: Type of report to generate
    
    Returns:
        The generated compliance report
    """
    crew = create_policy_analysis_crew(
        document_focus=document_focus,
        focus_areas=focus_areas,
        report_type=report_type,
    )
    
    result = crew.kickoff()
    return result
