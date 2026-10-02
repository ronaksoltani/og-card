import argparse
from pathlib import Path

from .render import create_card


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a 1200x630 social preview card.")
    parser.add_argument("title")
    parser.add_argument("--author", default="Author")
    parser.add_argument("--category", default="ARTICLE")
    parser.add_argument("--output", type=Path, default=Path("og-card.png"))
    parser.add_argument("--font", type=Path)
    args = parser.parse_args(argv)
    try:
        path = create_card(args.title, args.author, args.category, args.output, args.font)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Created {path} ({1200}x{630})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
