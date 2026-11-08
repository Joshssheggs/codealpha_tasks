"""Unit tests for all four tasks. Run from the project root:

    python -m unittest discover -s tests -v
"""

import csv
import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for folder in ("task1_hangman", "task2_portfolio_tracker", "task3_automation", "task4_chatbot"):
    sys.path.insert(0, os.path.join(ROOT, folder))

import automation  # noqa: E402
import chatbot  # noqa: E402
import hangman  # noqa: E402
import portfolio_tracker as pt  # noqa: E402


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text=""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def scripted(inputs):
    """Return an input function that replays the given answers."""
    it = iter(inputs)
    return lambda prompt="": next(it)


class HangmanTests(unittest.TestCase):
    def test_word_list_has_five_words(self):
        self.assertEqual(len(hangman.WORDS), 5)
        self.assertIn(hangman.choose_word(), hangman.WORDS)

    def test_mask_word(self):
        self.assertEqual(hangman.mask_word("python", {"p", "o"}), "p _ _ _ o _")

    def test_validate_guess(self):
        self.assertEqual(hangman.validate_guess(" A ", set()), ("a", None))
        for bad in ("", "ab", "1", "!", " "):
            self.assertIsNone(hangman.validate_guess(bad, set())[0])
        self.assertIsNone(hangman.validate_guess("a", {"a"})[0])

    def test_win(self):
        out = []
        won = hangman.play_game("cat", scripted("c a t".split()), out.append)
        self.assertTrue(won)
        self.assertTrue(any("won" in line for line in out))

    def test_loss_after_exactly_six_misses(self):
        out = []
        # six wrong letters, none in "cat"
        won = hangman.play_game("cat", scripted("z x q w e r".split()), out.append)
        self.assertFalse(won)
        self.assertTrue(any("Game over" in line for line in out))

    def test_five_misses_is_not_a_loss(self):
        out = []
        inputs = "z x q w e c a t".split()
        self.assertTrue(hangman.play_game("cat", scripted(inputs), out.append))

    def test_invalid_and_repeated_guesses_do_not_cost_lives(self):
        inputs = ["c", "c", "1", "ab", "a", "t"]
        self.assertTrue(hangman.play_game("cat", scripted(inputs), lambda *_: None))

    def test_repeated_letters_in_word(self):
        self.assertTrue(hangman.play_game("book", scripted(list("bok")), lambda *_: None))


class PortfolioTests(unittest.TestCase):
    def test_parse_quantity(self):
        self.assertEqual(pt.parse_quantity(" 5 "), 5)
        for bad in ("0", "-3", "abc", "2.5", ""):
            with self.assertRaises(ValueError):
                pt.parse_quantity(bad)

    def test_calculate_total(self):
        rows, total = pt.calculate_portfolio({"AAPL": 10, "TSLA": 2})
        self.assertEqual(total, 180 * 10 + 250 * 2)
        self.assertEqual(rows[0], ("AAPL", 10, 180.0, 1800.0))

    def test_add_holding_accumulates(self):
        h = {}
        pt.add_holding(h, "aapl", 2)
        pt.add_holding(h, "AAPL", 3)
        self.assertEqual(h, {"AAPL": 5})

    def test_collect_holdings_handles_bad_input(self):
        inputs = ["", "xyz", "aapl", "abc", "aapl", "0", "AAPL", "4", "tsla", "1", "done"]
        h = pt.collect_holdings(scripted(inputs), lambda *_: None)
        self.assertEqual(h, {"AAPL": 4, "TSLA": 1})

    def test_save_txt_and_csv(self):
        rows, total = pt.calculate_portfolio({"AAPL": 2})
        with tempfile.TemporaryDirectory() as d:
            txt, csv_path = os.path.join(d, "r.txt"), os.path.join(d, "r.csv")
            pt.save_report(txt, rows, total)
            pt.save_report(csv_path, rows, total)
            self.assertIn("360.00", read(txt))
            data = list(csv.reader(read(csv_path).splitlines()))
            self.assertEqual(data[-1][0], "TOTAL")
            self.assertEqual(data[-1][-1], "360.00")
            with self.assertRaises(ValueError):
                pt.save_report(os.path.join(d, "r.pdf"), rows, total)


class AutomationTests(unittest.TestCase):
    def test_move_jpg_files(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = os.path.join(d, "src"), os.path.join(d, "dst")
            os.mkdir(src)
            for name in ("a.jpg", "B.JPG", "c.jpeg", "d.png", "e.txt"):
                write(os.path.join(src, name))
            os.mkdir(os.path.join(src, "folder.jpg"))  # directory must be ignored
            moved = automation.move_jpg_files(src, dst)
            self.assertEqual(len(moved), 3)
            self.assertEqual(sorted(os.listdir(dst)), ["B.JPG", "a.jpg", "c.jpeg"])
            self.assertIn("d.png", os.listdir(src))

    def test_move_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = os.path.join(d, "src"), os.path.join(d, "dst")
            os.makedirs(src)
            os.makedirs(dst)
            write(os.path.join(dst, "a.jpg"), "old")
            write(os.path.join(src, "a.jpg"), "new")
            automation.move_jpg_files(src, dst)
            self.assertEqual(read(os.path.join(dst, "a.jpg")), "old")
            self.assertEqual(read(os.path.join(dst, "a_1.jpg")), "new")

    def test_move_errors(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(NotADirectoryError):
                automation.move_jpg_files(os.path.join(d, "missing"), os.path.join(d, "x"))
            with self.assertRaises(ValueError):
                automation.move_jpg_files(d, d)

    def test_find_emails(self):
        text = "Mail a.b@x.com, or A.B@X.com; also c_d+tag@sub.example.org. Not: @x.com, a@b"
        self.assertEqual(automation.find_emails(text),
                         ["a.b@x.com", "c_d+tag@sub.example.org"])

    def test_extract_emails_files(self):
        with tempfile.TemporaryDirectory() as d:
            i, o = os.path.join(d, "in.txt"), os.path.join(d, "out.txt")
            write(i, "hi bob@test.com and amy@test.org")
            self.assertEqual(len(automation.extract_emails(i, o)), 2)
            self.assertEqual(read(o).split(), ["bob@test.com", "amy@test.org"])

    def test_parse_title(self):
        self.assertEqual(automation.parse_title("<html><title> My  Page </title></html>"), "My Page")
        self.assertEqual(automation.parse_title("<title>Tom &amp; Jerry</title>"), "Tom & Jerry")
        self.assertIsNone(automation.parse_title("<html><body>none</body></html>"))

    def test_scrape_title_mocked(self):
        fake = mock.Mock(text="<title>Hello</title>")
        fake.raise_for_status = mock.Mock()
        with tempfile.TemporaryDirectory() as d, mock.patch("requests.get", return_value=fake):
            out = os.path.join(d, "t.txt")
            self.assertEqual(automation.scrape_title("http://x", out), "Hello")
            self.assertIn("Title: Hello", read(out))

    def test_cli_reports_errors_without_traceback(self):
        self.assertEqual(automation.main(["move-images", "/no/such/dir", "/tmp/zz"]), 1)


class ChatbotTests(unittest.TestCase):
    def test_required_replies(self):
        self.assertEqual(chatbot.get_response("hello"), ("Hi!", False))
        self.assertEqual(chatbot.get_response("How are you?"), ("I'm fine, thanks!", False))
        self.assertEqual(chatbot.get_response("bye"), ("Goodbye!", True))

    def test_normalization_and_whole_word_matching(self):
        self.assertEqual(chatbot.get_response("  HELLO!!!  ")[0], "Hi!")
        self.assertEqual(chatbot.get_response("this is nice")[0], chatbot.FALLBACK)
        self.assertEqual(chatbot.get_response("Hello, how are you?")[0], "Hi! I'm fine, thanks!")

    def test_empty_and_unknown(self):
        self.assertEqual(chatbot.get_response("   ")[0], "Please type something.")
        self.assertEqual(chatbot.get_response("blah")[0], chatbot.FALLBACK)

    def test_chat_loop_and_eof(self):
        out = []
        chatbot.chat(scripted(["hi", "bye", "never reached"]), out.append)
        self.assertEqual(out[-1], "Chatbot: Goodbye!")

        def eof(_=""):
            raise EOFError
        out = []
        chatbot.chat(eof, out.append)
        self.assertIn("Goodbye", out[-1])


if __name__ == "__main__":
    unittest.main()
