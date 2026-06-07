"""Input validation and prompting utilities for SkyNet console application.

Provides functions to prompt users for input with validation, re-prompting
on invalid entries. Supports integer, float, string, IATA code, and
priority level inputs.
"""


def get_int_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Prompt for an integer input, validating optional range constraints.

    Re-prompts the user on invalid (non-numeric or out-of-range) input
    with a descriptive error message showing the expected range.

    Args:
        prompt: The prompt message to display to the user.
        min_val: Optional minimum allowed value (inclusive).
        max_val: Optional maximum allowed value (inclusive).

    Returns:
        A valid integer within the specified range.
    """
    while True:
        try:
            value = int(input(prompt))
        except (ValueError, TypeError):
            range_msg = _format_range_msg(min_val, max_val)
            print(f"  Error: Please enter a valid integer{range_msg}.")
            continue

        if min_val is not None and value < min_val:
            print(f"  Error: Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"  Error: Value must be at most {max_val}.")
            continue

        return value


def get_float_input(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Prompt for a float input, validating optional range constraints.

    Re-prompts the user on invalid (non-numeric or out-of-range) input
    with a descriptive error message.

    Args:
        prompt: The prompt message to display to the user.
        min_val: Optional minimum allowed value (inclusive).
        max_val: Optional maximum allowed value (inclusive).

    Returns:
        A valid float within the specified range.
    """
    while True:
        try:
            value = float(input(prompt))
        except (ValueError, TypeError):
            range_msg = _format_range_msg(min_val, max_val)
            print(f"  Error: Please enter a valid number{range_msg}.")
            continue

        if min_val is not None and value < min_val:
            print(f"  Error: Value must be at least {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"  Error: Value must be at most {max_val}.")
            continue

        return value


def get_string_input(prompt: str) -> str:
    """Prompt for a non-empty string input.

    Re-prompts if the user enters an empty string or whitespace-only input.

    Args:
        prompt: The prompt message to display to the user.

    Returns:
        A non-empty, stripped string.
    """
    while True:
        value = input(prompt).strip()
        if not value:
            print("  Error: Input cannot be empty. Please try again.")
            continue
        return value


def get_iata_input(prompt: str) -> str:
    """Prompt for a valid IATA code (exactly 3 uppercase alphabetic characters).

    Automatically converts input to uppercase. Re-prompts on invalid format.

    Args:
        prompt: The prompt message to display to the user.

    Returns:
        A valid 3-character uppercase IATA code.
    """
    while True:
        value = input(prompt).strip().upper()
        if len(value) == 3 and value.isalpha():
            return value
        print("  Error: IATA code must be exactly 3 alphabetic characters (e.g., LHR, JFK).")


def get_priority_input(prompt: str) -> str:
    """Prompt for a valid priority level string.

    Accepts Platinum, Gold, Silver, or Economy (case-insensitive).
    Re-prompts on invalid input.

    Args:
        prompt: The prompt message to display to the user.

    Returns:
        A valid priority level string (capitalized form).
    """
    valid_levels = {"platinum", "gold", "silver", "economy"}
    while True:
        value = input(prompt).strip().lower()
        if value in valid_levels:
            return value.capitalize()
        print("  Error: Priority must be one of: Platinum, Gold, Silver, Economy.")


def _format_range_msg(min_val, max_val) -> str:
    """Build a range description string for error messages.

    Args:
        min_val: Optional minimum value.
        max_val: Optional maximum value.

    Returns:
        A string describing the valid range, or empty string if no constraints.
    """
    if min_val is not None and max_val is not None:
        return f" between {min_val} and {max_val}"
    elif min_val is not None:
        return f" (minimum {min_val})"
    elif max_val is not None:
        return f" (maximum {max_val})"
    return ""
