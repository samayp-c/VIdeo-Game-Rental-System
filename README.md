# Video Game Rental Management System

A Python-based video game rental system with a Jupyter notebook interface, database-backed rental/return workflows, and a weighted recommendation algorithm with data visualisations. Built as a university coursework project (grade: 93%).

## Features

- **Rent, return, and search games**, with input validation and empty-input handling
- **Subscription management** for customers
- **Weighted recommendation algorithm** - the standout feature. Users assign their own weightings to *popularity* and *price* depending on what matters most to them; the algorithm combines these into a single score per game to recommend the best purchases. For example, on a tight budget a user weights price more heavily, so cheaper games are favoured over merely popular ones.
- **Data visualisations** (matplotlib) - the recommendation results and additional analysis charts are rendered inline
- **Tab-based GUI** in the notebook, designed for simple, effective human-computer interaction
- **Modular design** - logic is separated into a `scripts` package (`database`, `gameRent`, `gameReturn`, `gameSearch`, `gameSelect`, `subscriptionManager`) with an `__init__.py`
- **Built-in test cases** at the end of each module (console-only, GUI-only, and shared), covering every function apart from direct database-editing functions, which are verified by console input and inspecting the database files afterwards

## Tech stack

- **Language:** Python
- **Interface:** Jupyter Notebook (`menu.ipynb`)
- **Visualisation:** matplotlib
- **Data:** flat-file storage (`.txt` data files)

## How to run

1. Clone the repository:
   ```
   git clone https://github.com/samayp-c/video-game-rental-system.git
   ```
2. Install the one external dependency:
   ```
   pip install -r requirements.txt
   ```
3. Launch Jupyter from the project folder:
   ```
   jupyter notebook
   ```
4. In the browser tab that opens, open **`menu.ipynb`** and run the cells.

**Tip:** the recommendation feature only suggests a game if it fits the entered budget. A blank time-period input means "all time". A budget of around £100+ guarantees a recommendation every time; the minimum workable budget depends on the weightings chosen.

## What I'm proud of

The weighted popularity/price recommendation algorithm, which lets users express their own priorities and produces genuinely tailored purchase recommendations, and the accompanying visualisation charts. I'm also pleased with the tabbed GUI layout and its clean, effective HCI.

## What I'd improve now

At submission, all data files couldn't be kept in a single `data` subfolder because the compiled `subscriptionManager` module had a fixed path to `subscription_info.txt`, forcing that file to sit in the root directory. Given more time I'd refactor `subscriptionManager` to resolve its path dynamically so all data files could live tidily in one folder. More broadly, I'd replace the flat-file storage with a proper database and formalise the ad-hoc module tests into a unit-testing framework.
