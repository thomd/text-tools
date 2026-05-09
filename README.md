# Text Tools

## `text`

Strips HTML, Markdown, and punctuation from text, leaving only plain words and numbers. Uses NLTK for tokenization.

### Requirements

- Python ≥ 3.13
- [uv](https://docs.astral.sh/uv/)

### Install

```bash
git clone https://github.com/thomd/text-tools
cd text-tools
uv tool install --python 3.13 .
```

### Usage

```bash
# Via pipe
cat document.html | text
echo "**Hello**, world!" | text

# Via flag
text -t "Some _marked up_ text."
```

### Tests

```bash
uv run --with pytest pytest tests/ -v
```
