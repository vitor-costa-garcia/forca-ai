class State:
    def __init__(self):
        self.__realWord = list()
        self.__lettersUsed = set()
        self.__currentWord = ['_'] * len(self.__realWord)

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
