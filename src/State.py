from unidecode import unidecode

class State:
    def __init__(self, word, tries):
        self.__realWord = list(word)
        self.__lettersUsed = set()
        self.__currentWord = ['_'] * len(self.__realWord)
        self.__tries = tries
        self.running = True

    def setWord(self, word, tries):
        """Set a new word to the environment"""
        self.__realWord = list(word)
        self.__lettersUsed = set()
        self.__currentWord = ['_'] * len(self.__realWord)
        self.__tries = tries
        self.running = True

    def addLetterUsed(self, letter):
        assert type(letter) == str and len(letter) == 1, "Letter must be a string with length == 1."
        self.__lettersUsed.add(letter)

    def getLetters(self):
        """Get letters already used by the agent"""
        return self.__lettersUsed
    
    def getWrongLetters(self):
        """Get letters that are not contained inside current word"""
        return {l for l in self.__lettersUsed if l not in self.__realWord}
    
    def getWord(self):
        """Returns list with current word partially revealed by agent choices"""
        return self.__currentWord
        
    def getWordLen(self):
        """Returns current word length"""
        return len(self.__currentWord)
    
    def getRemainingTries(self):
        """Returns current number of remaining tries"""
        return self.__tries
    
    def guess(self, guess):
        """Reveals a letter or word based on agent guess."""
        assert self.__tries > 0, "Agent ran out of tries."

        if len(guess) == 1:
            self.addLetterUsed(guess)
            
            changeMade = False
            for i, letterRealWord in enumerate(self.__realWord):
                if unidecode(letterRealWord) == guess and self.__currentWord[i] == '_':
                    self.__currentWord[i] = letterRealWord
                    changeMade = True

            if changeMade == False:
                self.__tries -= 1

            return changeMade

        else:
            self.running = False
            if guess == "".join(self.__realWord):
                return True

            self.__tries = 0
            return False

    def revealWord(self):
        """Reveals current word completely and ends the game"""
        self.running = False
        self.__tries = 0
        self.__currentWord = self.__realWord.copy()