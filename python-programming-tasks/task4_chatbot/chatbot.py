"""Task 4: Basic Rule-Based Chatbot.

Reads user input, matches it against predefined phrases and prints a canned
reply. Type 'bye' to end the conversation.

Run:  python task4_chatbot/chatbot.py
"""

import re

BYE_PHRASES = ("bye", "goodbye", "see you", "quit", "exit")

# (trigger phrases, reply) - all matching rules are combined in this order.
RULES = [
    (("hello", "hi", "hey", "good morning", "good afternoon", "good evening"), "Hi!"),
    (("how are you", "how are you doing", "how r u", "how are u"), "I'm fine, thanks!"),
    (("your name", "who are you"), "I'm a simple rule-based chatbot."),
    (("help", "what can you do"), "Try saying hello, asking how I am, or saying bye."),
    (("thanks", "thank you"), "You're welcome!"),
]

FALLBACK = "Sorry, I didn't understand that. Type 'help' to see what I can do."


def normalize(text):
    """Lowercase, strip punctuation and collapse whitespace."""
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower().replace("'", ""))
    return " ".join(text.split())


def contains_phrase(text, phrase):
    """True if `phrase` appears in `text` as whole word(s)."""
    return f" {phrase} " in f" {text} "


def get_response(user_input):
    """Return (reply, should_exit) for the given user message."""
    text = normalize(user_input)
    if not text:
        return "Please type something.", False

    if any(contains_phrase(text, phrase) for phrase in BYE_PHRASES):
        return "Goodbye!", True

    replies = [
        reply for phrases, reply in RULES
        if any(contains_phrase(text, p) for p in phrases)
    ]
    return (" ".join(replies) if replies else FALLBACK), False


def chat(input_fn=input, output_fn=print):
    """Run the chat loop until the user says goodbye."""
    output_fn("Chatbot: Hello! Say 'bye' when you want to leave.")
    while True:
        try:
            message = input_fn("You: ")
        except (EOFError, KeyboardInterrupt):
            output_fn("\nChatbot: Goodbye!")
            break
        reply, should_exit = get_response(message)
        output_fn(f"Chatbot: {reply}")
        if should_exit:
            break


if __name__ == "__main__":
    chat()
