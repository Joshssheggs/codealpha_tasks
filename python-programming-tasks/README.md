# Python Programming Tasks

A collection of four small Python projects covering fundamentals, data
structures, file handling, regular expressions, web requests and modular design.
All four tasks are completed, tested and documented.

| # | Project | Folder | Key concepts |
|---|---------|--------|--------------|
| 1 | Hangman Game | `task1_hangman/` | `random`, loops, conditionals, strings, lists/sets |
| 2 | Stock Portfolio Tracker | `task2_portfolio_tracker/` | dictionaries, I/O, arithmetic, `csv`, file handling |
| 3 | Task Automation Scripts | `task3_automation/` | `os`, `shutil`, `re`, `requests`, `argparse` |
| 4 | Basic Chatbot | `task4_chatbot/` | functions, `if/elif`-style rules, loops, I/O |

## Requirements

- Python 3.8 or newer
- Only Task 3's `scrape-title` command needs an external package:

```bash
pip install -r requirements.txt
```

## Running each task

```bash
python task1_hangman/hangman.py
python task2_portfolio_tracker/portfolio_tracker.py
python task4_chatbot/chatbot.py
```

### Task 3 commands

```bash
# Move every .jpg/.jpeg from ./photos into ./jpg_only (created if missing)
python task3_automation/automation.py move-images ./photos ./jpg_only

# Extract unique email addresses from a text file
python task3_automation/automation.py extract-emails input.txt emails.txt

# Save the <title> of a web page (defaults to https://example.com)
python task3_automation/automation.py scrape-title --url https://example.com --output page_title.txt
```

## Task details

**Task 1 - Hangman.** Random word from a list of 5 predefined words, maximum of
6 incorrect guesses, ASCII gallows, input validation (single letters only,
repeated or invalid guesses do not cost a life), and a play-again option.

**Task 2 - Portfolio Tracker.** Enter symbols and quantities; prices come from a
hardcoded dictionary (`AAPL`, `TSLA`, `GOOGL`, `MSFT`, `AMZN`). Shows a formatted
table and the total investment, and can save the report as `.txt` or `.csv`.
Unknown symbols and invalid quantities are rejected with a helpful message.

**Task 3 - Automation.** All three options are implemented: moving images
(case-insensitive, never overwrites existing files), extracting unique emails
with a regular expression, and scraping a page title with timeout and HTTP
error handling.

**Task 4 - Chatbot.** Replies to "hello" with "Hi!", "how are you" with
"I'm fine, thanks!" and "bye" with "Goodbye!" (and exits). Input is
case-insensitive, punctuation-tolerant and matched by whole words.

## Testing

```bash
python -m unittest discover -s tests -v
```

The suite covers normal use, edge cases and error handling for every task.
Network access is mocked, so the tests run offline.

## Project structure

```
python-programming-tasks/
├── README.md
├── requirements.txt
├── task1_hangman/hangman.py
├── task2_portfolio_tracker/portfolio_tracker.py
├── task3_automation/automation.py
├── task4_chatbot/chatbot.py
└── tests/test_all_tasks.py
```

## Submission

Upload this folder to a GitHub repository (for example `python-programming-tasks`),
then submit the repository link through the submission form.
