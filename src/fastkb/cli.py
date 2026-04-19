import sys

from .parser import build_parser
from .settings import config
from . import commands


def main():
    parser = build_parser()
    args = parser.parse_args()

    config.configure(
        memory=getattr(
            args,
            "memory",
            False,
        ),
        limit=getattr(
            args,
            "limit",
            5,
        ),
    )

    try:
        handler = getattr(
            commands,
            f"handle_{args.command}",
        )
        handler(args)
    except Exception as exception:
        print(f"\nError: {exception}")
        sys.exit(1)
