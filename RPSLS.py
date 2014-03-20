import random

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
            #gives all the possible outcomes for Rock being first
            ('Rock', 'Paper') : ('Paper covers Rock', 'Lose'),
            ('Rock', 'Scissors') : ('Rock crushes Scissors', 'Win'),
            ('Rock', 'Lizard') : ('Rock crushes Lizard', 'Win'),
            ('Rock', 'Spock') : ('Spock vaporizes Rock', 'Lose'),
            #gives all the possible outcomes for Paper being first
            ('Paper', 'Rock') : ('Paper covers Rock', 'Win'),
            ('Paper', 'Scissors') : ('Scissors cuts Paper', 'Lose'),
            ('Paper', 'Lizard') : ('Lizard eats Paper', 'Lose'),
            ('Paper', 'Spock') : ('Paper disproves Spock', 'Win'),
            #gives all the possible outcomes for Scissors being first
            ('Scissors', 'Rock') : ('Rock crushes Scissors', 'Lose'),
            ('Scissors', 'Paper') : ('Scissors cuts Paper', 'Win'),
            ('Scissors', 'Lizard') : ('Scissors decapitates Lizard', 'Win'),            
            ('Scissors', 'Spock') : ('Spock smashes Scissors', 'Lose'),
            #gives all the possible outcomes for Lizard being first
            ('Lizard', 'Rock') : ('Rock crushes Lizard', 'Lose'),
            ('Lizard', 'Paper') : ('Lizard eats Paper', 'Win'),
            ('Lizard', 'Scissors') : ('Scissors decapitates Lizard', 'Lose'),
            ('Lizard', 'Spock') : ('Lizard poisons Spock', 'Win'),
            #gives all the possible outcomes for Spock being first
            ('Spock', 'Rock') : ('Spock vaporizes Rock', 'Win'),
            ('Spock', 'Paper') : ('Paper disproves Spock', 'Lose'),
            ('Spock', 'Scissors') : ('Spock smashes Scissors', 'Win'),
            ('Spock', 'Lizard') : ('Lizard poisons Spock', 'Lose'),
        }[self.name(), opponent.name()]

# global list moves, containing a list of all moves
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

        selection = eval(input("Enter your move: "))
        while selection not in list(range(1, len(moves) + 1)):
            print("Invalid move. Please try again.")
            selection = eval(input("Enter your move: "))
                
        return moves[selection - 1]

class MyBot(Player):
    def play(self):
        return moves[0]

if __name__=='__main__':

    print(str(random.choice(moves)))
    print(str(random.choice(moves)))

    print('Welcome to Rock, Paper, Scissors, Lizard, Spock, implemented by Jesse Brown\n')

    print('Please choose two players:')
    print('\t(1) Human')
    print('\t(2) StupidBot')
    print('\t(3) RandomBot')
    print('\t(4) IterativeBot')
    print('\t(5) LastPlayBot')
    print('\t(6) MyBot')
    print('')

    selection1 = eval(input("Select Player 1: "))
    while selection1 not in list(range(1, 7)):
        print("Invalid selection. Please try again.")
        selection1 = eval(input("Select Player 1: "))

    selection2 = eval(input("Select Player 2: "))
    while selection2 not in list(range(1, 7)):
        print("Invalid selection. Please try again.")
        selection2 = eval(input("Select Player 2: "))

    #TODO: methodize this
    if selection1 == 1:
        p1 = Human('Jesse')
    elif selection1 == 2:
        p1 = StupidBot('StupidBot')
    elif selection1 == 3:
        p1 = RandomBot('RandomBot')
    elif selection1 == 4:
        p1 = IterativeBot('IterativeBot')
    elif selection1 == 5:
        p1 = LastPlayBot('LastPlayBot')
    else:
        p1 = MyBot("MyBot")

    if selection2 == 1:
        p2 = Human('Jesse2')
    elif selection2 == 2:
        p2 = StupidBot('StupidBot')
    elif selection2 == 3:
        p2 = RandomBot('RandomBot')
    elif selection2 == 4:
        p2 = IterativeBot('IterativeBot')
    elif selection2 == 5:
        p2 = LastPlayBot('LastPlayBot')
    else:
        p2 = MyBot("MyBot")

    print('\n' + p1.name() + ' versus ' + p2.name() + '. Go!\n')

    p1score = 0
    p2score = 0
    for roundNum in range(1, 6):
        print('Round ' + str(roundNum) + ':')
        p1move = p1.play()
        p2move = p2.play()
        if isinstance(p1, LastPlayBot):
            p1.rememberLast(p2move)
        if isinstance(p2, LastPlayBot):
            p2.rememberLast(p1move)
        print('Player 1 chose ' + p1move.name())
        print('Player 2 chose ' + p2move.name())
        action, outcome = p1move.compareTo(p2move)
        print(action)
        if outcome == 'Win':
            print('Player 1 won the round\n')
            p1score += 1
        elif outcome == 'Lose':
            print('Player 2 won the round\n')
            p2score += 1
        else:
            print('Round was a tie\n')

    print('\nThe score is ' + str(p1score) + ' to ' + str(p2score) + '.')
    if p1score > p2score:
        print('Player 1 won the game!')
    elif p1score < p2score:
        print('Player 2 won the game!')
    else:
        print('Game was a draw!')
