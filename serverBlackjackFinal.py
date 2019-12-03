import socket
import random

# Card class
class Card:
    # Constructor for card class
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    # Prints a card
    def printCards(self):
        return "\n{} of {}".format(self.value, self.suit)

    # Returns card value
    def getValue(self):
        return self.value

    # Sets card value
    def setValue(self, x):
        self.value = x

class Deck:
    # Constructor for deck class
    def __init__(self):
        self.cards = []
        self.generateDeck()

    # Generates all 52 cards with correct rank and value
    def generateDeck(self):
        for i in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for j in "Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King".split(", "):
                self.cards.append(Card(i, j))

    # Prints the cards in a given hand
    def printCards(self):
        for c in self.cards:
            c.printCards()

    # Shuffles the deck
    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    # Draws a card into a hand
    def drawCard(self):
        return self.cards.pop()

class Player:
    # Constructor for player class
    def __init__(self, name):
        self.name = name
        self.hand = []

    # Sets name of player
    def setName(self, name):
        self.name = name

    # Returns name of player
    def getName(self):
        return self.name

    # Draws from deck and puts into player hand
    def draw(self, deck):
        self.hand.append((deck.drawCard()))

    # Show all cards from both dealer and player
    def showHandPlayer(self):
        output = ''
        i = -1
        for i in range(len(self.hand)):
            output += self.hand[i].printCards()
            i += 1
        return output

    # Shows one card face up and one face down for dealer
    def showHandDealer(self):
        return "{}\nFACE DOWN".format(self.hand[-1].printCards())

    # Calculates the score of the hand based upon the value of the cards in hand
    def calcScore(self):
        value = 0
        for card in self.hand:
            if card.getValue() == "King" or card.getValue() == "Queen" or card.getValue() == "Jack":
                value += 10
            elif card.getValue() == "Ace":
                if (value + 11) <= 21:
                    value += 11
                elif (value + 11) > 21:
                    value += 1
            else:
                value += int(card.getValue())
        return value

# Compares the value returning 1,0,-1
def cmp(a, b):
    return (a > b) - (a < b)

# Prints out the hand of both player and dealer. Dealer has a face down card.
def showSome(player, dealer):
    return "_____________________\nDealer Hand: {} \n_____________________\nPlayer Hand: {}\n" \
           "Total: {}\n_____________________ \n\nHit or Stand?".format(
            dealer.showHandDealer(), player.showHandPlayer(), player.calcScore())

# Prints out the hand of both player and dealer.
def showAll(player, dealer):
    return "_____________________\nDealer Hand: {} \nTotal: {}\n_____________________\nPlayer Hand: {}\n" \
           "Total: {}\n_____________________ \n".format(
            dealer.showHandPlayer(), dealer.calcScore(), player.showHandPlayer(), player.calcScore())

# IP address for the server host
host = '10.220.25.180' #socket.gethostname()
# Server port to get access
serverPort = 5000

# Creates deck
deck = Deck()
deck.shuffle()

# Dealer draws 2 cards
dealer = Player("Dealer")
dealer.draw(deck)
dealer.draw(deck)

# Player draws 2 cards
player = Player('Player 1')
player.draw(deck)
player.draw(deck)

# TCP server socket connection
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(2)

print('BlackJack started.')

# Loop to transfer data between client and server
while True:
    # Connects
    connectionSocket, addr = serverSocket.accept()

    # Prints player and dealer hand
    show = str(showSome(player, dealer))
    print("Initial Hand\n" + show)

    # Prints player IP address
    print('Player = ' + addr[0] + ':' + str(addr[1]))
    sentence = connectionSocket.recv(1024).decode()

    # Starts game and sends data
    if sentence == 'play':
        connectionSocket.send(show.encode())

    # If client sends "hit"
    if sentence == 'hit':
        player.draw(deck)
        # If the player score is over 21, then player busted
        if player.calcScore() > 21:
            show = str(showAll(player, dealer))
            print(show)
            message =  show + "\nPlayer Busted, Game Over!"
            connectionSocket.send(message.encode())
            connectionSocket.close()
        else:
            show = str(showSome(player, dealer))
            print(show)
            message = "Player decided to hit\n" + show
            connectionSocket.send(message.encode())
    # If client sends "stand"
    elif sentence == 'stand':
        # If player did not go over 21 then the dealer reveals hand and hits if below 17
        if player.calcScore() <= 21:
            while dealer.calcScore() < 17:
                dealer.draw(deck)
                if dealer.calcScore() > 21:
                    show = str(showAll(player, dealer))
                    print(show)
                    message = show + "\nDealer Busted, Game Over!"
                    connectionSocket.send(message.encode())
                    break
            show = str(showAll(player, dealer))
            print(show)

            # Checks Win Conditions
            compareValues = cmp(player.calcScore(), dealer.calcScore())
            if dealer.calcScore() > 21:
                message = show + "\nDealer Busted, Game Over!"
            elif compareValues == 0:
                message = show + "\nTie, Game Over!"
            elif compareValues == -1:
                message = show + "\nDealer Wins, Game Over!"
            elif compareValues == 1:
                message = show + "\nPlayer Wins, Game Over!"

        connectionSocket.send(message.encode())
        connectionSocket.close()

connectionSocket.close()