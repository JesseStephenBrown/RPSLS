import wx
import wx.lib.statbmp
import random
import os
import RPSLS

# magic numbers
MIN = 0
MAX = 1
# these magic coords are based on drawing squares around the elements on the img,
# so clicks just outside the circle will be considered a move
SCISSORS_X = [208, 385]
SCISSORS_Y = [27, 203]
SPOCK_X = [22, 199]
SPOCK_Y = [161, 340]
LIZARD_X = [96, 274]
LIZARD_Y = [399, 569]
ROCK_X = [336, 510]
ROCK_Y = [392, 565]
PAPER_X = [402, 578]
PAPER_Y = [158, 338]
# Grid positions in (row, col)
START_POS = (1, 2)
BACKGROUND_POS = (2, 0)
LABEL_BAR_POS = (3, 0)
PLAYER_ONE_POS = (0, 0)
PLAYER_TWO_POS = (0, 4)
# Label status bar columns
P1_SCORE_COL = 0
P1_COL = 1
GAME_TEXT_COL = 2
P2_COL = 3
P2_SCORE_COL = 4
ROUND_COL = 5


class View(wx.Frame):
    """makes the frame of the GUI"""
    def __init__(self):
        # Passes relevant data to super constructor. Position is upperleft corner of client screen, style is a bitmask with no drag-to-resize available
        wx.Frame.__init__(self, None, -1, title="Rock Paper Scissors, Lizard, Spock", size=(100,100), pos=(0,0), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # View is actually a ViewController, so it needs an instance of game
        self.game = RPSLS.Game()
        self.buildWidgets()

    def buildWidgets(self):
        """builds the widgets used in the GUI"""
        # Build the window icon on platforms that support window icons
        img_path = os.path.abspath("./background.gif")
        self.SetIcon(wx.Icon(img_path, wx.BITMAP_TYPE_GIF))

        # Set the BG colour
        self.SetBackgroundColour("White")

        # establish a sizer - this holds/arranges all the components and is then added to the frame
        sizer = wx.GridBagSizer()

        # build player labels and choices
        self.buildPlayerSelections(sizer)

        # build start button and Bind its event
        self.startButton = wx.Button(self, -1, "Start the game!")
        sizer.Add(self.startButton, START_POS, (1,1,), wx.EXPAND)
        self.startButton.Bind(wx.EVT_BUTTON, self.OnStartButton)

        # build the play area image
        self.background = wx.Image("background.gif", wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.background = wx.lib.statbmp.GenStaticBitmap(self, -1, self.background)
        sizer.Add(self.background, BACKGROUND_POS, (1,5), wx.EXPAND)

        # build the upper status bar for status labels
        self.labelStatusBar = wx.StatusBar(self, -1)
        sizer.Add(self.labelStatusBar, LABEL_BAR_POS, (1,5), wx.EXPAND)

        # build the lower status bar for data
        self.statusBar = self.CreateStatusBar()

        # layout the status bars
        self.layoutStatusBars([self.labelStatusBar, self.statusBar])
        self.populateLabelStatusBar(self.labelStatusBar)

        # add sizer to frame and display
        self.SetSizerAndFit(sizer)
        self.Show(True)

    def OnStartButton(self, event):
        """On start button checks to see if the player has made valid player selections, then starts the game"""
        if self.validateOptions():
            for each in self.choices:
                each.Disable()
            self.startButton.Disable()
            self.labelStatusBar.SetStatusText('\n' + self.game.getplayer1().name() + ' vs ' + self.game.getplayer2().name() + '. Go!\n', GAME_TEXT_COL)
            self.statusBar.SetStatusText(str(0), P1_SCORE_COL)
            self.statusBar.SetStatusText(str(0), P2_SCORE_COL)
            self.statusBar.SetStatusText(str(0), ROUND_COL)

            # if neither player is human, round changing is handled by the next round button which takes over for the start button
            if not self.game.getplayer1().name() == "Human" and not self.game.getplayer2().name() == "Human":
                self.startButton.SetLabel("Next Round")
                self.startButton.Bind(wx.EVT_BUTTON, self.OnNextRound)
                self.startButton.Enable()
            # if one of the players is human, round changing is handled by clicking a move
            else:
                # bind click events to the frame
                self.background.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)


    def OnNextRound(self, event):
        """OnNextRound is an event handler bound only after successful player selection with non-human players"""
        self.statusBar.SetStatusText(str(eval(self.statusBar.GetStatusText(5)) + 1), ROUND_COL)
        if not isinstance(self.game.getplayer1(), RPSLS.Human) and not isinstance(self.game.getplayer2(), RPSLS.Human):
            p1move, p2move = self.game.getPlayerMoves()
            action, outcome = self.game.playRound(p1move, p2move)
            self.displayOutcome(action, outcome)

    def OnLeftClick(self, event):
        """OnLeftClick is an event handler bound only after successful player selection with a human player"""
        if self.game.getplayer1().name() == "Human":
            # calculate p1's move
            pos = event.GetPosition()
            p1move = self.getMoveByCoord(pos)
            # retrieve player 2's move
            if p1move:
                p2move = self.game.getplayer2().play()
                if isinstance(self.game.getplayer2(), RPSLS.LastPlayBot):
                    self.game.getplayer2().rememberLast(p1move)
            else:
                # if p1move not made successfully, p2move not made
                p2move = None
        else:
            # calculate p2's move
            pos = event.GetPosition()
            p2move = self.getMoveByCoord(pos)
            # retrieve player 1's move
            if p2move:
                p1move = self.game.getplayer1().play()
                if isinstance(self.game.getplayer1(), RPSLS.LastPlayBot):
                    self.game.getplayer1().rememberLast(p2move)
            else:
                # if p2move not made successfully, p1move not made
                p1move = None

        if p1move and p2move:
            # increment the round counter iff both plays have made their move
            self.statusBar.SetStatusText(str(eval(self.statusBar.GetStatusText(5)) + 1), ROUND_COL)
            action, outcome = self.game.playRound(p1move, p2move)
            self.displayOutcome(action, outcome)

    def OnPlayerOneSelection(self, event):
        """OnPlayerOneSelection handles selection events on the player one choice by setting
            the game instance's first player based on the selection made"""
        self.game.choosePlayer(1, self.choices[0].GetCurrentSelection() + 1)
        self.statusBar.SetStatusText(self.game.getplayer1().name(), P1_COL)

    def OnPlayerTwoSelection(self, event):
        """OnPlayerTwoSelection handles selection events on the player one choice by setting
            the game instance's second player based on the selection made"""
        self.game.choosePlayer(2, self.choices[1].GetCurrentSelection() + 1)
        self.statusBar.SetStatusText(self.game.getplayer2().name(), P2_COL)

    def getMoveByCoord(self, pos):
        """getMoveByCoord is a helper method that returns the Element corresponding to click location (pos) or None"""
        xPos, yPos = pos
        if xPos > ROCK_X[MIN] and xPos < ROCK_X[MAX] and yPos > ROCK_Y[MIN] and yPos < ROCK_Y[MAX]:
            return RPSLS.Element("Rock")
        elif xPos > PAPER_X[MIN] and xPos < PAPER_X[MAX] and yPos > PAPER_Y[MIN] and yPos < PAPER_Y[MAX]:
            return RPSLS.Element("Paper")
        elif xPos > SCISSORS_X[MIN] and xPos < SCISSORS_X[MAX] and yPos > SCISSORS_Y[MIN] and yPos < SCISSORS_Y[MAX]:
            return RPSLS.Element("Scissors")
        elif xPos > LIZARD_X[MIN] and xPos < LIZARD_X[MAX] and yPos > LIZARD_Y[MIN] and yPos < LIZARD_Y[MAX]:
            return RPSLS.Element("Lizard")
        elif xPos > SPOCK_X[MIN] and xPos < SPOCK_X[MAX] and yPos > SPOCK_Y[MIN] and yPos < SPOCK_Y[MAX]:
            return RPSLS.Element("Spock")
        return None

    def displayOutcome(self, action, outcome):
        self.labelStatusBar.SetStatusText(action, GAME_TEXT_COL)
        if outcome == "Win":
            self.statusBar.SetStatusText("Player 1 wins!", GAME_TEXT_COL)
            self.statusBar.SetStatusText(str(eval(self.statusBar.GetStatusText(0)) + 1), P1_SCORE_COL)
        elif outcome == "Lose":
            self.statusBar.SetStatusText("Player 2 wins!", GAME_TEXT_COL)
            self.statusBar.SetStatusText(str(eval(self.statusBar.GetStatusText(4)) + 1), P2_SCORE_COL)
        else:
            self.statusBar.SetStatusText("It was a tie!", GAME_TEXT_COL)

    def validateOptions(self):
        """validateOptions returns True iff both players are selected and at least one is non-human"""
        # If player 1 or player 2 has not been set:
        if self.game.getplayer1() == None or self.game.getplayer2() == None:
            return False
        # If player 1 is the same as player 2 and player 1 is human (which means player 2 is also)
        if self.game.getplayer1().name() == self.game.getplayer2().name() and self.game.getplayer1().name() == "Human":
            return False
        # If neither of the above tests match, then the player options are both valid
        return True

    def getPlayerData(self):
        """getPlayerData is a convenience method used to store the label, start position, and size of the player label and choices"""
        #        Player label   start  size
        return (("Player One:", PLAYER_ONE_POS, (1,1)),
                ("Player Two:", PLAYER_TWO_POS, (1,1)))

    def buildPlayerSelections(self, sizer):
        """buildPlayerSelections builds the labels and choice boxes for player selection"""
        self.choices = []
        # iterate through the player data from the helper method, and build a label and choice box for each
        for eachLabel, eachStart, eachSize in self.getPlayerData():
            sizer.Add(wx.StaticText(self, -1, eachLabel), eachStart, eachSize, wx.EXPAND)
            xStart, yStart = eachStart
            self.choices.append(wx.Choice(self, -1, choices=RPSLS.playerOptions))
            sizer.Add(self.choices[-1], (xStart+1, yStart), eachSize, wx.CENTER)
        # bind the choice boxes to their respective selection events
        self.choices[0].Bind(wx.EVT_CHOICE, self.OnPlayerOneSelection)
        self.choices[1].Bind(wx.EVT_CHOICE, self.OnPlayerTwoSelection)

    def layoutStatusBars(self, statusbars):
        for each in statusbars:
            each.SetFieldsCount(6)
            each.SetStatusWidths([-1, -2, -4, -2, -1, -1])

    def statusLabelData(self):
        """statusLabelData is a convenience method used to store the label and column of the label status bar fields"""
        return (("P1 Score", P1_SCORE_COL),
                ("Player One", P1_COL),
                ("Player Two", P2_COL),
                ("P2 Score", P2_SCORE_COL),
                ("Round", ROUND_COL))

    def populateLabelStatusBar(self, bar):
        """populateLabelStatusBar sets the labels on the labelStatusBar"""
        for eachLabel, eachCol in self.statusLabelData():
            bar.SetStatusText(eachLabel, eachCol)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = View()
    app.MainLoop()
