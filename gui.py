import Tkinter as tk

class Application(tk.Frame):
    """docstring for Appliction"""

    spockID = ''

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
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

if __name__ == '__main__':
    app = Application()
    app.master.title('Rock Paper Scissors Lizard Spock')
    app.mainloop()


#Rock is    #ff8181
#Paper is   #ffdb4d
#Scissors is#e47dff
#Spock is   #83b8ff
#Lizard is  #93e393

