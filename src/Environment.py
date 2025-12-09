from State import State

class Environment:
    def __init__(self, tries):
        """
        ## Hangman Environment
        This implementation of hangman game allows the user to load a set of words so an intelligent agent plays and learns gradually to make better guesses.
        A number of maximum errors a match can admit can be set.
        """
        self.__tries = tries
        self.__state = State()

    def setTries(self, tries):
        """
        ## Set tries
        Setter for tries variable
        """
        self.__tries = tries

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


