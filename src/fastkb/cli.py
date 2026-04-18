import sys
from .parser import build_parser
from . import commands


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        handler = getattr(commands, f"handle_{args.command}")
        handler(args)
    except Exception as exception:
        print(f"\nError: {exception}")
        sys.exit(1)
