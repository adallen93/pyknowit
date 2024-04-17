# {.tabset .tabset-fade .tabset-pills}

## Section 1: Reality 

### Introduction

This library has not been built yet. It's in process. Everything in the section 2 gives the outline for how I hope this project will go. It may be changed depending on issues I come across as I build this, but all in all, I'm shooting for something that I (and other students interested in real learning) can easily access and use as a sort of flash-card management and testing system.

For now, I'll outline my project plan in this section and keep it updated as I add more features. 

### Project Plan

* Implement SQLite3 database for storing "cards"
    - This will need to be a file that literally just takes data in some format (TBD) and stores it either in an existing database or a new database
    - The test example will be called `cheese`. This sample will have multiple categories. It will have a database for general cheese info that can test a person on their cheese knowledge, and it will have a database for cheese families, one for cheese making, and maybe one for cheese science? I'm sure there are other things I'll include
* Create functions that interact with users to do the following:
    - Print the list of "decks" that are stored for the user to choose from
    - Pull a chose "deck" out of a database
    - Randomly select a "card" to review
    - Give a user's pre-defined prompt and let the user know it's expecting an answer
    - Check the answer 
        - This could be done lots of ways. I could implement a strict version (word for word), a moderate version (e.g. most words match if it's like a sentence or a theorem), or a relaxed version (lots of tries until it's "right enough")
    - Store the user's most recent score on the card (between 0 and 1, 0 for no good and 1 for perfect)
    - Print out some kind of animations that go along with the 
* Add test database called `cheese` for users to practice with 
* Add to PyPy so that people can access the project using `pip install pyknowit`

# Section 2: End Product

## PyKnowIt

PyKnowIt is a Python library designed to facilitate flashcard-based learning through the command line interface. It provides a convenient way to review and quiz yourself on various topics using flashcards stored in a SQLite3 database.

### Features

* Flashcard Management: Easily manage your flashcards, including adding, editing, deleting, and viewing them.
* Command Line Interface: PyKnowIt offers a user-friendly command line interface for seamless interaction.
* SQLite3 Database: All flashcard data is stored in a SQLite3 database, ensuring reliability and scalability.
* Customizable: Tailor the flashcard content to your specific needs, whether it's for academic studies, language learning, or any other subject.
* Efficient Learning: PyKnowIt is designed to optimize the learning process, helping you retain information effectively.

### Installation

To install PyKnowIt, simply use pip:

`pip install pyknowit`

### Usage

After installing PyKnowIt, you can start using it immediately. Here are some basic commands to get started:

* To add a new flash card:

`pyknowit add`

* To review flashcards:

`pyknowit add`

* To delete a flashcard:

`pyknowit delete`

For more detailed usage instructions and options, please refer to the documentation.

### Contributing

Contributions are welcome! If you have any ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request. Please make sure to adhere to the code of conduct.


### Licensing

PyKnowIt is licensed under the MIT License. See LICENSE for more information. 