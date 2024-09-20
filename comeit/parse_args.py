import argparse
from dataclasses import dataclass
from pathlib import Path

from comeit import LogLevel


@dataclass
class ConfigArgs(argparse.Namespace):
    config_file: str
    log_level: LogLevel


def parse_args():
    parser = argparse.ArgumentParser(description="Process a configuration file.")

    parser.add_argument(
        "--config-file",
        type=Path,
        help="Path to the configuration file. This file can override the default severity levels "
        "of rules.",
    )

    parser.add_argument(
        "--log-level",
        type=LogLevel.from_string,
        choices=list(LogLevel),
        default=LogLevel.WARNING,
        help="Set the logging level. Defaults to WARNING.",
    )

    return parser.parse_args(namespace=ConfigArgs)
