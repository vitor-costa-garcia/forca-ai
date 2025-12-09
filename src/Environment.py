from src.State import State
from random import randint, sample

class Environment:
    def __init__(self, word, tries):
        """
        ## Hangman Environment
        This implementation of hangman game allows the user to load a set of words so an intelligent agent plays and learns gradually to make better guesses.
        A number of maximum errors a match can admit can be set.
        """
        self.__tries = tries
        self.__state = State(word, tries)

    def __str__(self):
        return f"""
| Current word: {" ".join(self.__state.getWord())}
| Letters used: {" ".join([ f"[{l}]" for l in self.__state.getLetters()])}
| Tries remaining: {self.__state.getRemainingTries()}
| Situation: {["Ongoing", "Win", "Loss"][self.getGameSituation()]}
                """
    
    def getState(self):
        return self.__state

    def setTries(self, tries):
        """
        ## Set tries
        Setter for tries variable. Does not reset current tries, reset() needs to be called.
        """
        self.__tries = tries

    def getRealWord(self):
        """
        ## Get real word
        Getter for real word. End the game automatically when called and tries are set to 0. Should be called only at the end so the agent can learn the word.
        """
        self.__state.revealWord()
        return "".join(self.__state.getWord())

    def getRunning(self):
        """
        ## Get Running
        Getter for state running variable. check if game is still running
        """
        return self.__state.running

    def getCurrentTries(self):
        """
        ## Get current tries
        Getter for current tries. Returns remaining number of tries of the current episode. 
        """
        return self.__state.getRemainingTries()
    
    def getGameSituation(self):
        """
        ## Get Game Situation
        Returns current game situation
        0-Ongoing
        1-Win
        2-Lose
        """
        if self.__state.running:
            return 0
        
        if self.__state.getRemainingTries():
            return 1
        
        return 2

    def load(self, filename, sep='\n'):
        """
        ## Load
        Load a set of words into the environment. File must be specified. THIS RESETS CURRENT WORDS LOADED.
        """
        with open(filename, encoding='utf-8') as f:
            self.__words = set(f.read().split(sep))

        print(f"Loaded {len(self.__words)} words succesfully.")

    def export(self, filename, sep='\n'):
        """
        ## Export
        Export set of words loaded into the environment. Output filename must be specified.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sep.join(self.__words))

        print(f"File saved in  {filename}.")

    def reset(self):
        """
        ## Reset
        Resets the environment and chooses a new word randomly from available set of words
        """
        assert len(self.__words) > 0, 'There are no words available. Use load() method to add new words to the environment.'
        nextRandomWord = sample(list(self.__words), 1)
        self.__state.setWord(nextRandomWord[0], self.__tries)

    def step(self, guess: str) -> bool:
        """
        ## Step
        Validates a guess and updates the environment.
        """
        assert type(guess) == str and len(guess) > 0, "Guess must be a string of length >= 1."
        if self.__state.getRemainingTries() == 0:
            self.__state.running = False
            return

        goodGuess = self.__state.guess(guess)
        
        return goodGuess