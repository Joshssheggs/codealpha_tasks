"""Task 3: Task Automation with Python Scripts.

Three small automation utilities in one command-line tool:

  move-images    Move all .jpg/.jpeg files from a folder into a new folder.
  extract-emails Extract all email addresses from a .txt file into another file.
  scrape-title   Fetch a web page and save its <title> to a file.

Examples:
  python task3_automation/automation.py move-images ./photos ./jpg_only
  python task3_automation/automation.py extract-emails input.txt emails.txt
  python task3_automation/automation.py scrape-title --url https://example.com
"""

import argparse
import html
import os
import re
import shutil
import sys
from html.parser import HTMLParser

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
)
JPG_EXTENSIONS = (".jpg", ".jpeg")
DEFAULT_URL = "https://example.com"


# ---------------------------------------------------------------- move images
def unique_path(path):
    """Return a path that does not exist yet by appending _1, _2, ..."""
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"


def move_jpg_files(source, destination):
    """Move .jpg/.jpeg files (any letter case) from source into destination.

    Only files directly inside `source` are moved. Existing files are never
    overwritten; duplicates get a numeric suffix. Returns the list of new paths.
    """
    if not os.path.isdir(source):
        raise NotADirectoryError(f"Source folder not found: {source}")
    if os.path.realpath(source) == os.path.realpath(destination):
        raise ValueError("Source and destination must be different folders.")

    os.makedirs(destination, exist_ok=True)
    moved = []
    for name in sorted(os.listdir(source)):
        full_path = os.path.join(source, name)
        if os.path.isfile(full_path) and name.lower().endswith(JPG_EXTENSIONS):
            target = unique_path(os.path.join(destination, name))
            shutil.move(full_path, target)
            moved.append(target)
    return moved


# ------------------------------------------------------------- extract emails
def find_emails(text):
    """Return unique email addresses in order of first appearance."""
    seen = set()
    result = []
    for match in EMAIL_PATTERN.findall(text):
        key = match.lower()
        if key not in seen:
            seen.add(key)
            result.append(match)
    return result


def extract_emails(input_path, output_path):
    """Read a text file, extract emails and write one per line. Returns the list."""
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        emails = find_emails(f.read())
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(emails) + ("\n" if emails else ""))
    return emails


# --------------------------------------------------------------- scrape title
class _TitleParser(HTMLParser):
    """Collects the text inside the first <title> element."""

    def __init__(self):
        super().__init__()
        self._in_title = False
        self._done = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title" and not self._done:
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title = False
            self._done = True

    def handle_data(self, data):
        if self._in_title:
            self.parts.append(data)


def parse_title(page_html):
    """Return the page title from an HTML string, or None if there is none."""
    parser = _TitleParser()
    parser.feed(page_html)
    title = " ".join("".join(parser.parts).split())
    return title or None


def scrape_title(url, output_path):
    """Download a page, extract its title and save it. Returns the title."""
    import requests  # imported here so the other tools work without it

    response = requests.get(
        url, timeout=10, headers={"User-Agent": "Mozilla/5.0 (Python task script)"}
    )
    response.raise_for_status()
    title = parse_title(response.text)
    if title is None:
        raise ValueError("No <title> tag found on the page.")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"URL: {url}\nTitle: {title}\n")
    return title


# ------------------------------------------------------------------------ CLI
def build_parser():
    parser = argparse.ArgumentParser(description="Python automation utilities.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("move-images", help="Move .jpg files into a new folder.")
    p.add_argument("source", help="Folder containing the images.")
    p.add_argument("destination", help="Folder to move them to (created if missing).")

    p = sub.add_parser("extract-emails", help="Extract emails from a text file.")
    p.add_argument("input", help="Input .txt file.")
    p.add_argument("output", help="Output file for the emails.")

    p = sub.add_parser("scrape-title", help="Save the title of a web page.")
    p.add_argument("--url", default=DEFAULT_URL, help=f"Page URL (default: {DEFAULT_URL}).")
    p.add_argument("--output", default="page_title.txt",
                   help="Output file (default: page_title.txt).")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "move-images":
            moved = move_jpg_files(args.source, args.destination)
            print(f"Moved {len(moved)} image(s) to {args.destination}")
        elif args.command == "extract-emails":
            emails = extract_emails(args.input, args.output)
            print(f"Found {len(emails)} unique email(s). Saved to {args.output}")
        else:
            title = scrape_title(args.url, args.output)
            print(f"Title: {title}\nSaved to {args.output}")
    except ImportError:
        print("Error: the 'requests' package is required. Run: pip install requests")
        return 1
    except Exception as error:  # report any failure cleanly instead of a traceback
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
