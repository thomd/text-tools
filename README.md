# Text Tools

## `text`

Strips HTML, Markdown, and punctuation from text, leaving only plain words and numbers. Uses NLTK for tokenization.

### Install

```bash
git clone https://github.com/thomd/text-tools
cd text-tools
uv tool install --python 3.13 .
```

### Update

```bash
git pull
uv tool upgrade text-tools
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
