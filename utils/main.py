import argparse
import subprocess


class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    PURPLE = "\033[95m"
    RED = "\033[91m"
    END = "\033[0m"


def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--rules", action="store_true",
        help="Get solution for optimized rules count instead of steps",
    )
    parser.add_argument(
        "-s", "--stats", action="store_true",
        help="See solution's statistics",
    )
    parser.add_argument(
        "-t", "--test",
        help="Test solution with the given input",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="See tape steps (only useful with -t)",
    )
    return parser.parse_args()


def get_clipboard_data() -> str:
    p = subprocess.Popen(["xclip","-selection", "clipboard", "-o"], stdout=subprocess.PIPE)
    retcode = p.wait()
    if retcode:
        raise ValueError(f"Something went wrong. Return code: {retcode}")
    data = p.stdout.read()
    return data.decode()


def set_clipboard_data(data: str) -> None:
    p = subprocess.Popen(["xclip","-selection","clipboard"], stdin=subprocess.PIPE)
    p.stdin.write(data.encode())
    p.stdin.close()
    retcode = p.wait()
    if retcode:
        raise ValueError(f"Something went wrong. Return code: {retcode}")
