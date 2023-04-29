# AAI 551-B Final Project: Crazy Eights Card Game
# By Trent Reichenbach
# Game rules taken from: https://en.wikipedia.org/wiki/Crazy_Eights 

import random

class Card:
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank_list[self.rank] + " of " + self.suit_list[self.suit]
    
    def __gt__(self, other):
        return self.suit > other.suit or (self.suit == other.suit and self.rank > other.rank)
    
    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
                
    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s += i * " " + str(self.cards[i]) + "\n"
        return s
    
    def shuffle(self):
        n_cards = len(self.cards)
        for i in range(n_cards):
            j = random.randrange(0, n_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
    def pop_card(self):
        return self.cards.pop()
    
    def is_empty(self):
        return len(self.cards) == 0
    
    def deal(self, hands, n_cards = 52):
        for i in range(n_cards):
            if self.is_empty(): break
            card = self.pop_card()
            current_player = i % len(hands)
            hands[current_player].add_card(card)

class Hand(Deck): 
    def __init__(self, name=""):
        self.cards = []
        self.name = name
        # Unique feature: Players have money they can bet with that carries over between games
        self.money = 500
        
    def add_card(self, card):
        self.cards.append(card)
    
    def pop_card(self, index=-1):
      return self.cards.pop(index)
        
    def __str__(self):
        s = self.name + "'s hand"
        if self.is_empty(): return s + " is empty"
        return s + " contains: \n" + Deck.__str__(self)

# Class for discard pile  
class Discard(Deck):
    suit_list = ["Clubs", "Diamonds", "Hearts", "Spades"]
    
    def __init__(self):
        self.cards = []
        # Define separate variable for current suit (for when player declares suit after playing 8)
        self.current_suit = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.current_suit = card.suit
        
    def top_card(self):
      return self.cards[-1]
    
    # Print card at top of pile and current suit
    def __str__(self):
      return "Top of discard pile: " + str(self.top_card()) + "\nCurrent suit: " + self.suit_list[self.current_suit]
    
    # Pick a new suit for the discard pile after playing an 8
    def pick_suit(self):
      while True:
        print("Pick a new suit. (Enter 1 for Clubs, 2 for Diamonds, 3 for Hearts, 4 for Spades)")
        suit = int(input())
        if 1 <= suit <= 4:
          self.current_suit = suit - 1
          break
        
        print("Invalid answer!")

class CrazyEights:
    def __init__(self, name1, name2):
        # Initialize deck
        self.deck = Deck()
        self.deck.shuffle()
        # Initialize player hands
        self.hand1, self.hand2 = Hand(name1), Hand(name2)
        self.hands = [self.hand1, self.hand2]
        self.deck.deal(self.hands, 6)
        # Initialize discard pile 
        self.discard = Discard()
        self.discard.add_card(self.deck.pop_card())
        # Initialize flags for special card effects
        self.new_suit = False
        self.skip_turn = False 
        self.draw_two = False
        # Initialize money being bet
        self.bet = 0
    
    # Set money paid to winner (winning player earns sum of all money bet)
    def set_bet(self):
      for hand in self.hands:
        print(hand.name + "'s current money is $" + str(hand.money) + ".")
        
        while True:
          print("How much is " + hand.name + " willing to bet?")
          wager = int(input())
          
          if wager <= hand.money:
            self.bet += wager
            hand.money -= wager
            break
          
          print("Not enough money!")
          
    # Draw cards from deck into hand, refill deck when empty
    def draw(self, hand, n_cards = 1):
      for i in range(n_cards):
            card = self.deck.pop_card()
            hand.add_card(card)
            if self.deck.is_empty(): self.refill_deck()
            
    # Refill deck with discarded cards when empty
    def refill_deck(self):
      print("\nRefilling deck...")
      # Add all discarded cards except top card to deck
      self.deck.cards = self.discard.cards[:-1]
      self.deck.shuffle()
      
      # Clear discard pile except for top card
      top_card = self.discard.top_card()
      self.discard.cards = []
      self.discard.add_card(top_card)
            
    # Check if card can be added to discard pile and handle special cards
    def check_card(self, card):
      # 8 is a wild card (no check needed)
      if card.rank == 8:
        # Set flag to change suit of discard pile
        self.new_suit = True
        return True
      
      if card.suit == self.discard.current_suit or card.rank == self.discard.top_card().rank:
        # Set flag to make next player draw two cards if card is a 2
        if card.rank == 2: self.draw_two = True
        # Set flag to skip next player's turn if card is a Queen
        if card.rank == 12: self.skip_turn = True
        return True
      
      return False
    
    # Move card from hand to discard pile, or draw card from deck (return True if discard successful)
    def discard_card(self, hand, choice):
      print("\n\n\n\n")
      
      # Draw card
      if choice == 0: 
        self.draw(hand)
        print(hand)
        print(str(c8.discard) + "\n")
        return False
      
      # Try discard
      elif 1 <= choice <= len(hand.cards): 
        chosen_card = hand.cards[choice - 1]
        if self.check_card(chosen_card): 
          self.discard.add_card(hand.pop_card(choice - 1))
          if self.new_suit:
            self.discard.pick_suit()
            self.new_suit = False
          return True
        
        print("Cannot discard!")
        return False
      
      print("Invalid choice!")
      return False
      
    # Reset everything except player names/money for new game
    def reset(self):
      # Reset deck
        self.deck = Deck()
        self.deck.shuffle()
        # Reset player hands
        self.hand1.cards = []
        self.hand2.cards = []
        self.deck.deal(self.hands, 6)
        # Reset discard pile 
        self.discard = Discard()
        self.discard.add_card(self.deck.pop_card())
        # Reset flags
        self.new_suit = False
        self.skip_turn = False 
        self.draw_two = False
        # Reset money being bet
        self.bet = 0


print("Welcome to Crazy Eights!")
print("The goal of the game is to get rid of all cards in your hand.")
print("During your turn, discard a card with the same suit or rank as the card on top of the discard pile.")
print("If you don't have any cards to discard, draw from the deck until you get one.")
print("8's act as wild cards and let you declare a new a suit for the discard pile.")
print("If you play a 2, the opponent must draw two cards.")
print("If you play a Queen, the opponent's turn is skipped.")         
           
print("\nEnter Player 1's name:")
name1 = input()
print("Enter Player 2's name: ")
name2 = input()

c8 = CrazyEights(name1, name2)

while True:
  c8.set_bet()

  game_run = True
  while game_run:
    for hand in c8.hands:
      print("\n\n\n\n")
      
      if c8.skip_turn:
        print("Skipping " + hand.name + "'s turn...")
        c8.skip_turn = False
        continue
      
      if c8.draw_two:
        print(hand.name + " drew two cards.")
        c8.draw(hand, 2)
        c8.draw_two = False
      
      print(hand.name + "'s turn:\n\n")
      print(hand)
      print(str(c8.discard) + "\n")
      
      print("Pick a card from your hand.")
      print("Enter number of card to choose (Topmost card displayed is 1).") 
      print("Enter 0 to draw a card from the deck.")
      
      while True:
        choice = int(input())
        discard_success = c8.discard_card(hand, choice)
        if discard_success: break
          
      if hand.is_empty():
        print(hand.name + " wins!")
        print(hand.name + " earned $" + str(c8.bet) + ".")
        hand.money += c8.bet 
        game_run = False
        break
    
  print("Play again? (Press 1 for Yes, anything else for No)")
  play = input()
  if play == "1": c8.reset()
  else:
    print ("Thanks for playing!")
    break
  
    
        
