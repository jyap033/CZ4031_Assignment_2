# CZ4031: Project 2
A Python program that parses Postgres EXPLAIN output and provides visualisation in a tree view.

## Setup

### Prerequisites
- Postgres
- Python 3

### Steps
1. Create a virtual environment and run `pip install -r requirements.txt` to install the required packages.
2. Update CONFIG.txt with your Postgres credentials and also the name of the database to connect to.
3. Run project.py and try out this program!


## Project Structure

- graph_generator.py **(EXTRA FILE)** -   Generates and displays the tree graph of the QEP.
- annotation.py - Parses the query output to JSON format.
- interface.py - Displays the Graphical User Interface
- preprocessing.py - Connects the Postgres database to the application and Setup initial configurations.
- project.py - Main file to run the application.


