"""Output formatting utility functions for SkyNet.

All formatters produce human-readable strings with no side effects.
"""


def format_path(nodes: list, total_distance: int) -> str:
    """Format a flight path as a readable string.

    Args:
        nodes: Ordered list of IATA codes representing the path.
        total_distance: Total distance of the path in kilometers.

    Returns:
        A formatted string like "A -> B -> C (1234 km)".
    """
    if not nodes:
        return "(empty path)"
    path_str = " -> ".join(str(node) for node in nodes)
    return f"{path_str} ({total_distance} km)"


def format_table(headers: list, rows: list) -> str:
    """Format data as a simple ASCII table.

    Args:
        headers: List of column header strings.
        rows: List of row lists, where each row has one value per header.

    Returns:
        A formatted ASCII table string with aligned columns.
    """
    if not headers:
        return ""

    # Convert all values to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    col_widths = [len(h) for h in str_headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))

    # Build the header line
    header_line = " | ".join(
        str_headers[i].ljust(col_widths[i]) for i in range(len(str_headers))
    )

    # Build the separator line
    separator = "-+-".join("-" * col_widths[i] for i in range(len(str_headers)))

    # Build data rows
    data_lines = []
    for row in str_rows:
        cells = []
        for i in range(len(str_headers)):
            cell = row[i] if i < len(row) else ""
            cells.append(cell.ljust(col_widths[i]))
        data_lines.append(" | ".join(cells))

    # Combine all parts
    lines = [header_line, separator] + data_lines
    return "\n".join(lines)


def format_mst_result(edges: list, total_cost: int) -> str:
    """Format MST computation result as a readable string.

    Args:
        edges: List of (source, destination, weight) tuples representing MST edges.
        total_cost: Total cost of the MST.

    Returns:
        A formatted string showing each MST edge and the total cost.
    """
    if not edges:
        return f"MST: (no edges)\nTotal Cost: {total_cost} km"

    lines = ["MST Edges:"]
    for src, dest, weight in edges:
        lines.append(f"  {src} -- {dest} (weight: {weight})")
    lines.append(f"Total Cost: {total_cost} km")
    return "\n".join(lines)


def format_separator(char: str = "=", length: int = 50) -> str:
    """Return a separator line composed of a repeated character.

    Args:
        char: The character to repeat. Defaults to '='.
        length: The total length of the separator. Defaults to 50.

    Returns:
        A string of the given character repeated to the specified length.
    """
    return char * length
