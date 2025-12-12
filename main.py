from src.Agent import Agent
from src.Environment import Environment
from src.State import State

if __name__ == "__main__":
    agent = Agent()
    env = Environment(5)

    agent.load("src/data/agent.txt") # Loading sabe data for both agent and environment
    env.load("src/data/words.txt")

    env.reset()
    agent.reset(env.getState().getWordLen())
    gameLoop = True

    while gameLoop: #Game loop
        actionValid = False
        while not actionValid:
            print(env)
            action = input("| (1) Guess | (2) Reset | (3) Exit |\n")
            print('')

            actionValid = action in ['1', '2', '3']

            if not actionValid:
                print("Invalid action.")

        match action:
            case '1': # Agents guess
                guess = agent.guess(env.getState())
                print(f"Agent's guess: '{guess}'")
                if env.step(guess):
                    print("Good guess!")
                else:
                    print("Wrong guess!")

            case '2':
                print("----------------------------------------\nGame has been reseted!\n----------------------------------------")
                env.reset()
                agent.reset(env.getState().getWordLen())

            case '3':
                break

        if not env.getRunning(): #Game ended
            if env.getGameSituation() == 1:
                print("Agent guessed the word!")
            else:
                print("Agent has lost the game!")

            realWord = env.getRealWord()
            agent.learn(realWord)
            print(f"Word: {realWord}")


            actionValid = False
            endMenu = True
            while endMenu:
                while not actionValid:
                    action = input("\n| (1) Reset | (2) Export agent data | (3) Export environment data | (4) Exit |\n")
                    actionValid = action in ['1', '2', '3', '4']
                match action:
                    case '1':
                        print("----------------------------------------\nGame has been reseted!\n----------------------------------------")
                        env.reset()
                        agent.reset(env.getState().getWordLen())
                        break

                    case '2':
                        agent.export('src/data/agent.txt')
                        print("Agent's knowledge exported succesfully!")
                        actionValid = False

                    case '3':
                        env.export('src/data/environment.txt')
                        print("Environment's data exported succesfully!")
                        actionValid = False

                    case '4':
                        gameLoop = False
                        break