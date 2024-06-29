"""Utility functions for PyKnowIt."""


class QuitError(Exception):
    """Returns users to previous menu."""

    pass


def check_yes_or_no(message: str) -> bool:
    """Checks whether a user says yes or no."""
    correct_answer = 0
    while correct_answer == 0:
        answer = input(message + "\n")
        acceptable_answer = [
            "Yes",
            "Y",
            "yes",
            "y",
            "1",
            "No",
            "N",
            "no",
            "n",
            "0",
        ]
        if answer in acceptable_answer:
            correct_answer += 1
        else:
            print(
                f"I'm sorry, '{answer}' is not an acceptable answer."
                + "\nPlease respond with 'Yes' or 'No'."
            )
    return acceptable_answer.index(answer) < 5


def validate_input_for_main(repeated_message: str, option_list: str) -> int:
    """This is a helper function for the main function."""
    # Retrieve
    user_input = input(repeated_message + option_list)

    # Ensure it was an integer
    while not user_input.isdigit():
        user_input = input(
            "\nThat was not valid number. "
            + "Please enter a number from the list below:\n"
            + option_list
            + "Type 'quit' to exit\n"
        )
        # IMPORTANT: In the function that calls this function, I'll need
        # to define what happens when there's a 'quit' error
        if user_input.lower() == "quit":
            raise QuitError

    # Define acceptable answers and handle errors
    list_length = option_list.count("\n")
    acceptable_answers = [i + 1 for i in range(list_length)]
    while int(user_input) not in acceptable_answers:
        user_input = input(
            "\nThat was not valid number. "
            + "Please enter a number from the list below:\n"
            + option_list
            + "Type 'quit' to exit\n"
        )
        if user_input.lower() == "quit" or not user_input.isdigit():
            raise QuitError
    return int(user_input)
