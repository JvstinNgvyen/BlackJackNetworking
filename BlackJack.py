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


    def showHand(self):
        for card in self.hand:
            card.printCards()

    def calcScore(self):
        value = 0
        for card in self.hand:
            if card.getValue() == "KING" or card.getValue() == "QUEEN" or card.getValue() == "JACK":
                value += 10
            elif card.getValue() == "ACE":
                if value + 11 > 21:
                    return value + 1
                else:
                    return value + 11
            else:
                value += int(card.getValue())
        return value

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()

    Dealer = Player("Dealer")
    Dealer.draw(deck)
    Dealer.draw(deck)
    print("Dealer Hand:")
    Dealer.showHand()


    Player = Player("Player 1")
    Player.draw(deck)
    Player.draw(deck)
    print("Player Hand:")
    Player.showHand()
    print(Player.calcScore())

