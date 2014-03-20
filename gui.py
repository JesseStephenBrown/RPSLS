import Tkinter as tk
import random

class Game:

    def __init__(self):
        """initializes self for player 1 and 2"""
        self._player1 = None
        self._player2 = None
        self.resetScores()

    def getplayer1(self):
        """gets player 1"""
        return self._player1

    def getplayer2(self):
        """gets player 2"""
        return self._player2

    def choosePlayer(self, playerNum, playerSelection):
        """chooses the player"""
        if playerSelection not in range(1, len(playerOptions) + 1):
            return False
        else:
            player = eval(playerOptions[playerSelection-1] + '("' + playerOptions[playerSelection-1] + '")')

        if playerNum == 1:
            self._player1 = player
            return True
        elif playerNum == 2:
            self._player2 = player
            return True
        else:
            return False

    def getScores(self):
        """gets the score for each player"""
        return self._player1score, self._player2score

    def getPlayer1Score(self):
        """gets the score for player 1"""
        return self._player1score

    def getPlayer2Score(self):
        """gets the score for player 2"""
        return self._player2score    

    def playRound(self, player1move, player2move):
        """plays the round"""
        action, outcome = player1move.compareTo(player2move)
        if outcome == 'Win':
            self.addScore(1)
        elif outcome == 'Lose':
            self.addScore(2)

        return action, outcome

    def addScore(self, playerNum):
        """adds to the score"""
        if playerNum == 1:
            self._player1score = self._player1score + 1
        elif playerNum == 2:
            self._player2score = self._player2score + 1

    def getResultString(self):
        """tells you who one the game"""
        if self._player1score > self._player2score:
            return 'Player 1 won the game!'
        elif self._player1score < self._player2score:
            return 'Player 2 won the game!'
        else:
            return 'Game was a draw!'

    def endGame(self):
        """end of the game"""
        self.resetScores()

    def resetScores(self):
        """resets the score of each player"""
        self._player1score = 0
        self._player2score = 0

    def getPlayerMoves(self):
        """get the moves for the player"""
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
    """returns the first move"""
    def play(self):
        return moves[0]

class RandomBot(Player):
    """randomly chooses the move"""
    def play(self):
        return random.choice(moves)

class IterativeBot(Player):
    """iteratively chooses the next move"""
    _currentSelection = -1
    def play(self):
        self._currentSelection += 1
        if self._currentSelection > len(moves) - 1:
            self._currentSelection = 0
        return moves[self._currentSelection]

class LastPlayBot(Player):
    """does the last play of the game"""
    _firstMove = True
    def play(self):
        if self._firstMove:
            return random.choice(moves)
        return self._lastElement
    def rememberLast(self, element):
        self._lastElement = element
        self._firstMove = False

class Human(Player):
    """lets the human choose their move"""
    def play(self):
        for i in range(0, len(moves)):
            print('(' + str(i + 1) + ') : ' + moves[i].name())

        selection = input("Enter your move: ")
        while selection not in list(range(1, len(moves) + 1)):
            print("Invalid move. Please try again.")
            selection = input("Enter your move: ")
                
        return moves[selection - 1]

class MyBot(Player):
    def play(self):
        return moves[0]

class Controller(object):

    def __init__(self, game):
        self._game = game

    def setView(self, view):
        self._view = view

    def validateOptions(self, player1, player2):
        if player1 == None or player2 == None:
            return True
        if player1 == "Human" and player2 == "Human":
            return False
        return True

    def choosePlayerOne(self, event):
        if self.validateOptions(game.getplayer1, game.getplayer2):
            self._game.choosePlayer(1, event.widget.getvar(self._view.player1var).get())
        else:
            event.widget.set('StupidBot')

    def chooseMove(self, event):
        pass        
        
class View(tk.Frame):
    """Docstring for Application"""

    def __init__(self, controller, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.controller = controller
        self.createWidgets()

    def createWidgets(self):
        #labels
        self.playerOneLabel = tk.Label(self, text='Player One')
        self.playerOneLabel.grid(row=0, column=0)

        self.playerTwoLabel = tk.Label(self, text='Player Two')
        self.playerTwoLabel.grid(row=0, column=4)

        # List of potential players
        playerList = ('Human', 'StupidBot', 'RandomBot', 'IterativeBot', 'LastPlayBot', 'MyBot')
        
        self.player1var = tk.StringVar()
        self.player1var.set(playerList[0])
        self.player2var = tk.StringVar()
        self.player2var.set(playerList[0])
        
        self.player1option = tk.OptionMenu(self, self.player1var, *playerList)
        self.player1option.grid(row=1, column=0)
        self.player1option.bind("<ButtonRelease-1>", self.controller.choosePlayerOne) 

        self.player2option = tk.OptionMenu(self, self.player2var, *playerList)
        self.player2option.grid(row=1, column=4)

        self.startButton = tk.Button(self, text="Start", state="disabled")
        self.startButton.grid(row=1, column=2)

        self.canvas = tk.Canvas(self, background="white", width="600", height="600")
        self.backgroundImage = tk.PhotoImage(file="background.gif")

        self.photoid = self.canvas.create_image(300,300, image=self.backgroundImage)
        self.spockID = self.canvas.create_oval(30, 170, 191, 338, outline="#83b8ff", width=0)
        self.paperID = self.canvas.create_oval(409,168,568,328, outline="#ffdb4d", width=0)
        self.scissorsID = self.canvas.create_oval(213, 35, 374, 194, outline="#e47dff", width=0)
        self.lizardID = self.canvas.create_oval(106, 405, 267, 564, outline="#93e393", width=0)
        self.rockID = self.canvas.create_oval(339, 401, 499, 564, outline="#ff8181", width=0)

        self.canvas.tag_bind(self.spockID, '<ButtonPress-1>', self.onObjectClick)
        self.canvas.tag_bind(self.paperID, '<ButtonPress-1>', self.onObjectClick)
        self.canvas.tag_bind(self.scissorsID, '<ButtonPress-1>', self.onObjectClick)
        self.canvas.tag_bind(self.lizardID, '<ButtonPress-1>', self.onObjectClick)
        self.canvas.tag_bind(self.rockID, '<ButtonPress-1>', self.onObjectClick)

        self.canvas.grid(row=2, columnspan=5)

        self.resultsBox = tk.Label(self, text="Results go here")
        self.resultsBox.grid(row=3, column=2)

    def onObjectClick(self, event):
        #event.widget.find_closest(event.x, event.y).configure(width=20)
        for cobject in (self.canvas.find_all()):
            if cobject != self.photoid:
                self.canvas.itemconfig(cobject, width=0)
        self.canvas.itemconfig(event.widget.find_closest(event.x, event.y), width=20)
        
    def setController(self, controller):
        """setController saves an instance of Controller to instance variable controller, or returns a type error is controller is not a Controller"""
        if isinstance(controller, Controller):
            self.controller = controller
        else:
            raise TypeError("Requires instance of Controller, not instance of " + controller.__class__.__name__)

    def toggleStartButton(self):
        """toggleStartButton toggles the state between disabled and enabled"""

if __name__ == '__main__':
    game = Game()
    controller = Controller(game)
    app = View(controller)
    controller.setView(app)
    app.master.title('Rock Paper Scissors Lizard Spock')
    app.mainloop()
