"""Sandbox for PyKnowit."""

import sqlite3  # noqa: F401
import string  # noqa: F401
from os.path import dirname, join  # noqa: F401
from random import choice, choices, random, sample, seed, shuffle  # noqa: F401
from time import sleep  # noqa: F401

from utils import (  # noqa: F401
    QuitError,
    check_yes_or_no,
    validate_input_for_main,
)

BOLDT = "\033[1m"
UNDERLINE = "\033[4m"
REDT = "\033[91m"
REDB = "\033[41m"
GREENT = "\033[92m"
GREENB = "\033[42m"
YELLOWT = "\033[1m"
YELLOWB = "\033[43m"
BLUET = "\033[94m"
BLUEB = "\033[44m"
GRAYT = "\033[90m"
GRAYB = "\033[100m"
PURPLET = "\033[95m"
CYANT = "\033[96m"
WHITET = "\033[97m"
WHITEB = "\033[107m"
RESET = "\033[0m"
YN = f"({GREENB} Y {RESET}/{REDB} N {RESET})"


class Card:
    """This is an item that stores information to retrieve."""

    def __init__(
        self, conn: sqlite3.Connection, table: str, id: int, tag: str
    ) -> None:
        """Initializer."""
        self.conn = conn
        self.id = id
        self.tag = tag
        self.table = table

        # Set cursor
        cursor = conn.cursor()

        # Retrieve card information
        cursor.execute(
            f"""SELECT question, answer, 
        correct_response_count, incorrect_response_count 
        FROM {table} WHERE tag=? AND id=?""",
            (tag, id),
        )
        card_info = cursor.fetchall()
        question = card_info[0][0]
        answer = card_info[0][1]
        correct_response_count = card_info[0][2]
        incorrect_response_count = card_info[0][3]

        self.question = question
        self.answer = answer
        self.correct_response_count = correct_response_count
        self.incorrect_response_count = incorrect_response_count

    def print_question(self, attempts: int, is_question: bool = True) -> None:
        """Wrapper function for print_card, printing the question side."""
        print_card("Question", CYANT, self.question, attempts, is_question)

    def print_answer(self, is_correct: bool) -> None:
        """Wrapper function for print_card, printing the answer side."""
        col = GREENT if is_correct else REDT
        print_card("Answer", col, self.answer, 0, False)

    def calculate_max_attempts(self) -> int:
        """Calculates the number of attempts a user can get."""
        # Set numerator and denominator for easy calculations
        denominator = (
            self.correct_response_count + self.incorrect_response_count
        )
        denominator = 1 if denominator == 0 else denominator
        numerator = self.correct_response_count

        # Calculate the proportion of correct reponses
        proportion_correct = numerator / denominator

        # Determine max attempts based on the proportion of correct responses
        if proportion_correct >= 0.8:
            max_attempts = 1
        elif proportion_correct >= 0.2:
            max_attempts = 2
        else:
            max_attempts = 3

        return max_attempts

    def test_user(self) -> bool:
        """Tests user's knowledge."""
        # Calculate the number of attempts the user has
        attempts_remaining = self.calculate_max_attempts()
        message = "\n"
        correct_response = False
        while attempts_remaining > 0 and not correct_response:
            print(message)
            # Print the card question for the user and retrieve a response
            self.print_question(attempts_remaining)
            response = input(f"{GRAYB}Please enter your response:{RESET}\n\n")

            # Verify the user is satisfied with the response
            is_correct = False
            while not is_correct:
                print(
                    f"Your response is below:\n\n{GRAYB}{response}{RESET}\n\n"
                )
                is_correct = check_yes_or_no(
                    f"Do you want to submit this response? {YN}\n"
                )
                if not is_correct:
                    response = input("Please enter your response:\n\n")

            # Check whether the user responded correctly
            correct_response = examine_response(self.answer, response)
            attempts_remaining -= 1
            if not correct_response:
                message = (
                    "I'm sorry, but that was not the correct response.\n"
                    + f"You have {GRAYB} {attempts_remaining} {RESET} "
                    + "attempts remaining.\n"
                )
                sleep(0.25)

        # Update the appropriate field in the table
        item_to_update = (
            "correct_response_count"
            if correct_response
            else "incorrect_response_count"
        )
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE {self.table} SET {item_to_update} = {item_to_update} + 1"
        )

        # Print the card for the user and a final message
        final_message = (
            f"\n{GREENB}CORRECT!{RESET}\n"
            if correct_response
            else f"\n{REDB}INCORRECT:{RESET}\n"
        )
        print(final_message)
        self.print_answer(correct_response)

        return correct_response


def add_card(conn: sqlite3.Connection, table: str) -> None:
    """Works with user to add a card to the database."""
    # Set cursor
    cursor = conn.cursor()

    # Retrieve tags from database
    cursor.execute(f"SELECT DISTINCT tag FROM {table}")
    tags = cursor.fetchall()

    # List tags for user
    tag_opts = {1: "New tag"}
    for i, tag in enumerate(tags):
        tag_opts[i + 2] = tag[0]
    tag_string = ""
    for i, tag in tag_opts.items():
        tag_string += f"{i}: {tag}\n"

    # Retrieve user's chosen tag
    user_input = validate_input_for_main(
        "Please select a tag from the list below:\n", tag_string
    )
    chosen_tag = tag_opts[user_input]
    is_new_tag = chosen_tag == "New tag"

    # Ensure new tags are entered correctly
    is_correct = False
    while not is_correct and is_new_tag:
        chosen_tag = input("Please enter a tag for your card:\n")
        is_correct = check_yes_or_no(
            f"Your response:\n\n{GRAYB}{chosen_tag}{RESET}"
            + f"\n\nIs this correct? {YN}\n"
        )

    # Get card information from user

    # Question
    is_correct = False
    while not is_correct:
        card_question = input("Please enter the card question:\n")
        is_correct = check_yes_or_no(
            f"Your response:\n\n{GRAYB}{card_question}{RESET}"
            + f"\n\nIs this correct? {YN}\n"
        )
    # Answer
    is_correct = False
    while not is_correct:
        card_answer = input("Please enter the card answer:\n")
        is_correct = check_yes_or_no(
            f"Your response:\n{GRAYB}{card_answer}{RESET}"
            + f"\n\nIs this correct? {YN}\n\n"
        )

    # Get the card ID
    id = auto_increment(conn, table, chosen_tag)

    # Add the card to the database
    cursor.execute(
        f"""INSERT INTO {table} (id, tag, question, answer, 
        correct_response_count, incorrect_response_count) VALUES 
        (?, ?, ?, ?, ?, ?)
        """,
        (id, chosen_tag, card_question, card_answer, 0, 0),
    )
    conn.commit()

    # Create the card
    card = Card(conn, table, id, chosen_tag)
    print(f"Card added {GRAYB}successfully{RESET}\nSee below for card info:\n")
    card.print_question(attempts=0, is_question=False)
    card.print_answer(is_correct=True)


def auto_increment(conn: sqlite3.Connection, table: str, tag: str) -> int:
    """Returns the last ID plus 1 for a given tag."""
    # Set cursor
    cursor = conn.cursor()

    # Retrieve most recent ID for the given tag
    cursor.execute(
        f"SELECT id FROM {table} WHERE tag='{tag}' ORDER BY id DESC LIMIT 1"
    )

    # Try subscripting the tuple to see if data is available
    try:
        new_id: int = cursor.fetchone()[0] + 1
        return new_id

    # If there is no data available, start the index at 1
    except Exception:
        return 1


def create_cards_table(conn: sqlite3.Connection) -> None:
    """Creates the default 'cards' table."""
    # Set cursor
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cards (
            tag TEXT,
            id INTEGER,
            question TEXT,
            answer TEXT,
            correct_response_count INTEGER,
            incorrect_response_count INTEGER
        ) 
        """
    )


def choose_card(conn: sqlite3.Connection, table: str, tag: str) -> Card:
    """Returns a card from an SQLite3 database."""
    # Set cursor
    cursor = conn.cursor()

    # Get ID's
    cursor.execute(f"SELECT id FROM {table} WHERE tag='{tag}'")
    id_choices = cursor.fetchall()
    if not id_choices:
        raise QuitError

    # Randomly choose an id
    id = choice(id_choices)[0]

    return Card(conn, table, id, tag)


def examine_response(
    question: str, response: str, level: float = 0.85
) -> bool:
    """Determines whether a user responded correctly enough."""
    # Prepare question and response for easy comparison
    q_adjusted = question.lower()
    r_adjusted = response.lower()
    q_list = q_adjusted.split(" ")
    r_list = r_adjusted.split(" ")

    # Test if each word of the response is in the question
    n_correct = 0
    for r_word in r_list:
        n_correct += 1 if r_word in q_list else 0

    # Return whether the user responded with a higher correct word proportion
    # than the level
    return n_correct / len(q_list) > level


def print_card(
    side: str,
    col: str,
    text: str,
    attempts_left: int,
    is_question: bool = True,
) -> None:
    """Prints one side of the card."""
    card_width = 50

    # Create all pieces of the printed output
    banner = col + "-" * (card_width + 4) + RESET + "\n"
    header = (
        f"{col}|{RESET}{GRAYT} {side}:"
        + " " * (card_width - len(f"{side}:") + 1)
        + f"{col}|{RESET}\n"
    )
    if is_question:
        footer = (
            f"{col}|{RESET}{GRAYT} Number of attempts remaining:{RESET} "
            + f"{GRAYB} {attempts_left} {RESET}"
            + " " * 18
            + f"{col}|{RESET}\n"
        )
    else:
        footer = ""
    blank_line = f"{col}|{RESET}" + (card_width + 2) * " " + f"{col}|{RESET}\n"
    wrapped_text = wrap_text(text, card_width, col)

    # Put all the pieces together
    card = (
        banner
        + header
        + blank_line
        + wrapped_text
        + blank_line
        + footer
        + banner
    )
    print(card)


def review_cards(conn: sqlite3.Connection, table: str) -> None:
    """Tests user on cards."""
    # Set cursor
    cursor = conn.cursor()

    # Set logical parameter to exit the program when the user is done
    user_not_done = True
    repeated_message = "Let's begin reviewing.\n\nRetrieving all decks.\n\n"
    while user_not_done:
        print(repeated_message)
        # Retrieve tags from database
        cursor.execute(f"SELECT DISTINCT tag FROM {table}")
        tags = cursor.fetchall()

        # End the function if there are no tags
        if not tags:
            print(
                "I'm sorry, but there aren't any cards available.\n"
                + "Come back when you've added a few cards to a deck!\n"
            )
            return

        # List tags for user
        tag_opts: dict[int, str] = {}
        for i, tag in enumerate(tags):
            tag_opts[i + 1] = tag[0]
        tag_string = ""
        for i, tag in tag_opts.items():
            tag_string += f"{i}: {tag}\n"

        # Retrieve user's chosen tag
        user_input = validate_input_for_main(
            "Please select a tag to review from the list below:\n", tag_string
        )
        chosen_tag = tag_opts[user_input]

        # Randomly select a card
        card = choose_card(conn, "cards", chosen_tag)
        card.test_user()

        # Ask the user if they would like to continue
        user_not_done = check_yes_or_no(
            f"\nWould you like to review another card? {YN}\n\n"
        )
        repeated_message = ""


def run_cards() -> None:
    """Runs all functions related to flash cards for PyKnowIt."""
    # Set database path
    db = join(dirname(dirname(__file__)), "db/cards.db")

    # Open database connection
    with sqlite3.connect(db) as conn:
        # Create the cards table
        create_cards_table(conn)

        # define user options
        user_options = {
            1: "Add card",
            2: "Review cards",
            3: f"Return to {GRAYB}main menu{RESET}",
        }

        # Set the string for printing
        user_opts_string = ""
        for i, opt in user_options.items():
            user_opts_string += f"{i}: {opt}\n"

        user_choice = 0
        while user_choice != 3:
            user_choice = validate_input_for_main(
                "\nPlease select an option below:\n", user_opts_string
            )
            if user_choice == 1:
                add_card(conn, "cards")
            elif user_choice == 2:
                review_cards(conn, "cards")


def wrap_text(message: str, width: int, col: str) -> str:
    """Wraps text and aligns it within certain bounds."""
    # Separate the words into a list for easy parsing
    word_list = message.split(" ")

    # Start the message with the first word (must contain at least 1 word)
    wrapped_message = ""
    current_line = ""

    # Iterate over each word and add to the current line
    for current_word in word_list:
        # The potential line is the current line as lon as it's less than
        # the width length
        potential_line = current_line + " " + current_word
        current_line = (
            potential_line if len(potential_line) < width else current_line
        )

        # Add the line to the message if the potential line is too large
        if len(potential_line) >= width:
            # Adjust the margins as needed
            col_adjustment = len(f"{col}{RESET}") + 2
            left_margin = (
                col + "| " + RESET + int((width - len(current_line)) / 2) * " "
            )
            current_line = left_margin + current_line
            right_margin = (
                (width - len(current_line) + col_adjustment) * " "
                + col
                + " |"
                + RESET
            )

            # Add all parts to the wrapped message
            wrapped_message += current_line + right_margin + "\n"

            # Set the new 'current line' to be the word that was left off
            current_line = current_word

    # After going through the list, add the last line to the text
    col_adjustment = len(f"{col}{RESET}") + 2
    left_margin = (
        col + "| " + RESET + int((width - len(current_line)) / 2) * " "
    )
    current_line = left_margin + current_line
    right_margin = (
        (width - len(current_line) + col_adjustment) * " " + col + " |" + RESET
    )
    wrapped_message += current_line + right_margin + "\n"

    return wrapped_message


if __name__ == "__main__":
    run_cards()
