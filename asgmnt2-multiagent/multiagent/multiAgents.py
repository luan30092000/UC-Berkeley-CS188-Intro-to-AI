# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        newGhostPosition = [ghostState.getPosition() for ghostState in newGhostStates]
        newGhostDistance = [manhattanDistance(ghostPos, newPos) for ghostPos in newGhostPosition]

        newFoodDistance = [manhattanDistance(foodPos, newPos) for foodPos in newFood.asList()]
        currentFoodPosition = currentGameState.getFood().asList()
        currentFoodDistance = [manhattanDistance(foodPos, newPos) for foodPos in currentFoodPosition]
        
        newCapsule = successorGameState.getCapsules()
        currentCapsule = currentGameState.getCapsules()
        newCapsuleDistance = [manhattanDistance(capsulePos, newPos) for capsulePos in newCapsule]
        currentCapsuleDistance = [manhattanDistance(capsulePos, newPos) for capsulePos in currentCapsule]

        if newPos in newGhostPosition and 0 in newScaredTimes:  # if newPos is in newGhostPosition
            return -1
        if 0 in currentFoodDistance:                            # if newPos is in currentfoodPos
            return 1
        
        if not (0 in newScaredTimes):
            return (min(newFoodDistance))**-18 + (min(newGhostDistance)**-1)    # account for chasing ghost
        
        # larger return value -> better, foodDistance increase, return value decrease, ghostDistance increase value decrease less 
        return (min(newFoodDistance))**-1 - (min(newGhostDistance))**-1
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, pacmanDepth):
            if pacmanDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = float("-inf")
            pacmanActions = gameState.getLegalActions(0)
            for action in pacmanActions:
                gameStateSuccessor = gameState.generateSuccessor(0, action)
                successorValue = minValue(gameStateSuccessor, pacmanDepth, 1)
                v = max(v, successorValue)   
            return v

        def minValue(gameState, ghostDepth, ghostIndex):
            if ghostDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = float("inf")
            ghostActions = gameState.getLegalActions(ghostIndex) 
            for action in ghostActions:
                gameStateSuccessor = gameState.generateSuccessor(ghostIndex, action)
                if ghostIndex < gameState.getNumAgents()-1:   # first to second last ghost to run
                    successorValue = minValue(gameStateSuccessor, ghostDepth, ghostIndex+1)
                    v = min(v, successorValue)
                else:   # last ghost -> pacman turn to run
                    successorValue = maxValue(gameStateSuccessor, ghostDepth+1)
                    v = min(v, successorValue)
            return v
        
        v = float("-inf")
        pacmanActions = gameState.getLegalActions(0)
        for action in pacmanActions:
            gameStateSuccessor = gameState.generateSuccessor(0, action)
            successorValue = minValue(gameStateSuccessor, 0, 1)
            if successorValue > v:
                v = successorValue
                returnAction = action
        return returnAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, pacmanDepth, alpha, beta):
            if pacmanDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = float("-inf")
            pacmanActions = gameState.getLegalActions(0)
            for action in pacmanActions:
                gameStateSuccessor = gameState.generateSuccessor(0, action)
                successorValue = minValue(gameStateSuccessor, pacmanDepth, 1, alpha, beta)
                v = max(v, successorValue)   
                if v > beta: return v
                alpha = max(alpha, v)
            return v

        def minValue(gameState, ghostDepth, ghostIndex, alpha, beta):
            if ghostDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = float("inf")
            ghostActions = gameState.getLegalActions(ghostIndex)
            for action in ghostActions:
                gameStateSuccessor = gameState.generateSuccessor(ghostIndex, action)
                if ghostIndex < gameState.getNumAgents()-1:   # first to second last ghost to run
                    successorValue = minValue(gameStateSuccessor, ghostDepth, ghostIndex+1, alpha, beta)
                    v = min(v, successorValue)
                else:   # last ghost -> pacman turn to run
                    successorValue = maxValue(gameStateSuccessor, ghostDepth+1, alpha, beta)
                    v = min(v, successorValue)
                if v < alpha: return v
                beta = min(beta, v)
            return v
        
        v = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        pacmanActions = gameState.getLegalActions(0)
        for action in pacmanActions:
            gameStateSuccessor = gameState.generateSuccessor(0, action)
            successorValue = minValue(gameStateSuccessor, 0, 1, alpha, beta)
            if successorValue > v:
                v = successorValue
                returnAction = action
                alpha = v
        return returnAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, pacmanDepth):
            if pacmanDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            v = float("-inf")
            pacmanActions = gameState.getLegalActions(0)
            for action in pacmanActions:
                gameStateSuccessor = gameState.generateSuccessor(0, action)
                successorValue = expectedValue(gameStateSuccessor, pacmanDepth, 1)
                v = max(v, successorValue)   
            return v

        def expectedValue(gameState, ghostDepth, ghostIndex):
            if ghostDepth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            sumSuccessorValue = 0
            ghostActions = gameState.getLegalActions(ghostIndex)
            for action in ghostActions:
                gameStateSuccessor = gameState.generateSuccessor(ghostIndex, action)
                if ghostIndex < gameState.getNumAgents()-1:   # first to second last ghost to run
                    sumSuccessorValue += expectedValue(gameStateSuccessor, ghostDepth, ghostIndex+1)
                else:   # last ghost -> pacman turn to run
                    sumSuccessorValue += maxValue(gameStateSuccessor, ghostDepth+1)    
            return sumSuccessorValue / len(ghostActions)
        
        v = float("-inf")
        for action in gameState.getLegalActions(0):
            gameStateSuccessor = gameState.generateSuccessor(0, action)
            successorValue = expectedValue(gameStateSuccessor, 0, 1)
            if successorValue > v:
                v = successorValue
                returnAction = action
        return returnAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    currentPos = currentGameState.getPacmanPosition()
    currentFoodPositions = currentGameState.getFood().asList()

    currentGhostStates = currentGameState.getGhostStates()

    currentGhostDistances = [manhattanDistance(currentPos, aCurrentGhostState.getPosition()) for aCurrentGhostState in currentGhostStates]
    currentFoodDistances = [manhattanDistance(currentPos, aCurrentFoodPosition) for aCurrentFoodPosition in currentFoodPositions]

    if 0 in currentGhostDistances:
        return -1
    
    ghostValue = max(currentGhostDistances)**-1 if currentGhostDistances else 0
    foodValue = max(currentFoodDistances)**-1 if currentFoodDistances else 0
    
    return foodValue + ghostValue + currentGameState.getScore()
    
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
