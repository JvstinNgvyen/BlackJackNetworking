import random
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def printCards(self):
        print("{} of {}".format(self.value, self.suit))

    def getValue(self):
        return self.value

    def setValue(self, x):
        self.value = x

class Deck:
    def __init__(self):
        self.cards = []
        self.generateDeck()

    def generateDeck(self):
        for i in ["SPADES", "CLUB", "DIAMONDS", "HEARTS" ]:
            for j in "ACE, 2, 3, 4, 5, 6, 7, 8, 9, 10, JACK, QUEEN, KING".split(", "):
                self.cards.append(Card(i,j))

    def printCards(self):
        for c in self.cards:
            c.printCards()

    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append((deck.drawCard()))


    def showHandPlayer(self):
        for card in self.hand:
            card.printCards()

    def showHandDealer(self):
        self.hand[-1].printCards()
        print("FACE DOWN")

    def calcScore(self):
        value = 0
        for card in self.hand:
            if card.getValue() == "KING" or card.getValue() == "QUEEN" or card.getValue() == "JACK":
                value += 10
            elif card.getValue() == "ACE":
                if value + 11 > 21:
                    return value + 1
                elif value + 11 < 21:
                    return value + 11
            else:
                value += int(card.getValue())
        return value

def cmp(a, b):
    return (a > b) - (a < b)

def showSome(player, dealer):
    print("Dealer Hand:")
    dealer.showHandDealer()
    print('_____________________')
    print("Player Hand:")
    player.showHandPlayer()
    print(player.calcScore())
    print('_____________________')

def showAll(player, dealer):
    print("Dealer Hand:")
    dealer.showHandPlayer()
    print(dealer.calcScore())
    print('_____________________')
    print("Player Hand:")
    player.showHandPlayer()
    print(player.calcScore())
    print('_____________________')

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    print('_____________________')
    Dealer1 = Player("Dealer")
    Dealer1.draw(deck)
    Dealer1.draw(deck)

    Player1 = Player("Player 1")
    Player1.draw(deck)
    Player1.draw(deck)

    #showSome(Player1, Dealer1)
    showAll(Player1,Dealer1)
    playing = True
    while playing:
        while True:
            action = input("Hit or Stand? ")
            if action.lower() == "h":
                Player1.draw(deck)
            elif action.lower() == "s":
                print("Player Stands")
                playing = False
            else:
                print("Try again")
                continue
            break
        showSome(Player1, Dealer1)
        if Player1.calcScore() > 21:
            print("Player Bust")
            break

    if Player1.calcScore() <= 21:
        while Dealer1.calcScore() < 18:
            Dealer1.draw(deck)
            if Dealer1.calcScore() > 21:
                print("Dealer Bust")
                break
        showAll(Player1,Dealer1)

        compareValues = cmp(Player1.calcScore(), Dealer1.calcScore())
        if Dealer1.calcScore() > 21:
            print("Dealer Bust")
        elif compareValues == 0:
            print("Tie")
        elif compareValues == -1:
            print('Dealer Wins')
        elif compareValues == 1:
            print("Player Wins")