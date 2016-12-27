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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        food = currentGameState.getFood()
        score = 0.0

        # check whether pacman could eat food if he take this action
        for x in xrange(food.width):
            for y in xrange(food.height):
                if (food[x][y]):
                    distance = manhattanDistance((x, y), newPos)
                    if (distance == 0):
                        # take this action, pacman will eat food
                        score += 200.0
                    else:
                        score += 2.0 / (distance * distance)

        # check whether pacman could eat capsule if he take this action
        for capsule in currentGameState.getCapsules():
            distance = manhattanDistance(capsule, newPos)
            if(distance == 0):
                # take this step, pacman will eat a capsule
                score += 2000.0
            else:
                score += 20.0 / distance

        # check whether pacman will meet ghost if he take this action
        for ghost in newGhostStates:
            distance = manhattanDistance(ghost.getPosition(), newPos)
            if(distance <= 1):
                # take this step, pacman will have high probability to meet ghost
                if(ghost.scaredTimer != 0):
                    score += 4000.0
                else:
                    score -= 400.0

        return score
        # return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"
        v, action = self.maxValue(gameState, 0, self.depth)
        return action

    def maxValue(self, gameState, agent, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agent)
        v = list()
        for action in actions:
            v.append(self.minValue(gameState.generateSuccessor(self.index, action), 1, depth))
        bestV = max(v)
        actionIndex = -1
        for index in range(len(v)):
            if v[index] == bestV :
                actionIndex = index
                break
        return bestV, actions[actionIndex]

    def minValue(self, gameState, agent, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), "Stop"
        actions = gameState.getLegalActions(agent)
        v = list()
        if(agent != gameState.getNumAgents() - 1):
            # if this agent is not the last ghost
            for action in actions:
                v.append(self.minValue(gameState.generateSuccessor(agent, action), agent + 1, depth))
        else:
            # if this agent is the last ghost
            for action in actions:
                v.append(self.maxValue(gameState.generateSuccessor(agent, action), 0, (depth - 1)))
        bestV = min(v)
        actionIndex = -1
        for index in range(len(v)):
            if v[index] == bestV :
                actionIndex = index
                break
        return bestV, actions[actionIndex]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        a = -(float("inf"))
        b = float("inf")
        v = -(float("inf"))
        # v, action = self.maxValue(gameState, 0, self.depth, a, b)

        actions = gameState.getLegalActions(0)
        bestAction = Directions.STOP
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = v
            s = self.minValue(nextState, 1, self.depth, a, b)
            # print "s="+str(s)+" a="+str(a)+" b="+str(b)
            v = max(v, s)
            if v > prevscore:
                bestAction = action
            if v > b:
                return bestAction
            a = max(a, v)
        return bestAction

        # return action

    def maxValue(self, gameState, agent, depth, a, b):
        # print "max : gamestate="+str(gameState.state), " agent="+str(agent), " depth="+str(depth), " a="+str(a), " b="+str(b)
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agent)
        v = -(float("inf"))
        for action in actions:
            s = self.minValue(gameState.generateSuccessor(self.index, action), 1, depth, a, b)
            v = max(v, s)
            if v > b:
                return v
            a = max(a, v)
        return v

    def minValue(self, gameState, agent, depth, a, b):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agent)
        v = float("inf")
        if(agent != gameState.getNumAgents() - 1):
            # if this agent is not the last ghost
            for action in actions:
                s = self.minValue(gameState.generateSuccessor(agent, action), agent + 1, depth, a, b)
                v = min(v, s)
                if v < a:
                    return v
                b = min(b, v)
            return v
        else:
            # if this agent is the last ghost
            for action in actions:
                # v.append(self.maxValue(gameState.generateSuccessor(agent, action), 0, (depth - 1), a, b))
                s = self.maxValue(gameState.generateSuccessor(agent, action), 0, depth - 1, a, b)
                # print "s="+str(s)+" a="+str(a)+" b="+str(b)
                v = min(v, s)
                if v < a:
                    return v
                b = min(b, v)
            return v





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
        return self.getActionRecursive(gameState, self.depth, 0)[1]

    def getActionRecursive(self, gameState, depth, agent):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return (self.evaluationFunction(gameState), '')
        nextAgent = agent + 1
        if agent == gameState.getNumAgents() - 1:
            depth -= 1
            # if this one is the last agent, then next agent should be pacman
            nextAgent = 0
        if agent == 0:
            maxAlpha = -(float("inf"))
        else:
            maxAlpha = 0
        maxAction = ''
        actions = gameState.getLegalActions(agent)
        for action in actions:
            (evaluation, bestAction) = self.getActionRecursive(gameState.generateSuccessor(agent, action), depth, nextAgent)
            if agent == 0:
                # if agent is pacman
                maxAlpha = max(maxAlpha, evaluation)
                if maxAlpha == evaluation:
                    maxAction = action
            else:
                # if agent is ghost
                maxAlpha += 1.0 / len(actions) * evaluation
                maxAction = action
        return (maxAlpha, maxAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    evaluation = 0
    pacmanPosition = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    ghostPositions = currentGameState.getGhostPositions()
    minDistance = 10000
    # feature 1 is nearest food's distance
    foodDistances = [util.manhattanDistance(pacmanPosition, foodPosition) for foodPosition in foodPositions]
    if len(foodDistances) != 0:
        if min(foodDistances) < minDistance:
            minDistance = min(foodDistances)
            evaluation += minDistance
    # feature 2 is food's number
    evaluation += 10000 * currentGameState.getNumFood()
    # feature 3 is capsule's number
    evaluation += 100 * len(currentGameState.getCapsules())
    # feature 4 is nearest ghost's distance
    ghostDistances = [util.manhattanDistance(pacmanPosition, ghostPosition) for ghostPosition in ghostPositions]
    if len(ghostDistances) != 0:
        if min(ghostDistances) < 2:
            evaluation = 9999999999999999
    # feature 5 is current score
    evaluation -= 10 * currentGameState.getScore()
    return -(evaluation)

# Abbreviation
better = betterEvaluationFunction

