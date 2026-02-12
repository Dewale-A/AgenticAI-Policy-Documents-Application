#!/usr/bin/env python3
"""
Policy Documents Agentic AI Application

An autonomous multi-agent system for ingesting, analyzing, and reporting
on policy documents for compliance assessment.

Usage:
    python main.py [options]

Options:
    --focus TOPIC       Focus analysis on specific topic or document
    --areas AREAS       Comma-separated list of focus areas (e.g., "GDPR,SOX")
    --report TYPE       Report type: executive, detailed, or full (default: full)
    --pdf               Export report to PDF
    --telegram          Send report to Telegram
    --email             Send report via email
    --help              Show this help message
"""

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crew import run_policy_analysis
from src.config.settings import POLICY_DOCS_DIR, OUTPUT_DIR


console = Console()


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║       🔍 Policy Documents Agentic AI Application 🔍              ║
║                                                                   ║
║   Autonomous Multi-Agent System for Compliance Analysis           ║
║   Built with CrewAI | Powered by OpenAI/Anthropic                ║
╚══════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold blue")


def check_prerequisites():
    """Check that prerequisites are met."""
    issues = []
    
    # Check for policy documents
    docs = list(POLICY_DOCS_DIR.glob("*.*"))
    if not docs:
        issues.append(f"No policy documents found in {POLICY_DOCS_DIR}")
        issues.append("  → Add PDF, DOCX, TXT, or MD files to analyze")
    
    # Check for API keys
    from src.config.settings import OPENAI_API_KEY, ANTHROPIC_API_KEY
    if not OPENAI_API_KEY and not ANTHROPIC_API_KEY:
        issues.append("No LLM API key configured")
        issues.append("  → Copy .env.example to .env and add your API key")
    
    if issues:
        console.print("\n[yellow]⚠️  Prerequisites Check:[/yellow]")
        for issue in issues:
            console.print(f"  {issue}")
        console.print()
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Policy Documents Agentic AI - Compliance Analysis System"
    )
    parser.add_argument(
        "--focus",
        type=str,
        help="Focus analysis on specific topic or document",
    )
    parser.add_argument(
        "--areas",
        type=str,
        help="Comma-separated list of focus areas (e.g., 'GDPR,SOX,data governance')",
    )
    parser.add_argument(
        "--report",
        type=str,
        choices=["executive", "detailed", "full"],
        default="full",
        help="Type of report to generate (default: full)",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Export report to PDF format",
    )
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="Send report to Telegram (requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env)",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Send report via email (requires SMTP settings in .env)",
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check prerequisites
    if not check_prerequisites():
        console.print("[red]Please resolve the above issues before running.[/red]")
        sys.exit(1)
    
    # Parse focus areas if provided
    focus_areas = None
    if args.areas:
        focus_areas = [area.strip() for area in args.areas.split(",")]
    
    # Display configuration
    console.print(Panel(
        f"""
[bold]Configuration:[/bold]
• Policy Documents: {POLICY_DOCS_DIR}
• Output Directory: {OUTPUT_DIR}
• Document Focus: {args.focus or 'All documents'}
• Focus Areas: {', '.join(focus_areas) if focus_areas else 'All areas'}
• Report Type: {args.report}
        """,
        title="🚀 Starting Analysis",
        border_style="green",
    ))
    
    try:
        # Run the analysis
        console.print("\n[bold]Initializing agents...[/bold]\n")
        result = run_policy_analysis(
            document_focus=args.focus,
            focus_areas=focus_areas,
            report_type=args.report,
        )
        
        # Display results
        console.print("\n")
        console.print(Panel(
            Markdown(str(result)),
            title="📋 Compliance Analysis Report",
            border_style="green",
        ))
        
        console.print(f"\n[green]✅ Report saved to {OUTPUT_DIR}/compliance_report.md[/green]")
        
        # Handle PDF export
        if args.pdf or args.telegram or args.email:
            try:
                from src.utils.export import export_to_pdf, send_to_telegram, send_to_email
                
                console.print("\n[bold]Converting to PDF...[/bold]")
                pdf_path = export_to_pdf()
                console.print(f"[green]✅ PDF saved to {pdf_path}[/green]")
                
                # Send to Telegram
                if args.telegram:
                    console.print("\n[bold]Sending to Telegram...[/bold]")
                    send_to_telegram(pdf_path)
                
                # Send via email
                if args.email:
                    console.print("\n[bold]Sending via email...[/bold]")
                    send_to_email(pdf_path)
                    
            except ImportError as e:
                console.print(f"\n[yellow]⚠️ Export dependencies missing: {e}[/yellow]")
            except Exception as e:
                console.print(f"\n[red]❌ Export/send failed: {e}[/red]")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error during analysis: {e}[/red]")
        raise


if __name__ == "__main__":
    main()
