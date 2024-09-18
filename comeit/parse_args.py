import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConfigArgs(argparse.Namespace):
    config_file: str


def parse_args():
    parser = argparse.ArgumentParser(description="Process a configuration file.")

    # Define the --config-file argument
    parser.add_argument(
        "--config-file",
        type=Path,
        help="Path to the configuration file. This file can override the default severity levels"
        "of rules.",
    )

    return parser.parse_args(namespace=ConfigArgs)


if __name__ == "__main__":
    args = parse_args()
    # Access the dataclass attributes
    print(f"Config file path: {args.config_file}")
