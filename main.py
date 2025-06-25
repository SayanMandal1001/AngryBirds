from Scripts import Game
from Scripts import MainMenu

def storeGame(playerNames,scores):
    with open("Data/GameHistory.csv",'r') as file:
        data=file.read().split()
        line = playerNames[0] + "," + str(scores[0]) + "," + playerNames[1] + "," + str(scores[1])
        data.insert(0,line)
        dataStr=""
        for i in range(0,len(data)):
            if(i<10):
                dataStr+=data[i] + "\n"
    with open("Data/GameHistory.csv",'w') as file:
        file.write(dataStr)

RC=1
MainMenu.changeResolutionConstant(RC)
Game.changeResolutionConstant(RC)
quit=False
while(not quit):
    startGame = MainMenu.titleScreen()
    quit=MainMenu.quit
    if(startGame==1):
        playAgain=True
        while(playAgain):
            playerName,settingVals=MainMenu.gameSettings()
            if(not MainMenu.mainMenu):
                if(not MainMenu.quit):
                    MainMenu.loadingScreen()
                    if(not MainMenu.quit):
                        playerNames,scores,winner,playAgain=Game.game(playerName,settingVals)
                        storeGame(playerNames,scores)
                    else:
                        quit=MainMenu.quit
                        break
                else:
                    quit=MainMenu.quit
                    break
            else:
                break
    elif(startGame==2):
        MainMenu.gameHistory()
        quit=MainMenu.quit
    else:
        break