import subprocess
import sys

import pytest

from text_tools.cli import _ensure_nltk_data, process, strip_html, strip_markdown

_ensure_nltk_data()


# ── strip_html ────────────────────────────────────────────────────────────────

def test_strip_html_removes_basic_tags():
    assert "hello" in strip_html("<b>hello</b>")

def test_strip_html_removes_nested_tags():
    result = strip_html("<p>Hello <strong>world</strong></p>")
    assert "Hello" in result and "world" in result

def test_strip_html_excludes_script_content():
    result = strip_html("<script>alert('evil')</script>Hello")
    assert "alert" not in result
    assert "Hello" in result

def test_strip_html_excludes_style_content():
    result = strip_html("<style>body { color: red; }</style>Hello")
    assert "color" not in result
    assert "Hello" in result


# ── strip_markdown ────────────────────────────────────────────────────────────

def test_strip_markdown_removes_atx_headers():
    assert strip_markdown("# Title\n\nBody") == "Title\n\nBody"

def test_strip_markdown_removes_bold():
    assert strip_markdown("**bold**") == "bold"

def test_strip_markdown_removes_italic():
    assert strip_markdown("_italic_") == "italic"

def test_strip_markdown_extracts_link_text():
    assert strip_markdown("[Google](https://google.com)") == "Google"

def test_strip_markdown_removes_images():
    assert strip_markdown("![alt](img.png)").strip() == ""

def test_strip_markdown_removes_fenced_code_block():
    assert "print" not in strip_markdown("```python\nprint('hi')\n```")

def test_strip_markdown_removes_inline_code():
    assert "foo" not in strip_markdown("`foo()`")


# ── process ───────────────────────────────────────────────────────────────────

def test_process_removes_punctuation():
    result = process("Hello, world!")
    assert "," not in result and "!" not in result

def test_process_preserves_words():
    result = process("Hello world")
    assert "Hello" in result and "world" in result

def test_process_preserves_numbers():
    assert "42" in process("I have 42 apples.")

def test_process_strips_html_and_markdown():
    result = process("<b>**Hello**</b>, world!")
    assert "Hello" in result and "world" in result
    assert "<b>" not in result and "," not in result


# ── CLI ───────────────────────────────────────────────────────────────────────

def test_cli_pipe():
    proc = subprocess.run(
        [sys.executable, "-m", "text_tools.cli"],
        input="Hello, world!", capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "Hello" in proc.stdout and "world" in proc.stdout
    assert "," not in proc.stdout

def test_cli_t_flag():
    proc = subprocess.run(
        [sys.executable, "-m", "text_tools.cli", "-t", "Hello, world!"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0
    assert "Hello" in proc.stdout and "world" in proc.stdout
