from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box # Import the box module!
import time

console = Console()

# --- Common Header Text ---
COMMON_HEADER_CONTENT = {
    "title": "Rich Border Styles Demo",
    "messages": [
        "This content remains the same,",
        "but watch how the bjjjjjjjjjjjjjjjjjjjjjjjjjjjorder changes!",
        "Each style has its own unique feel."
    ]
}

# --- Different Border Type Configurations ---
BORDER_TYPE_DEMOS = {
    "Standard Box (Blue)": {
        "box_type": box.SQUARE,
        "border_style": "blue",
        "title_style": "bold cyan",
        "message_style": "white"
    },
    "Rounded Box (Green)": {
        "box_type": box.ROUNDED,
        "border_style": "green",
        "title_style": "bold lime",
        "message_style": "light_green"
    },
    "Double Line Box (Magenta)": {
        "box_type": box.DOUBLE,
        "border_style": "magenta",
        "title_style": "bold magenta",
        "message_style": "bright_white"
    },
    "Heavy Line Box (Yellow)": {
        "box_type": box.HEAVY,
        "border_style": "yellow",
        "title_style": "bold gold",
        "message_style": "yellow3"
    },
    "ASCII Box (Red)": {
        "box_type": box.ASCII,
        "border_style": "red",
        "title_style": "bold red",
        "message_style": "white"
    },
    "Simple Box (Cyan)": {
        "box_type": box.SIMPLE,
        "border_style": "cyan",
        "title_style": "bold cyan",
        "message_style": "white"
    },
    "Minimal Box (Grey)": {
        "box_type": box.MINIMAL,
        "border_style": "dim grey35",
        "title_style": "bold grey82",
        "message_style": "grey70"
    },
    "ROUNDED (Orange)": {
        "box_type": box.ROUNDED, # Only shows top and bottom lines
        "border_style": "orange1",
        "title_style": "bold orange_red1",
        "message_style": "dark_orange3"
    },
    "No Border (White)": { # Example of removing the border entirely
        "box_type": box.SQUARE_DOUBLE_HEAD, # Set box_type to None
        "border_style": "white", # This style will still apply to title/messages
        "title_style": "bold white on black",
        "message_style": "dim white"
    }
}

def display_border_demo(name, config):
    """
    Displays a header with common content, applying the specified box type and styles.
    """
    console.print(f"\n[bold underline]{name}[/bold underline]\n", justify="center")

    inner_content_block = Text()
    inner_content_block.append(COMMON_HEADER_CONTENT["title"], style=config["title_style"])
    inner_content_block.append("\n\n") # Double newline for spacing

    for i, msg in enumerate(COMMON_HEADER_CONTENT["messages"]):
        inner_content_block.append(msg, style=config["message_style"])
        if i < len(COMMON_HEADER_CONTENT["messages"]) - 1:
            inner_content_block.append("\n")

    # The key change: passing 'box_type' to the Panel constructor
    console.print(
        Panel(
            Align.center(inner_content_block),
            width=60, # Keep width consistent for comparison
            box=config["box_type"], # <--- This is where the magic happens!
            border_style=config["border_style"],
            padding=(1, 2),
            expand=False
        )
    )
    console.print("\n")


# --- Main Execution ---
if __name__ == "__main__":
    console.clear()
    console.print("[bold green]--- Rich Border Type Showcase ---[/bold green]\n", justify="center")
    console.print("[dim]Observe how the actual border characters change, not just their color.[/dim]\n")
    time.sleep(2)

    for name, config in BORDER_TYPE_DEMOS.items():
        display_border_demo(name, config)
        time.sleep(3) # Give more time to observe the border differences

    console.print("[bold green]--- End of Border Showcase ---[/bold green]\n", justify="center")
    console.input("[yellow]Press Enter to exit.[/yellow]")
