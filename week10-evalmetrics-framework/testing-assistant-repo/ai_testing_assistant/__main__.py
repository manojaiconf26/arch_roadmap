"""CLI entry point for the AI Testing Assistant pipeline.

Usage:
    python -m ai_testing_assistant <file_path_or_raw_text>

Accepts a file path (.txt or .md) or raw requirement text as a positional
argument, runs the full pipeline, and prints the result as formatted JSON.
"""

import argparse
import json
import sys
from dataclasses import asdict

from ai_testing_assistant.observability import configure_logging
from ai_testing_assistant.orchestrator import run_pipeline


def main() -> None:
    """Parse CLI arguments, run the pipeline, and print the result."""
    parser = argparse.ArgumentParser(
        description="AI Testing Assistant — multi-agent pipeline for software testing",
    )
    parser.add_argument(
        "input",
        help="A file path (.txt/.md) or raw requirement text",
    )
    args = parser.parse_args()

    configure_logging()

    try:
        result = run_pipeline(args.input)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
