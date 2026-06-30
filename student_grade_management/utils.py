"""
utils.py
--------
Helper / utility functions for the CLI interface.
Demonstrates: standalone Functions as a required OOP feature.
"""


def get_float_input(prompt: str, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Prompt the user for a float within [min_val, max_val]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if min_val <= value <= max_val:
                return value
            print(f"  ⚠  Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  ⚠  Invalid input. Please enter a numeric value.")


def get_non_empty_input(prompt: str) -> str:
    """Prompt until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ⚠  Input cannot be empty.")


def get_menu_choice(prompt: str, valid_choices: list[str]) -> str:
    """Prompt until the user picks a valid menu option."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"  ⚠  Invalid choice. Options: {', '.join(valid_choices)}")


def format_score_bar(score: float, width: int = 20) -> str:
    """Return a simple ASCII progress bar for a score out of 100."""
    filled = int((score / 100) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score:.1f}%"


def clear_screen() -> None:
    """Print blank lines to simulate clearing the terminal."""
    print("\n" * 3)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    width = 48
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)
