import random

# global list of player possibilities - can be extended iff matching class designed, and play will reflect new additions
playerOptions = ['Human', 'StupidBot', 'RandomBot', 'IterativeBot', 'LastPlayBot', 'MyBot']
# global variable for number of rounds to be played
NUM_ROUNDS = 5

class Game:
    """Game encapsulates game state, and non-input-required behaviour"""
    def __init__(self):
        """__init__ ensures references to player variables and sets their scores to 0"""
        self._player1 = None
        self._player2 = None
        self.resetScores()

    def getplayer1(self):
        """getplayer1 returns a reference to player 1"""
        return self._player1

    def getplayer2(self):
        """getplayer2 returns a reference to player 2"""
        return self._player2

    def choosePlayer(self, playerNum, playerSelection):
        """choosePlayer sets the specified player # to the specified player selection.
            It returns False if the player could not be set, and True if set successfully"""
        # checks playerSelection is valid, and assigns to local variable player
        if playerSelection not in range(1, len(playerOptions) + 1):
            return False
        else:
            player = eval(playerOptions[playerSelection-1] + '("' + playerOptions[playerSelection-1] + '")')
        #assigns player to correct player instance variable
        if playerNum == 1:
            self._player1 = player
            return True
        elif playerNum == 2:
            self._player2 = player
            return True
        else:
            return False

    def getScores(self):
        """getScores returns the score for each player"""
        return self._player1score, self._player2score

    def getPlayer1Score(self):
        """getPlayer1Score returns the score for player 1"""
        return self._player1score

    def getPlayer2Score(self):
        """getPlayer2Score returns the score for player 2"""
        return self._player2score    

    def playRound(self, player1move, player2move):
        """playRound executes the player's moves, increases the winner's score, and returns the round outcome"""
        # Use Element's compareTo method to get the outcome and the result string
        action, outcome = player1move.compareTo(player2move)
        if outcome == 'Win':
            self.addScore(1)
        elif outcome == 'Lose':
            self.addScore(2)
        return action, outcome

    def addScore(self, playerNum):
        """addScore adds one to the given player #'s score"""
        if playerNum == 1:
            self._player1score += 1
        elif playerNum == 2:
            self._player2score += 1

    def getResultString(self):
        """getResultString compares the scores and returns the game outcome"""
        if self._player1score > self._player2score:
            return 'Player 1 won the game!'
        elif self._player1score < self._player2score:
            return 'Player 2 won the game!'
        else:
            return 'Game was a draw!'

    # endGame exists in case client of Game wants to start a new game after finishing a game
    # this method is not required to fulfill the CSCI305 lab2 requirements, and is not used in the submission
    def endGame(self):
        """endGame resets the scores on game end"""
        self.resetScores()
        self._player1 = None
        self._player2 = None

    def resetScores(self):
        """resetScores sets both player scores to 0"""
        self._player1score = 0
        self._player2score = 0

    def getPlayerMoves(self):
        """getPlayerMoves calls the play method of the player instance variables, and ensures LastPlayBot is passed the opponent's move.
        Returns the player moves."""
        p1move, p2move = self._player1.play(), self._player2.play()
        if isinstance(self._player1, LastPlayBot):
            self._player1.rememberLast(p2move)
        if isinstance(self._player2, LastPlayBot):
            self._player2.rememberLast(p1move)
        return p1move, p2move

class Element:
    """Element is a representation of a Rock-Paper-Scissors-Lizard-Spock weapon choice"""
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self.name()
    def name(self):
        return self._name
    def compareTo(self, opponent):
        """compareTo compares this instance of an Element to another and returns an description string and outcome"""
        #all tie cases are handled the same
        if self.name() == opponent.name():
            return (self.name() + ' equals ' + opponent.name(), 'Tie')
        # builds an outcome dictionary and returns the value corresponding to the key (self.name(), opponent.name())
        # this needs to be modified if additional Element types are used (and moves below must reflect additional types
        # to select them). The outcomes are based on Player 1's perspective
        return {
            ('Rock', 'Paper') : ('Paper covers Rock', 'Lose'),
            ('Rock', 'Scissors') : ('Rock crushes Scissors', 'Win'),
            ('Rock', 'Lizard') : ('Rock crushes Lizard', 'Win'),
            ('Rock', 'Spock') : ('Spock vaporizes Rock', 'Lose'),

            ('Paper', 'Rock') : ('Paper covers Rock', 'Win'),
            ('Paper', 'Scissors') : ('Scissors cuts Paper', 'Lose'),
            ('Paper', 'Lizard') : ('Lizard eats Paper', 'Lose'),
            ('Paper', 'Spock') : ('Paper disproves Spock', 'Win'),
            
            ('Scissors', 'Rock') : ('Rock crushes Scissors', 'Lose'),
            ('Scissors', 'Paper') : ('Scissors cuts Paper', 'Win'),
            ('Scissors', 'Lizard') : ('Scissors decapitates Lizard', 'Win'),            
            ('Scissors', 'Spock') : ('Spock smashes Scissors', 'Lose'),

            ('Lizard', 'Rock') : ('Rock crushes Lizard', 'Lose'),
            ('Lizard', 'Paper') : ('Lizard eats Paper', 'Win'),
            ('Lizard', 'Scissors') : ('Scissors decapitates Lizard', 'Lose'),
            ('Lizard', 'Spock') : ('Lizard poisons Spock', 'Win'),

            ('Spock', 'Rock') : ('Spock vaporizes Rock', 'Win'),
            ('Spock', 'Paper') : ('Paper disproves Spock', 'Lose'),
            ('Spock', 'Scissors') : ('Spock smashes Scissors', 'Win'),
            ('Spock', 'Lizard') : ('Lizard poisons Spock', 'Lose'),
        }[self.name(), opponent.name()]

# global moves list, can be expanded (in conjunction with Element.compareTo(opponent)) to allow more moves
rock = Element('Rock')
paper = Element('Paper')
scissors = Element('Scissors')
lizard = Element('Lizard')
spock = Element('Spock')
moves = [rock, paper, scissors, lizard, spock]

class Player:
    """Player represents a player of the game"""
    def __init__(self, name):
        self._name = name
    def name(self):
        return self._name
    def play(self):
        raise NotImplementedError("Not yet implemented")

class StupidBot(Player):
    """StupidBot always plays rock. Because he's stupid."""
    def play(self):
        return moves[0]

class RandomBot(Player):
    """RandomBot plays pseudorandomly"""
    def play(self):
        return random.choice(moves)

class IterativeBot(Player):
    """Iterative plays the moves in order"""
    _currentSelection = -1
    def play(self):
        self._currentSelection += 1
        if self._currentSelection > len(moves) - 1:
            self._currentSelection = 0
        return moves[self._currentSelection]

class LastPlayBot(Player):
    """LastPlayBot plays a random move for the first round, and its opponent's 
    previous move in subsequent round. LastPlayBot.rememberLast(Element) must 
    always be called if this bot is in play, or it will act as a RandomBot"""
    def __init__(self, name):
        Player.__init__(self, name)
        self._firstMove = True
    def play(self):
        if self._firstMove:
            return random.choice(moves)
        return self._lastElement
    def rememberLast(self, element):
        self._lastElement = element
        self._firstMove = False

class MyBot(LastPlayBot):
    """MyBot extends LastPlayBot by returning a randomly selected element that could beat the previous element"""
    def __init__(self, name):
        LastPlayBot.__init__(self, name)
        
    def play(self):
        if self._firstMove == True:
            return random.choice(moves)
        else:
            return self.nextMove()

    def rememberLast(self, element):
        LastPlayBot.rememberLast(self, element)

    def nextMove(self):
        """Compares the opponent's previous move and selects a move that could beat the previous move"""
        if self._lastElement.name() == 'Rock':
            return Element(random.choice(['Rock', 'Paper', 'Spock']))
        elif self._lastElement.name() == 'Paper':
            return Element(random.choice(['Paper', 'Lizard', 'Scissors']))
        elif self._lastElement.name() == 'Scissors':
            return Element(random.choice(['Scissors', 'Spock', 'Rock']))
        elif self._lastElement.name() == 'Lizard':
            return Element(random.choice(['Lizard', 'Rock', 'Scissors']))
        elif self._lastElement.name() == 'Spock':
            return Element(random.choice(['Spock', 'Paper', 'Lizard']))
        # Should never happen, but fail gracefully
        else:
            return random.choice(moves)

class Human(Player):
    """Human represents a Human player. Its play method is only used for text-
    based interaction"""
    def play(self):
        """play provides a text prompt for move selection, and should not be used in other contexts"""
        for i in range(0, len(moves)):
            print('(' + str(i + 1) + ') : ' + moves[i].name())

        selection = input("Enter your move: ")
        while selection not in list(range(1, len(moves) + 1)):
            print("Invalid move. Please try again.")
            selection = input("Enter your move: ")
                
        return moves[selection - 1]

if __name__ == '__main__':
    print('Welcome to Rock, Paper, Scissors, Lizard, Spock, implemented by Tabetha Boushey and Jesse Brown\n')

    # game provides game state and behaviour
    game = Game()

    # prompts player selection and enumerates choices to console
    print('Please choose two players:')
    for i in range(1, len(playerOptions) + 1):
        print('\t(' + str(i) + ') ' + playerOptions[i-1])
    print('')

    # player selection process
    for player in (1, 2):
        selection = input("Select Player " + str(player) + ": ")
        while not game.choosePlayer(player, selection):
            print("Invalid selection. Please try again.")
            selection = input("Select Player " + str(player) + ": ")

    # player selection outcome
    print '\n' + game.getplayer1().name() + ' versus ' + game.getplayer2().name() + '. Go!\n'

    # plays NUM_ROUNDS rounds
    for roundNum in range(1, NUM_ROUNDS + 1):
        print('Round ' + str(roundNum) + ':')
        p1move, p2move = game.getPlayerMoves()
        print('Player 1 chose ' + p1move.name())
        print('Player 2 chose ' + p2move.name())
        action, outcome = game.playRound(p1move, p2move)
        print(action)
        # outcome reflects Player 1's perspective
        if outcome == 'Win':
            print('Player 1 won the round\n')
        elif outcome == 'Lose':
            print('Player 2 won the round\n')
        else:
            print('Round was a tie\n')

    print('\nThe score is ' + str(game.getPlayer1Score()) + ' to ' + str(game.getPlayer2Score()) + '.')
    print(game.getResultString())
