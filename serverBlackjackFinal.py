import socket
import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def printCards(self):
        return "\n{} of {}".format(self.value, self.suit)

    def getValue(self):
        return self.value

    def setValue(self, x):
        self.value = x


class Deck:
    def __init__(self):
        self.cards = []
        self.generateDeck()

    def generateDeck(self):
        for i in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for j in "Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King".split(", "):
                self.cards.append(Card(i, j))

    def printCards(self):
        for c in self.cards:
            c.printCards()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
    def draw(self, deck):
        self.hand.append((deck.drawCard()))

    def showHandPlayer(self):
        output = ''
        i = -1
        for i in range(len(self.hand)):
            output += self.hand[i].printCards()
            i += 1
        return output

    def showHandDealer(self):
        return "{}\nFACE DOWN".format(self.hand[-1].printCards())

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


def cmp(a, b):
    return (a > b) - (a < b)


def showSome(player, dealer):
    return "_____________________\nDealer Hand: {} \n_____________________\nPlayer Hand: {}\n" \
           "Total: {}\n_____________________ \n\nHit or Stand?".format(
            dealer.showHandDealer(), player.showHandPlayer(), player.calcScore())


def showAll(player, dealer):
    return "_____________________\nDealer Hand: {} \nTotal: {}\n_____________________\nPlayer Hand: {}\n" \
           "Total: {}\n_____________________ \n".format(
            dealer.showHandPlayer(), dealer.calcScore(), player.showHandPlayer(), player.calcScore())

host = '192.168.0.4' #socket.gethostname()
serverPort = 5000

deck = Deck()
deck.shuffle()

dealer = Player("Dealer")
dealer.draw(deck)
dealer.draw(deck)

player = Player('Player 1')
player.draw(deck)
player.draw(deck)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(2)

print('BlackJack started.')


while True:
    connectionSocket, addr = serverSocket.accept()
    show = str(showSome(player, dealer))
    print("Initial Hand\n" + show)

    print('Player = ' + addr[0] + ':' + str(addr[1]))
    sentence = connectionSocket.recv(1024).decode()

    if sentence == 'play':
        connectionSocket.send(show.encode())

    if sentence == 'hit':
        player.draw(deck)

        if player.calcScore() > 21:
            show = str(showAll(player, dealer))
            print(show)
            message =  show + "\nPlayer Busted, Game Over"
            connectionSocket.send(message.encode())
            connectionSocket.close()
        else:
            show = str(showSome(player, dealer))
            print(show)
            message = "Player decided to hit\n" + show
            connectionSocket.send(message.encode())
    elif sentence == 'stand':
       # message = ("{} decided to stand.".format(addr[0]))
        if player.calcScore() <= 21:
            while dealer.calcScore() < 17:
                dealer.draw(deck)
                if dealer.calcScore() > 21:
                    show = str(showAll(player, dealer))
                    print(show)
                    message = show + "\nDealer Busted, Game Over"
                    connectionSocket.send(message.encode())
                    break
            show = str(showAll(player, dealer))
            print(show)

            compareValues = cmp(player.calcScore(), dealer.calcScore())
            if dealer.calcScore() > 21:
                message = show + "\nDealer Busted, Game Over"
            elif compareValues == 0:
                message = show + "\nTie, Game Over"
            elif compareValues == -1:
                message = show + "\nDealer Wins, Game Over"
            elif compareValues == 1:
                message = show + "\nPlayer Wins, Game Over"
        connectionSocket.send(message.encode())
        connectionSocket.close()

connectionSocket.close()