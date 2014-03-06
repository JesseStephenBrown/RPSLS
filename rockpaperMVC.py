import wx
import random
import os

playerOptions = ['Human', 'StupidBot', 'RandomBot', 'IterativeBot', 'LastPlayBot', 'MyBot']
numRounds = 5

class Game:

    def __init__(self):
        self._player1 = None
        self._player2 = None
        self.resetScores()

    def getplayer1(self):
        return self._player1

    def getplayer2(self):
        return self._player2

    def choosePlayer(self, playerNum, playerSelection):
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
        return self._player1score, self._player2score

    def getPlayer1Score(self):
        return self._player1score

    def getPlayer2Score(self):
        return self._player2score    

    def playRound(self, player1move, player2move):
        action, outcome = player1move.compareTo(player2move)
        if outcome == 'Win':
            self.addScore(1)
        elif outcome == 'Lose':
            self.addScore(2)

        return action, outcome

    def addScore(self, playerNum):
        if playerNum == 1:
            self._player1score = self._player1score + 1
        elif playerNum == 2:
            self._player2score = self._player2score + 1

    def getResultString(self):
        if self._player1score > self._player2score:
            return 'Player 1 won the game!'
        elif self._player1score < self._player2score:
            return 'Player 2 won the game!'
        else:
            return 'Game was a draw!'

    def endGame(self):
        self.resetScores()

    def resetScores(self):
        self._player1score = 0
        self._player2score = 0

    def play(self):
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
    def play(self):
        return moves[0]

class RandomBot(Player):
    def play(self):
        return random.choice(moves)

class IterativeBot(Player):
    _currentSelection = -1
    def play(self):
        self._currentSelection += 1
        if self._currentSelection > len(moves) - 1:
            self._currentSelection = 0
        return moves[self._currentSelection]

class LastPlayBot(Player):
    _firstMove = True
    def play(self):
        if self._firstMove:
            return random.choice(moves)
        return self._lastElement
    def rememberLast(self, element):
        self._lastElement = element
        self._firstMove = False

class Human(Player):
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

class App(wx.App):

    def __init__(self):
        wx.App.__init__(self)

    def OnInit(self):
        self.view = View()
        self.controller = Controller(self.view)
        self.SetTopWindow(self.view)
        return True

class View(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Rock Paper Scissors, Lizard, Spock", size=(100,100), pos=(100,100), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.buildWidgets()

    def buildWidgets(self):

        img_path = os.path.abspath("./background.gif")
        self.SetIcon(wx.Icon(img_path, wx.BITMAP_TYPE_GIF))

        sizer = wx.GridBagSizer()

        self.player1Label = wx.StaticText(self, -1, "Player One: ")
        sizer.Add(self.player1Label, (0,0), (1,1), wx.EXPAND)

        self.player1choice = wx.Choice(self, -1, choices=playerOptions)
        sizer.Add(self.player1choice, (1, 0), (1,1), wx.EXPAND)

        self.player2Label = wx.StaticText(self, -1, "Player Two: ")
        sizer.Add(self.player2Label, (0,4), (1,1))

        self.player2choice = wx.Choice(self, -1, choices=playerOptions)
        sizer.Add(self.player2choice, (1, 4), (1,1), wx.EXPAND)

        self.startButton = wx.Button(self, -1, "Start the game!")
        sizer.Add(self.startButton, (1,2), (1,1,), wx.EXPAND)

        self.background = wx.Image("background.gif", wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.background = wx.StaticBitmap(self, -1, self.background)
        sizer.Add(self.background, (2,0), (1,5), wx.EXPAND)

        self.statusBar = wx.StatusBar(self, -1)
        sizer.Add(self.statusBar, (3,0), (1,5), wx.EXPAND)

        self.SetSizerAndFit(sizer)
        self.Show(True)

class Controller:

    def __init__(self, view):
        self._game = Game()
        self._view = view

    def validateOptions(self, player1, player2):
        if player1 == "Human" and player2 == "Human":
            return False
        return True

    def choosePlayer(self, event):
        pass

    def chooseMove(self, event):
        pass

if __name__ == '__main__':
    app = App()
    app.MainLoop()

# if __name__ == '__main__':
#     print len(playerOptions)
#     print('Welcome to Rock, Paper, Scissors, Lizard, Spock, implemented by Tabetha Boushey and Jesse Brown\n')

#     game = Game()

#     print('Please choose two players:')
#     for i in range(1, len(playerOptions) + 1):
#         print('\t(' + str(i) + ') ' + playerOptions[i-1])
#     print('')

#     selection = input("Select Player 1: ")
#     while not game.choosePlayer(1, selection):
#         print("Invalid selection. Please try again.")
#         selection = input("Select Player 1: ")

#     selection = input("Select Player 2: ")
#     while not game.choosePlayer(2, selection):
#         print("Invalid selection. Please try again.")
#         selection = input("Select Player 2: ")

#     print '\n' + game.getplayer1().name() + ' versus ' + game.getplayer2().name() + '. Go!\n'

#     for roundNum in range(1, numRounds + 1):
#         print('Round ' + str(roundNum) + ':')
#         p1move, p2move = game.play()
#         print('Player 1 chose ' + p1move.name())
#         print('Player 2 chose ' + p2move.name())
#         action, outcome = game.playRound(p1move, p2move)
#         print(action)
#         if outcome == 'Win':
#             print('Player 1 won the round\n')
#         elif outcome == 'Lose':
#             print('Player 2 won the round\n')
#         else:
#             print('Round was a tie\n')

#     print('\nThe score is ' + str(game.getPlayer1Score()) + ' to ' + str(game.getPlayer2Score()) + '.')
#     print(game.getResultString())
#     game.endGame()