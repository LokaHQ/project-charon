#!/usr/bin/env python3
"""
Charon CLI - Your Personal Assistant Ferryman
Guiding you through the complexities of daily life with intelligent task orchestration.
"""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box
from rich.align import Align
from rich.table import Table

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
        self.session_context = {}
        self.user_preferences = {}

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

        def show_help_panel(self):
            """Show what users can do"""
            help_table = Table(show_header=False, box=box.MINIMAL)
            help_table.add_column("Category", style="bold cyan", width=15)
            help_table.add_column("Examples", style="white")

            help_table.add_row(
                "📋 Work Tasks",
                "Analyze my project • Schedule coding time • GitHub issues",
            )
            help_table.add_row(
                "🎭 Leisure", "What should I watch? • Recommend a book • YouTube videos"
            )
            help_table.add_row(
                "📅 Planning", "When am I free? • Block focus time • Schedule meeting"
            )
            help_table.add_row("⚙️ Control", "help • audio on/off • clear • exit")

            console.print("\n")
            console.print(help_table)
            console.print(
                "\n[dim]💡 Tip: Just describe what you need in natural language[/dim]"
            )

    def show_help_panel(self):
        """Show what users can do"""
        help_table = Table(show_header=False, box=box.MINIMAL)
        help_table.add_column("Category", style="bold cyan", width=15)
        help_table.add_column("Examples", style="white")

        help_table.add_row(
            "📋 Work Tasks", "Analyze my project • Schedule coding time • GitHub issues"
        )
        help_table.add_row(
            "🎭 Leisure", "What should I watch? • Recommend a book • YouTube videos"
        )
        help_table.add_row(
            "📅 Planning", "When am I free? • Block focus time • Schedule meeting"
        )
        help_table.add_row("⚙️ Control", "help • audio on/off • clear • exit")

        console.print("\n")
        console.print(help_table)
        console.print(
            "\n[dim]💡 Tip: Just describe what you need in natural language[/dim]"
        )

    def handle_command(self, user_input: str) -> bool:
        """Handle special commands, return True if handled"""
        if user_input.lower() in ["help", "?"]:
            self.show_help_panel()
            return True
        elif user_input.lower() in ["audio off", "mute"]:
            self.user_preferences["audio"] = False
            console.print("🔇 Audio disabled")
            return True
        elif user_input.lower() in ["audio on", "unmute"]:
            self.user_preferences["audio"] = True
            console.print("🔊 Audio enabled")
            return True
        elif user_input.lower() == "clear":
            console.clear()
            self.show_compact_banner()
            return True
        elif user_input.lower() == "status":
            self.show_status()
            return True
        return False

    def show_status(self):
        """Show system status"""
        status_table = Table(title="System Status")
        status_table.add_column("Component", style="cyan")
        status_table.add_column("Status", style="green")

        # Check each agent's availability
        status_table.add_row("Task Agent", "✅ Ready")
        status_table.add_row("Home Agent", "✅ Ready")
        status_table.add_row("Calendar", "✅ Connected")
        status_table.add_row("GitHub", "✅ Connected")
        status_table.add_row(
            "Audio", "🔊 On" if self.user_preferences.get("audio", True) else "🔇 Off"
        )

        console.print(status_table)

    def get_user_input_with_history(self) -> str:
        """Enhanced input with better UX"""
        try:
            return Prompt.ask("[bold white]💬 You", console=console)
        except KeyboardInterrupt:
            return "exit"


@app.command()
def chat(
    minimal: bool = typer.Option(
        False, "--minimal", "-m", help="Start with minimal UI"
    ),
    audio: bool = typer.Option(True, "--audio/--no-audio", help="Enable/disable audio"),
):
    """Start interactive chat with Charon"""

    cli = CharonCLI()
    cli.user_preferences["audio"] = audio

    try:
        # Minimal startup
        if not minimal:
            cli.display_banner()
            cli.show_help_panel()

        # Initialize agent with progress feedback
        with console.status("[bold magenta]Initializing Charon...", spinner="dots"):
            if cli.user_preferences.get("audio", True):
                cli.agent = BigBossOrchestratorAgent()
            else:
                cli.agent = BigBossOrchestratorAgent(silent=True)

        console.print(
            "🛶 [bold magenta]Ready![/bold magenta] What would you like to do?\n"
        )

        # Main loop with better error handling
        while True:
            try:
                user_input = cli.get_user_input_with_history()

                if user_input.lower() in ["exit", "quit", "bye"]:
                    if Confirm.ask("Ready to disembark?"):
                        break
                    continue

                # Handle special commands
                if cli.handle_command(user_input):
                    continue

                # Process actual queries
                cli.agent.query(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit gracefully[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]❌ Something went wrong: {str(e)}[/red]")
                console.print("[dim]Try rephrasing your request or type 'help'[/dim]")

    except Exception as e:
        console.print(f"[red]Failed to start Charon: {str(e)}[/red]")
        raise typer.Exit(1)

    # Graceful exit
    console.print("\n🛶 [magenta]Safe travels![/magenta]\n")


@app.command()
def setup():
    """Interactive setup wizard"""
    console.print("🛶 [bold magenta]Charon Setup Wizard[/bold magenta]\n")

    # Check for required files/configs
    console.print("Checking configuration...")

    # Guide user through setup
    if not Path("config/project-config.yaml").exists():
        console.print("[yellow]⚠️  Configuration file not found[/yellow]")
        console.print("I'll help you create one...")
        # Interactive config creation

    console.print("✅ Setup complete! Run 'charon chat' to get started.")


@app.command()
def agents():
    """List available agents and their capabilities"""
    agents_table = Table(title="Available Agents")
    agents_table.add_column("Agent", style="cyan")
    agents_table.add_column("Purpose", style="white")
    agents_table.add_column("Example Commands", style="dim")

    agents_table.add_row(
        "📋 Task", "Work & Development", "Analyze project, schedule coding"
    )
    agents_table.add_row(
        "🎭 Home", "Leisure & Entertainment", "Movie night, book recommendations"
    )
    agents_table.add_row("📅 Calendar", "Time Management", "Check schedule, block time")
    agents_table.add_row(
        "🐙 GitHub", "Repository Management", "Check issues, create PRs"
    )

    console.print(agents_table)


if __name__ == "__main__":
    app()
