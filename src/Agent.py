from State import State
from random import randint
from unidecode import unidecode

ABC = 'abcdefghijklmnopqrstuvwxyz'

class Agent:
    def __init__(self):
        """
        ## Agent
        Simple agent for the hangman game.

        ## Methods
        ### Load:
        Load external knowledge for agent. Must recieve path to .csv file with words.
        ### Export:
        Export internal knowledge from agent. Must receive name for exported file.
        ### Guess:
        Guesses a letter or word based on current state. If no words matches the current state, a simple heuristic is used to determine
        a good guess. Returns a string.
        """

        self.__words = set()
        self.__tWords = set()
        self.__letterRelations = dict()
        self.__firstLetterFrequency = dict()

    def __filter(self, state: State):
        """
        ## Filter
        Filters possible words based on current state.
        """
        def mask(word, currentWord, wrongLetters): # Verifies if word matches partially revealed word pattern
            for wordL, stateL in zip(word, currentWord):
                if wordL != stateL and stateL != '_':
                    return False
                if wordL in wrongLetters:
                    return False
            return True
        
        self.__tWords = {w for w in self.__tWords if mask(w, state.getWord(), state.getWrongLetters())}

    def __letterRelationships(self):
        """
        ## Letter Relationship
        Estimate letter relationships for a good guess when the word is unknown by the agent.
        ONLY RUN ONCE IF NECESSARY, WHEN THE WORD IN UNKNOWN AND AGENT HAS SOME KNOWLEGDE.
        Result is saved on self.__letterRelations and self.__firstLetterFrequency.
        There is no reason to run this function again if no knowledge is obtained.
        """
        for word in self.__tWords:
            wordWP = unidecode(word)
            for i, letter in enumerate(wordWP):
                if i == 0:
                    if letter in self.__firstLetterFrequency.keys():
                        self.__firstLetterFrequency[letter] += 1
                    else:
                        self.__firstLetterFrequency[letter] = 1

                else:
                    previousLetter = wordWP[i-1]
                    if previousLetter in self.__letterRelations.keys():
                        if letter in self.__letterRelations[previousLetter].keys():
                            self.__letterRelations[previousLetter][letter] += 1
                        else:
                            self.__letterRelations[previousLetter][letter] = 1

                    else:
                        self.__letterRelations[previousLetter] = dict()
                        self.__letterRelations[previousLetter][letter] = 1

    def reset(self):
        """
        ## Reset
        Resets agent temporary word buffer
        """
        self.__tWords = self.__words

    def learn(self, word):
        """
        ## Learn
        Adds a new word to agent knowledge. RESETS AGENT TEMPORARY WORD BUFFER WHEN CALLED. Must be used only at the end of episode.
        """
        self.__words.add(word)
        self.reset()

    def load(self, filename, sep='\n'):
        """
        ## Import
        Import knowledge for agent. RESETS CURRENT KNOWLEGDE.
        """
        with open(filename, encoding='utf-8') as f:
            self.__words = set(f.read().split(sep))

        print(f"Loaded {len(self.__words)} words succesfully.")

    def export(self, filename, sep='\n'):
        """
        ## Export
        Export agent knowlegde to a .csv or .txt file. File type MUST BE SPECIFIED in filename.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sep.join(self.__words))

        print(f"File saved in  {filename}.")

    def guess(self, state):
        """
        ## Guess
        Guesses a letter or word based on current state.
        """
        # Filtering possible words
        self.__filter(state)

        if len(self.__tWords) == 1 and '_' not in state.getWord():
            # Word found!
            return self.__tWords[0]

        elif len(self.__tWords) > 0:
            # Chooses most frequent letter count by word
            frequencyByLetter = {l : 0 for l in ABC}
            for word in self.__tWords:
                wordWP = unidecode(word)
                bufferSeenLetter = set()
                for letter in wordWP:
                    if letter not in bufferSeenLetter:
                        frequencyByLetter[letter] += 1
                        bufferSeenLetter.add(letter)

            # Returns letter with max frequency
            return max(frequencyByLetter, key=frequencyByLetter.get)

        else: # The word is unknown, heuristic is needed. Full agent knowlegde should be used here to estimate best letter.

            if len(self.__words) > 0: #Using agent total knowledge to estimate letter relationships. This might be expesive!
                self.__letterRelationships()
                currentWord = state.getWord()
                for i, letter in enumerate(currentWord):
                    if letter == '_': #Algorithm should guess for first unknown letter found left to right
                        if i == 0: # If the first letter is missing
                            return max(self.__firstLetterFrequency, key=self.__firstLetterFrequency.get)
                        
                        elif currentWord[i-1] != '_': # If any other letter is missing
                            return max(self.__firstLetterFrequency, key=self.__firstLetterFrequency.get)

            #Returns random letter case no other heuristic is available
            return set(ABC).difference(state.getLetters())[randint(0, 25 - len(state.getLetters()))]
