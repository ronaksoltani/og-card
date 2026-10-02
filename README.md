# OG Card Studio

Generate a clean 1200×630 Open Graph card from a title, author, and category. The image is rendered locally with Pillow; no design service or network request is needed.

## Quick start

```bash
python -m venv .venv
python -m pip install -e .
og-card "Build better Python habits" --author "Ronak Soltani" --category "LEARNING" --output build/card.png
```

The renderer uses an installed font when one is available and has a portable fallback. `--font` accepts a `.ttf` or `.otf` file. Long titles are wrapped and the type size is reduced to keep them inside the card.

## Learning notes

The project practices command-line parsing, image drawing, font measurement, and pure helper functions. `create_card` returns a `Path`, so the same rendering code can later power a web API.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See [LICENSE](LICENSE).
