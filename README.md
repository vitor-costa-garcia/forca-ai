# Hangman Game!
This repository contains a simple algorithm that plays the hangman game. Its able to learn new words and make better predictions as it learns more.

## Structure
```text
main.py
src/
├─ data/
│  ├─ icf.txt
│  └─ words.txt
├─ Agent.py
├─ Environment.py
└─ State.py
README.md
```


## Agent & Environment
The environment is a simple implementation of the hangman game with some tweaks to facilitate the implementation of a simple intelligent agent, which can guess and learn new words as it plays.

The agent keeps track of new words thrown by the environment, so when it doesn't know the word and fails (or even gets it right with enough luck), it learns and makes better guesses after.

The heuristics used by the agent are simple and easy to understand.

## Requirements
To run this algorithm you need the unidecode module, which is used only for character accents removal. Highly reccomended to run this following block of code instead of downloading module in global python environment:

```cmd
python -m venv venv
cd venv\Scripts\
activate
pip install unidecode
```

Made by André Tomonada Schettini & Vitor da Costa Garcia
