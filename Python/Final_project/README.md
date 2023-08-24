# 🎮Hangman game🎮

   The origins of the game are unclear but could stretch back to the 1890s. Players guess letters of an unrevealed word and then draw an arm, leg, head or torso of a stick figure hanging from gallows for every incorrect guess. If players draw all body parts and the word still hasn't been spelled out, the players lose.

## Launching

### Requirements

- Python 3.11 or higher
- Docker (for dockerizing all parts of app as microservice)

### Starting Installation

1. Clone this repository.

```bash
git clone https://github.com/TiksGal/Final_project.git
```

2. Create virtual enviroment and activate it.

```bash
python -m venv .venv
```
```bash
source .venv/Scripts/activate
```

3. Install requirements from "requirements.txt" file.

```bash
pip install -r requirements.txt
```

### Executing the program

Go to the directory where you clone this repository and type this:

```bash
python run.py
```
 or this:

 ```bash
flask run
```

### Docker

If you want to dockerize this app you should follow these steps:

This command build the container.
```bash
docker compose build --no-cache
```
This command run it.
```bash
docker compose up
```


### Gameplay instructions

1. Go to http://127.0.0.1:5000
2. Register and log in to your account.
3. Press big button in the center of the screen.
3. Guess the letters to uncover the hidden word.
4. Each wrong guess cuts the remaining tries by 1.
5. Achieve success by figuring out the full word within the given number of attempts.
6. Check the scoreboard after the game or kick off a new adventure!

