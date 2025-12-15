from src.Agent import Agent
from src.Environment import Environment
from src.State import State

if __name__ == "__main__":
    agent = Agent()
    env = Environment("", 5)

    agent.load("src/data/agent.txt") # Carregando conhecimento do agente
    env.load("src/data/words.txt") # Carregando palavras do ambiente

    #Reseta as variáveis do ambiente e do agente
    env.reset()
    agent.reset(env.getState().getWordLen())
    gameLoop = True

    # Loop principal
    while gameLoop:
        actionValid = False
        while not actionValid:
            print(env) # Visualização do estado atual
            action = input("| (1) Guess | (2) Reset | (3) Exit |\n") # Menu de ações
            print('')

            actionValid = action in ['1', '2', '3']

            if not actionValid:
                print("Invalid action.")

        match action:
            case '1': # Ação de palpite
                guess = agent.guess(env.getState()) # Agente percebe o ambiente e realiza um palpite
                print(f"Agent's guess: '{guess}'") # Palpipe pode ser tanto uma palavra quanto uma letra
                if env.step(guess): # Ambiente atualiza o estado e retorna resultado do palpite
                    print("Good guess!") 
                else:
                    print("Wrong guess!")

            case '2': # Ação de reset
                print("----------------------------------------\nGame has been reseted!\n----------------------------------------")
                env.reset() # Ambiente escolhe uma palavra nova
                agent.reset(env.getState().getWordLen()) # Agente percebe a palavra nova

            case '3':
                break

        if not env.getRunning(): # Jogo finalizado
            if env.getGameSituation() == 1:
                print("Agent guessed the word!")
            else:
                print("Agent has lost the game!")

            realWord = env.getRealWord() # Ambiente revela palavra real
            agent.learn(realWord) # Agente percebe a palavra real e aprende
            print(f"Word: {realWord}")


            actionValid = False
            endMenu = True
            while endMenu: # Menu de fim de jogo
                while not actionValid:
                    action = input("\n| (1) Reset | (2) Export agent data | (3) Export environment data | (4) Exit |\n")
                    actionValid = action in ['1', '2', '3', '4']
                match action:
                    case '1': # Reseta o jogo 
                        print("----------------------------------------\nGame has been reseted!\n----------------------------------------")
                        env.reset()
                        agent.reset(env.getState().getWordLen())
                        break

                    case '2': # Exportar dados do agente
                        agent.export('src/data/agent.txt')
                        print("Agent's knowledge exported succesfully!")
                        actionValid = False

                    case '3': # Exportar dados do ambiente
                        env.export('src/data/environment.txt')
                        print("Environment's data exported succesfully!")
                        actionValid = False

                    case '4': # Finaliza o programa
                        gameLoop = False
                        break