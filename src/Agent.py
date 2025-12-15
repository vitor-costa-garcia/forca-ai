from src.State import State
from random import randint
from unidecode import unidecode

ABC = 'abcdefghijklmnopqrstuvwxyz'

class Agent:
    def __init__(self):
        self.__words = set()
        self.__tWords = set()
        self.__letterRelations = dict()
        self.__firstLetterFrequency = dict()
        self.__letterRelationsUpdated = False

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
        self.__letterRelations = dict() #Reseting old ones
        self.__firstLetterFrequency = dict()

        for word in self.__words:
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

    def reset(self, lengthWord):
        """
        ## Reset
        Resets agent temporary word buffer and filters for current word
        """
        self.__tWords = {w for w in self.__words if len(w) == lengthWord}

    def learn(self, word):
        """
        ## Learn
        Adds a new word to agent knowledge. RESETS AGENT TEMPORARY WORD BUFFER WHEN CALLED. Must be used only at the end of episode.
        """
        self.__words.add(word)
        self.reset(len(word))
        self.__letterRelationsUpdated = False

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
        # Filtra as palavras possíveis
        self.__filter(state)

        if '_' not in state.getWord(): # Retorna a palavra caso tenha encontrado
            return "".join(state.getWord())

        elif len(self.__tWords) > 0: # Se o agente ainda tem palavras que batem com o padrão do ambiente
            # Conta a frequência de cada letra no conjunto de palavras conhecidas
            frequencyByLetter = {l : 0 for l in ABC}
            for word in self.__tWords:
                wordWP = unidecode(word)
                bufferSeenLetter = set()
                for letter in wordWP:
                    if letter not in bufferSeenLetter:
                        frequencyByLetter[letter] += 1
                        bufferSeenLetter.add(letter)

            for letter in state.getLetters():
                frequencyByLetter[letter] = -1

            # Retorna a letra com maior frequência
            letterChosen = max(frequencyByLetter, key=frequencyByLetter.get)
            return letterChosen

        else: # Caso o agente não conheça a palavra, usa o modelo n-gramas como heurística para adivinhar letras.

            if len(self.__words) > 0: # Usa o conhecimento total do agente para encontrar relações bigrama.
                if not self.__letterRelationsUpdated:
                    self.__letterRelationsUpdated = True
                    self.__letterRelationships()

                currentWord = "".join(state.getWord())
                currentWordWA = unidecode(currentWord)
                for i, letter in enumerate(currentWordWA):
                    try:
                        if letter == '_': #Algoritmo tenta adivinhar a primeira letra primeiro
                            if i == 0:
                                letterRelationsSorted = sorted(self.__firstLetterFrequency, key=self.__firstLetterFrequency.get, reverse=True)
                            
                            elif currentWord[i-1] != '_': # Se não for a primeira letra faltando, utiliza bigramas
                                letterRelationsSorted = sorted(self.__letterRelations[currentWordWA[i-1]], key=self.__letterRelations[currentWordWA[i-1]].get, reverse=True)
                            
                            else:
                                continue
                        
                            for letterFromRelations in letterRelationsSorted:
                                if letterFromRelations not in state.getLetters():
                                    return letterFromRelations
                    except Exception as e:
                        continue

            #Caso nenhum dos algoritmos acima seja possível, retorna uma letra aleatória
            return list(set(ABC).difference(state.getLetters()))[randint(0, 25 - len(state.getLetters()))]
