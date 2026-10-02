from PIL import ImageFont

from og_card.render import HEIGHT, WIDTH, wrap_text


def test_wrap_text_keeps_words_and_respects_width():
    font = ImageFont.load_default()
    lines = wrap_text("small clear words for a card", font, 80)
    assert len(lines) > 1
    assert " ".join(lines) == "small clear words for a card"


def test_dimensions_are_standard():
    assert (WIDTH, HEIGHT) == (1200, 630)
