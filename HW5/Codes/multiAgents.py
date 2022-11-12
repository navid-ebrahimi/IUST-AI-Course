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
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        Foods = successorGameState.getFood()
        GhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in GhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        if action == 'Stop':
            score -= 60
        GhostStatesScore = 999999
        for ghostState in GhostStates:
            if (manhattanDistance(newPos, ghostState.configuration.pos) < GhostStatesScore):
                GhostStatesScore = manhattanDistance(newPos, ghostState.configuration.pos)
        FoodScore = 999999
        for food in Foods.asList():
            if (manhattanDistance(newPos, food) < FoodScore):
                FoodScore = manhattanDistance(newPos, food)

        score += successorGameState.getScore() + (GhostStatesScore*3) / (FoodScore*10)
        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0


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
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        self.nodesCount = 0
        score, situation = self.minimax(gameState, 0, 0)
        return situation

    def minimax(self, gameState, agentIndex, depth):
        self.nodesCount += 1
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        best_score, best_action, best_move = None, None, None
        
        if (agentIndex == 0): # max player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.minimax(successorGameState, agentIndex + 1, depth)
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = legalmove
        else: # min player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.minimax(successorGameState, agentIndex + 1, depth)
                if best_score is None or score < best_score:
                    best_score = score
                    best_action = legalmove
        if best_score is None:
            return self.evaluationFunction(gameState), None
        return best_score, best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        self.nodesCount = 0
        score, situation = self.alphabeta(gameState, 0, 0, None, None)
        return situation

    def alphabeta(self, gameState, agentIndex, depth, a, b):
        self.nodesCount += 1
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        legalMoves = gameState.getLegalActions(agentIndex)
        best_score, best_action, best_move = None, None, None
        
        if (agentIndex == 0): # max player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.alphabeta(successorGameState, agentIndex + 1, depth, a, b)
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = legalmove
                if (b is not None and best_score > b):
                    return best_score, best_action
                if (a is None):
                    a = best_score
                else:
                    a = max(a, best_score)
        else: # min player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.alphabeta(successorGameState, agentIndex + 1, depth, a, b)
                if best_score is None or score < best_score:
                    best_score = score
                    best_action = legalmove
                    
                if (a is not None and best_score < a):
                    return best_score, best_action
                if (b is None):
                    b = best_score
                else:
                    b = min(b, best_score)
        if best_score is None:
            return self.evaluationFunction(gameState), None
        return best_score, best_action

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
        self.nodesCount = 0
        score, situation = self.Expectimax(gameState, 0, 0)
        return situation

    def Expectimax(self, gameState, agentIndex, depth):
        self.nodesCount += 1
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), None
        
        legalMoves = gameState.getLegalActions(agentIndex)
        best_score, best_action, best_move = None, None, None
        
        if (agentIndex == 0): # max player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.Expectimax(successorGameState, agentIndex + 1, depth)
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = legalmove
        else: # min player
            for legalmove in legalMoves:
                successorGameState = gameState.generateSuccessor(agentIndex, legalmove)
                score, best_move = self.Expectimax(successorGameState, agentIndex + 1, depth)
                if best_score is None:
                    best_score = score
                else:
                    best_score += score
            best_score /= len(legalMoves)
        if best_score is None:
            return self.evaluationFunction(gameState), None
        return best_score, best_action


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return 999999
    if currentGameState.isLose():
        return -999999
    score = currentGameState.getScore()
    foodListPositions = currentGameState.getFood().asList()
    ghost_States = currentGameState.getGhostStates()
    circleList_Position = currentGameState.getCapsules()
    pac_Position = currentGameState.getPacmanPosition()
    ghost_Posistion = currentGameState.getGhostPositions()
    for ghost_State in ghost_States:
        if ghost_State.scaredTimer > 0:
            score += 50
        else:
            score -= 50
    for ghost in ghost_Posistion:
        if manhattanDistance(pac_Position, ghost) <= 1:
            score -= 1000
    food_score = 0
    for food in foodListPositions:
        food_score += manhattanDistance(pac_Position, food)
    circle_score = 0
    for circle in circleList_Position:
        circle_score += manhattanDistance(pac_Position, circle)
    try:
        score += 5/food_score
        score += 15/circle_score
    except:
        pass
    return score


# Abbreviation
better = betterEvaluationFunction
