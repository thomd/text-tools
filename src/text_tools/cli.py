import sys
import re
import argparse
from html.parser import HTMLParser
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize


def _ensure_nltk_data():
    for pkg in ("punkt_tab", "punkt"):
        try:
            nltk.data.find(f"tokenizers/{pkg}")
            return
        except LookupError:
            pass
    nltk.download("punkt_tab", quiet=True)


class _HTMLStripper(HTMLParser):
    _SKIP_TAGS = {"script", "style"}

    def __init__(self):
        super().__init__()
        self._parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self._SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag.lower() in self._SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)

    def handle_data(self, data):
        if self._skip_depth == 0:
            self._parts.append(data)

    def get_text(self):
        return " ".join(self._parts)


def strip_html(text):
    s = _HTMLStripper()
    s.feed(text)
    return s.get_text()


def strip_markdown(text):
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]*)\]\(.*?\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}([^*\n]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_\n]+)_{1,3}", r"\1", text)
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    return text


def process(text):
    text = strip_html(text)
    text = strip_markdown(text)
    sentences = sent_tokenize(text)
    clean = []
    for sent in sentences:
        tokens = word_tokenize(sent)
        words = [t for t in tokens if t.isalpha() or t.isnumeric()]
        if words:
            clean.append(" ".join(words))
    return "\n".join(clean)


def main():
    _ensure_nltk_data()
    parser = argparse.ArgumentParser(
        description="Strip HTML, Markdown, and punctuation — output plain text only."
    )
    parser.add_argument("-t", "--text", help="Input text (default: read from stdin)")
    parser.add_argument("-i", action="store_true", help="Lowercase output")
    parser.add_argument("-u", action="store_true", help="Output unique words, one per line")
    args = parser.parse_args()

    if args.text:
        raw = args.text
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    result = process(raw)
    if args.i:
        result = result.lower()
    if args.u:
        words = sorted(set(result.split()))
        result = "\n".join(words)
    print(result)


if __name__ == "__main__":
    main()
