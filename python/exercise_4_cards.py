import random
def createDeck() -> list:
    nominals = ('J','Q','K','A','10','9','8','7','6')
    types = ('s','h','d','c')

    cards = []
    for tp in types:
        for card in nominals:
            cards.append(card+tp)
    return cards

def customShuffle(deck:list) -> list:
    len_deck = len(deck)

    for i in range(len(deck)-1):
        deck.remove(deck[i])
        deck.insert(random.randint(i, len_deck), deck[i])
    return deck