import pandas as pd
import numpy as np
import itertools
import random

data = pd.read_csv("Elo_System_Matrix.csv")
data = data.drop("Unnamed: 0", axis = 1)

#Defining Elo Boundaries
k = 10
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
        score = float(score) + float(1/(1 + 10**((Rb - Ra)/400)))
    return float(score)

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
    newScoreP1 = Ra + k*(actualscoreP1 - float(expectedP1))
    newScoreP2 = Rb + k*(actualscoreP2 - float(expectedP2))

    #print (str(newScoreP1) + ", " + str(newScoreP2))
    players[player1index][1] = newScoreP1
    players[player2index][1] = newScoreP2

    #print ("The new Elo for " + str(players[player1index][0]) + " is: " + str(newScoreP1))
    #print ("The new Elo for " + str(players[player2index][0]) + " is: " + str(newScoreP2))

#Get Total Sum of all ratings --> This is used to normalize as a Elo
#System is a zero-sum game
def getSum():
    sum = 0
    for x in players:
        sum = sum + float(x[1])
    return sum

#normalizes data so all elo's average to 1500
def normalize():
    sum = getSum()
    if float(sum/14) < elo_start:
        standard_diff = elo_start - float(sum/14)

    for i in range(len(players)):
        players[i][1] = float(players[i][1]) + float(standard_diff)

#simulates a Runthrough
def simulateGames(n):
    j = int(n/10)
    combinations = np.array(list(itertools.combinations(names, 2)))
    for b in range(j):
        for x in combinations:
            wins = 0
            losses = 0
            winfactor = matrix[x[0]].ix[findPlayer(x[1])]
            for l in range(10):
                if random.random() > winfactor:
                    wins += 1
                else:
                    losses += 1
            getElo(x[0],x[1], wins, losses)
        
        normalize()

        

simulateGames(10000)
print (players)



