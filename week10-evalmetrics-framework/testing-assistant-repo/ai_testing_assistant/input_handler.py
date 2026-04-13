"""Input handling for the AI Testing Assistant pipeline.

Resolves user input to raw requirement text and a file path.
Supports both file path input (.txt/.md) and raw text input.
"""

import os
from datetime import datetime
from pathlib import Path


def resolve_input(input_value: str, output_dir: str = "./output") -> tuple[str, str]:
    """Resolve input to (raw_text, file_path).

    If input_value is an existing file path (.txt or .md), read and return
    its contents along with the path. If input_value is raw text, write it
    to a timestamped file in output_dir and return the text and file path.

    Args:
        input_value: A file path or raw requirement text.
        output_dir: Directory for writing raw text to file. Defaults to "./output".

    Returns:
        A tuple of (raw_text, file_path).

    Raises:
        FileNotFoundError: If input_value looks like a file path but does not exist.
    """
    path = Path(input_value)

    # Check if it looks like a file path (has a .txt or .md extension)
    if path.suffix.lower() in (".txt", ".md"):
        if path.is_file():
            raw_text = path.read_text(encoding="utf-8")
            return raw_text, str(path)
        raise FileNotFoundError(
            f"Requirements file not found: {input_value}"
        )

    # It's raw text — write to a timestamped file in output_dir
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(output_dir) / f"requirements_{timestamp}.txt"
    file_path.write_text(input_value, encoding="utf-8")
    return input_value, str(file_path)
