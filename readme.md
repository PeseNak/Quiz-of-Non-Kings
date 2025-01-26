# Quiz of Non-Kings

A small Python-based project created as a **programming practice** and **university project**. This project features a simple **multiple-choice quiz game** with a graphical user interface (GUI) developed using `tkinter`. It includes several functionalities such as user registration, login, and question submission.

---

## Features

- **User Registration & Login**: Users can create an account and log in to play the game.
- **Multiple-Choice Quiz**: Players answer timed, four-option questions during the game.
- **Submit Questions**: Users can propose their own quiz questions. Submitted questions, if approved by the admin, are added to the game along with the user’s name.
- **Admin Panel**: The admin has access to a dedicated menu to review, approve, or reject submitted questions.
  - To access the admin menu and manage submitted questions, run `admin.py`.
- **Sound Effects**: Audio effects enhance the gameplay experience.

---

## Installation

### Requirements

- **Python 3.7+**
- **pygame 2.6.1**

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/PeseNak/Quiz-of-Non-Kings.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Quiz-of-Non-Kings
   ```
3. Install dependencies:
   ```bash
   pip install pygame==2.6.1
   ```
   or
   ```bash
   pip install -r requirements.txt
   ```
4. Run the game:
   ```bash
   python main.py
   ```

---

## Usage

1. Register a new user or log in with an existing account.
2. Start the quiz and answer questions within the time limit.
3. Optionally, propose new questions through the user interface.

---

## Project Structure

```plaintext
Quiz-of-Non-Kings/
│
├── assets/            # Assets for the game
│   ├── images/        # Image files for the GUI
│   └── sounds/        # Sound effects
│       ├── correct.mp3
│       ├── timeout.mp3
│       └── wrong.mp3
├── data/              # Data storage
│   ├── questions.json # Default questions
│   ├── userQ.json     # User-submitted questions
│   └── users.json     # User accounts data
├── admin.py           # Admin functionalities
├── main.py            # Entry point of the game
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```
