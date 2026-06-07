"""Input validation utility functions for SkyNet.

All validators return booleans and never raise exceptions.
"""


def validate_iata_code(code: str) -> bool:
    """Validate that code is exactly 3 uppercase alphabetic characters.

    Args:
        code: The IATA code string to validate.

    Returns:
        True if the code is exactly 3 uppercase alpha characters, False otherwise.
    """
    if not isinstance(code, str):
        return False
    return len(code) == 3 and code.isalpha() and code.isupper()


def validate_pnr(pnr: str) -> bool:
    """Validate that PNR is a non-empty alphanumeric string.

    Args:
        pnr: The Passenger Name Record string to validate.

    Returns:
        True if the PNR is non-empty and contains only alphanumeric characters.
    """
    if not isinstance(pnr, str):
        return False
    return len(pnr) > 0 and pnr.isalnum()


def validate_priority_level(level: str) -> bool:
    """Validate that level is one of Platinum, Gold, Silver, or Economy (case-insensitive).

    Args:
        level: The priority level string to validate.

    Returns:
        True if the level is a valid priority level (case-insensitive).
    """
    if not isinstance(level, str):
        return False
    valid_levels = {"platinum", "gold", "silver", "economy"}
    return level.strip().lower() in valid_levels


def validate_numeric_range(value, min_val, max_val) -> bool:
    """Validate that value is within the inclusive range [min_val, max_val].

    Args:
        value: The numeric value to check.
        min_val: The minimum allowed value (inclusive).
        max_val: The maximum allowed value (inclusive).

    Returns:
        True if min_val <= value <= max_val, False otherwise.
    """
    try:
        return min_val <= value <= max_val
    except (TypeError, ValueError):
        return False


def validate_non_empty_string(text: str) -> bool:
    """Validate that text is a non-empty, non-whitespace-only string.

    Args:
        text: The string to validate.

    Returns:
        True if the string is non-empty and contains at least one non-whitespace character.
    """
    if not isinstance(text, str):
        return False
    return len(text.strip()) > 0
