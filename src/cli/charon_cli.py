#!/usr/bin/env python3
"""
Charon CLI - Your Personal Assistant Ferryman
Guiding you through the complexities of daily life with intelligent task orchestration.
"""

import sys
from pathlib import Path
from typing import Optional
import re

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box
from rich.align import Align

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.agents.big_boss_orchestrator_agent import BigBossOrchestratorAgent
from src.utils.charon_ascii_art import CHARON_ART_ASCII, THE_FARRYMANS_ASSISTANT_ASCII

# Initialize rich console and typer app
console = Console()
app = typer.Typer(
    name="charon",
    help="💀🛶  Charon - Your Personal Assistant Ferryman",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


class CharonCLI:
    def __init__(self):
        self.agent = None
        self.session_active = False

    def display_banner(self):
        """Display the mythological Charon-themed banner"""
        banner = Text()
        banner.append(CHARON_ART_ASCII, style="bold magenta")
        banner.append(THE_FARRYMANS_ASSISTANT_ASCII, style="magenta")
        banner.append("")

        subtitle = Text(
            "Guiding you across the river of daily complexities\n"
            "Your intelligent orchestrator for work, leisure, and life management",
            style="italic dim white",
        )

        panel = Panel(
            Align.center(Text.assemble(banner, "\n\n", subtitle)),
            title="⚡ [bold yellow]Welcome Aboard[/bold yellow] ⚡",
            border_style="dark_magenta",
            box=box.DOUBLE,
            padding=(1, 2),
        )

        console.print()
        console.print(panel)
        console.print()

    def display_capabilities(self):
        """Show what Charon can help with"""
        capabilities = Text.assemble(
            ("🔧 ", "yellow"),
            ("Work & Development: ", "bold yellow"),
            ("Project analysis, GitHub management, task scheduling\n", "white"),
            ("🎭 ", "cyan"),
            ("Leisure & Entertainment: ", "dim cyan"),
            ("Books, movies, YouTube, content curation\n", "white"),
            ("📅 ", "green"),
            ("Time Management: ", "bold green"),
            ("Calendar integration, availability checking\n", "white"),
            ("🧠 ", "blue"),
            ("Intelligent Routing: ", "bold blue"),
            ("Context-aware assistance across all life domains", "white"),
        )

        panel = Panel(
            capabilities,
            title="🌟 [bold white]My Capabilities[/bold white] 🌟",
            border_style="dim white",
            padding=(1, 1),
        )

        console.print(panel)
        console.print()

    def format_response(self, response_text: str) -> None:
        """Format and display agent responses with proper indentation for sub-agents"""

        # Check if this looks like a sub-agent call/response pattern
        if self._is_sub_agent_response(response_text):
            self._display_orchestrated_response(response_text)
        else:
            self._display_charon_response(response_text)

    def _is_sub_agent_response(self, text: str) -> bool:
        """Detect if the response contains sub-agent interactions"""
        sub_agent_indicators = [
            "task_agent_query",
            "home_agent_query",
            "file_search_agent",
            "calendar_agent",
            "github_agent",
            "book_agent",
            "movies_agent",
            "recommender_agent",
        ]
        return any(indicator in text.lower() for indicator in sub_agent_indicators)

    def _display_orchestrated_response(self, response_text: str):
        """Display response with clear separation between Charon and sub-agents"""

        # Main Charon response
        console.print("💀🛶 ", style="magenta", end="")
        console.print(
            "[magenta]Charon:[/magenta] Let me coordinate the right assistance for you..."
        )
        console.print()

        # Try to parse and format the response nicely
        lines = response_text.split("\n")
        in_sub_agent_section = False
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect agent mentions
            if any(
                agent in line.lower()
                for agent in [
                    "task agent",
                    "home agent",
                    "file search",
                    "calendar",
                    "github",
                    "book agent",
                    "movies agent",
                    "recommender",
                ]
            ):
                if not in_sub_agent_section:
                    console.print(
                        "   🔄 [dim yellow]Consulting specialized agents...[/dim yellow]"
                    )
                    console.print()
                    in_sub_agent_section = True

                # Determine which agent
                agent_name = self._extract_agent_name(line)
                if agent_name:
                    console.print(f"      🤖 [bold blue]{agent_name}:[/bold blue]")

            # Display the content with proper indentation
            if in_sub_agent_section:
                # Indent sub-agent responses
                formatted_line = self._format_line_content(line)
                if formatted_line:
                    console.print(f"         {formatted_line}")
            else:
                # Main Charon content
                formatted_line = self._format_line_content(line)
                if formatted_line:
                    console.print(f"   {formatted_line}")

        console.print()
        console.print(
            "💀🛶 [dark_magenta]Charon:[/dark_magenta] [italic]Your journey guidance is complete. What else may I assist you with?[/italic]"
        )

    def _display_charon_response(self, response_text: str):
        """Display a regular Charon response"""
        console.print("💀🛶 ", style="dark_magenta", end="")
        console.print("[dark_magenta]Charon:[/dark_magenta]", end=" ")

        # Format the response nicely
        formatted_text = self._format_response_text(response_text)
        console.print(formatted_text)

    def _extract_agent_name(self, line: str) -> Optional[str]:
        """Extract agent name from a line"""
        agents_map = {
            "task agent": "Task Agent",
            "home agent": "Home Agent",
            "file search": "File Search Agent",
            "calendar": "Calendar Agent",
            "github": "GitHub Agent",
            "book agent": "Books Agent",
            "movies agent": "Movies Agent",
            "recommender": "Recommender Agent",
        }

        line_lower = line.lower()
        for key, name in agents_map.items():
            if key in line_lower:
                return name
        return None

    def _format_line_content(self, line: str) -> str:
        """Format a line with basic styling"""
        if not line:
            return ""

        # Remove common prefixes that aren't needed in display
        line = re.sub(
            r"^(Agent Response:|Response from|Task Agent|Home Agent):\s*", "", line
        )

        # Add some basic formatting
        if line.startswith("✅") or line.startswith("✓"):
            return f"[green]{line}[/green]"
        elif line.startswith("❌") or line.startswith("✗"):
            return f"[red]{line}[/red]"
        elif line.startswith("⚠️") or line.startswith("Warning"):
            return f"[yellow]{line}[/yellow]"
        elif "**" in line:
            # Handle bold markdown
            line = re.sub(r"\*\*(.*?)\*\*", r"[bold]\1[/bold]", line)

        return line

    def _format_response_text(self, text: str) -> str:
        """Apply general formatting to response text"""
        # Handle basic markdown-style formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"[bold]\1[/bold]", text)
        text = re.sub(r"\*(.*?)\*", r"[italic]\1[/italic]", text)

        return text

    def get_user_input(self) -> str:
        """Get styled user input"""
        console.print()
        return Prompt.ask("[bold white]🗣️  You", console=console)

    def display_goodbye(self):
        """Display farewell message"""
        farewell = Panel(
            Align.center(
                Text.assemble(
                    ("💀🛶 ", "dark_magenta"),
                    ("Safe travels, voyager!", "bold dark_magenta"),
                    (
                        "\n\nMay your tasks be swift and your leisure fulfilling.\n",
                        "italic dim white",
                    ),
                    ("Until we meet again across the digital river...", "dark_magenta"),
                )
            ),
            title="⚡ [bold yellow]Farewell[/bold yellow] ⚡",
            border_style="dark_magenta",
            box=box.DOUBLE,
        )
        console.print()
        console.print(farewell)
        console.print()


@app.command()
def chat(
    intro: bool = typer.Option(
        True, "--intro/--no-intro", "-i/-n", help="Show intro banner"
    ),
):
    """
    🚣 Start an interactive chat session with Charon, your personal assistant ferryman.

    Charon will help you navigate through:
    • Work tasks and development projects
    • Personal leisure and entertainment
    • Calendar management and scheduling
    • Intelligent routing between specialized assistants
    """

    cli = CharonCLI()

    try:
        # Initialize the agent
        with console.status(
            "[bold dark_magenta]Preparing the ferry...", spinner="dots"
        ):
            cli.agent = BigBossOrchestratorAgent()

        # Show intro if requested
        if intro:
            cli.display_banner()
            cli.display_capabilities()

        # Show ready message
        console.print(
            "💀🛶 [bold dark_magenta]Charon:[/bold dark_magenta] [italic]Welcome aboard, traveler! I'm here to guide you through your digital journey.[/italic]"
        )
        console.print(
            "     [dim white]Type 'exit', 'quit', or 'farewell' to end our session.[/dim white]"
        )

        cli.session_active = True

        # Main interaction loop
        while cli.session_active:
            try:
                # Get user input
                user_input = cli.get_user_input()

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "farewell", "bye", "goodbye"]:
                    break

                # Process the request
                with console.status(
                    "[bold dark_magenta]Navigating your request...",
                    spinner="bouncingBar",
                ):
                    response = cli.agent.query(user_input)

                # Display the response
                console.print()
                cli.format_response(str(response))

            except KeyboardInterrupt:
                console.print("\n\n[yellow]⚠️  Journey interrupted by user[/yellow]")
                break
            except Exception as e:
                console.print(f"\n[red]❌ Error during navigation: {str(e)}[/red]")
                console.print(
                    "[dim]The ferry encountered rough waters, but we can continue...[/dim]"
                )

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Ferry preparation interrupted[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Failed to prepare the ferry: {str(e)}[/red]")
        raise typer.Exit(1)

    finally:
        # Show goodbye message
        cli.display_goodbye()


@app.command()
def quick(query: str = typer.Argument(..., help="Your question or request for Charon")):
    """
    🚀 Ask Charon a quick question without starting an interactive session.

    Example: charon quick "What should I read tonight?"
    """

    try:
        # Initialize agent quietly
        with console.status("[bold dark_magenta]Summoning Charon...", spinner="dots"):
            agent = BigBossOrchestratorAgent()

        # Process the request
        with console.status(
            "[bold dark_magenta]Navigating your request...", spinner="bouncingBar"
        ):
            response = agent.query(query)

        # Display minimal response
        console.print()
        console.print("💀🛶 [bold dark_magenta]Charon:[/bold dark_magenta]")
        console.print(f"   {response}")
        console.print()

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Request interrupted[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Navigation failed: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def status():
    """
    📊 Check Charon's operational status and available agents.
    """

    console.print()
    console.print("💀🛶 [bold dark_magenta]Charon System Status[/bold dark_magenta]")
    console.print()

    status_info = Text.assemble(
        ("🔧 ", "green"),
        ("Task Agent: ", "bold"),
        ("Ready for work & development tasks\n", "green"),
        ("🎭 ", "green"),
        ("Home Agent: ", "bold"),
        ("Ready for leisure & entertainment\n", "green"),
        ("📅 ", "green"),
        ("Calendar Integration: ", "bold"),
        ("Connected to Google Calendar\n", "green"),
        ("🌐 ", "green"),
        ("GitHub Integration: ", "bold"),
        ("Connected to repositories\n", "green"),
        ("🔍 ", "green"),
        ("File Search: ", "bold"),
        ("Ready for project analysis\n", "green"),
        ("📚 ", "green"),
        ("Content Curation: ", "bold"),
        ("Books, movies, YouTube ready\n", "green"),
    )

    panel = Panel(
        status_info,
        title="⚡ [bold green]All Systems Operational[/bold green] ⚡",
        border_style="green",
    )

    console.print(panel)
    console.print()


if __name__ == "__main__":
    app()
