import pandas as pd
import numpy as np

data = pd.read_csv("Elo_System_Matrix.csv")
data = data.drop("Unnamed: 0", axis = 1)

#Defining Elo Boundaries
k = 30
elo_start = 1500

#Create a correlation matrix of winning/losing 
#Probabilities between players
def createCorrelationMatrix(data): 
    for i in range(len(data)):
        for j in range(len(data.ix[i])):
            if (pd.isnull(data.iloc[i,j])):
                data.ix[i,j] = 1 - data.ix[j,i] 
    
    return data

matrix = createCorrelationMatrix(data)
names = np.array(matrix.columns)
startratings = [elo_start] * len(matrix.columns)
players = np.array(list(zip(names, startratings)))

#ExpectedScore from multiple plays
def getExpectedScore(Ra, Rb, games):
    score = 0
    for i in range(games):
        score = score + 1/(1 + 10**((Rb - Ra)/400))
    return score

#Finds Player given Player Name
def findPlayer(playername):
    return matrix.columns.get_loc(playername)

#Get Elo of a Player
def getElo(player1, player2, wins, losses):
    player1index = findPlayer(player1)
    player2index = findPlayer(player2)

    gamesplayed = wins + losses

    Ra = float(players[player1index][1])
    Rb = float(players[player2index][1])

    actualscoreP1 = 1 * wins
    actualscoreP2 = 1 * losses

    expectedP1 = getExpectedScore(Ra, Rb, gamesplayed)
    expectedP2 = getExpectedScore(Rb, Ra, gamesplayed)
    

    #print (str(Ra) + ", " + str(Rb) + ", " + str(expectedP1) + ", " + str(expectedP2))
    newScoreP1 = round(Ra + k*(actualscoreP1 - expectedP1),2)
    newScoreP2 = round(Ra + k*(actualscoreP2 - expectedP2),2)

    #print (str(newScoreP1) + ", " + str(newScoreP2))
    players[player1index][1] = newScoreP1
    players[player2index][1] = newScoreP2

    print ("The new Elo for " + str(players[player1index][0]) + " is: " + str(newScoreP1))
    print ("The new Elo for " + str(players[player2index][0]) + " is: " + str(newScoreP2))



getElo("Mesh", "Trot", 10, 10)
getElo("LP", "Mesh", 17, 4)




