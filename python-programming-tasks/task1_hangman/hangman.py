"""Task 1: Hangman Game.

A text-based Hangman game. The computer picks a random word from a small
predefined list and the player guesses one letter at a time. The player is
allowed 6 incorrect guesses.

Run:  python task1_hangman/hangman.py
"""

import random
import string

WORDS = ["python", "developer", "algorithm", "variable", "function"]
MAX_INCORRECT = 6

# One ASCII drawing per number of incorrect guesses (0 through 6).
HANGMAN_STAGES = [
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
]


def choose_word(words=WORDS):
    """Return a random word from the given list."""
    return random.choice(words)


def mask_word(word, guessed):
    """Return the word with unguessed letters shown as underscores."""
    return " ".join(letter if letter in guessed else "_" for letter in word)


def validate_guess(raw, guessed):
    """Validate a raw guess.

    Returns a tuple (letter, error). Exactly one of them is None.
    """
    guess = raw.strip().lower()
    if len(guess) != 1 or guess not in string.ascii_lowercase:
        return None, "Please enter a single letter (a-z)."
    if guess in guessed:
        return None, f"You already guessed '{guess}'. Try a different letter."
    return guess, None


def play_game(word, input_fn=input, output_fn=print):
    """Play one round of Hangman. Returns True if the player wins."""
    word = word.lower()
    guessed = set()
    incorrect = 0

    output_fn("\n=== HANGMAN ===")
    output_fn(f"The word has {len(word)} letters. You may miss {MAX_INCORRECT} times.")

    while incorrect < MAX_INCORRECT and not set(word) <= guessed:
        output_fn("\n" + HANGMAN_STAGES[incorrect])
        output_fn("\nWord:    " + mask_word(word, guessed))
        output_fn("Guessed: " + (", ".join(sorted(guessed)) or "-"))
        output_fn(f"Incorrect guesses left: {MAX_INCORRECT - incorrect}")

        guess, error = validate_guess(input_fn("Your guess: "), guessed)
        if error:
            output_fn(error)
            continue

        guessed.add(guess)
        if guess in word:
            output_fn(f"Good job! '{guess}' is in the word.")
        else:
            incorrect += 1
            output_fn(f"Sorry, '{guess}' is not in the word.")

    if set(word) <= guessed:
        output_fn(f"\nCongratulations, you won! The word was '{word}'.")
        return True

    output_fn("\n" + HANGMAN_STAGES[MAX_INCORRECT])
    output_fn(f"\nGame over! The word was '{word}'.")
    return False


def main():
    """Run the game, allowing the player to play repeatedly."""
    try:
        while True:
            play_game(choose_word())
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                break
    except (KeyboardInterrupt, EOFError):
        print()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
