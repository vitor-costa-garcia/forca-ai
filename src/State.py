class State:
    def __init__(self, word):
        self.__realWord = list(word)
        self.__lettersUsed = set()
        self.__currentWord = ['_'] * len(self.__realWord)

    def setWord(self, word):
        """Set a new word to the environment"""
        self.__realWord = list(word)
        self.__lettersUsed = set()
        self.__currentWord = ['_'] * len(self.__realWord)

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
