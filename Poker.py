#Poker game - Unfinished

import pygame 
import sys
import random 
pygame.init()

#Screen
WIDTH, HEIGHT = 1800,1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poker Simulation")
#Cards
cardh = 150
cardw = 100
whitecard = (255,255,255)
redcard = (255,0,0)
blackcard = (0,0,0)
table = (0,100,0)
font = pygame.font.Font(None,48)
smallfont = pygame.font.Font(None,30)

#buttons
startbutton = pygame.Rect(0, 0, 260, 80)
startbutton.center = (WIDTH // 2, HEIGHT // 2 + 80)
buttonfont = pygame.font.SysFont(None, 36)

checkbutton = pygame.Rect(0, 0, 260, 80)
checkbutton.center = (WIDTH //2 + 600, HEIGHT//2 + 80)


#lookup table for values
cardpoints = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8, 
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11
}
#class for cards
class card:
    def __init__(self, suit, value, x,y):
        self.suit = suit
        self.value = value
        self.points = cardpoints[value]
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,cardw,cardh)

    def draw(self,surface): 
        pygame.draw.rect(surface, whitecard,self.rect,0,5)
        pygame.draw.rect(surface,blackcard,self.rect, 2,5)
        valuetext = font.render(self.value, True, blackcard if self.suit in ["Clubs", "Spades"]else redcard)
        surface.blit(valuetext, (self.x +5, self.y +5))
        suittext = font.render(self.suit[0], True, blackcard if self.suit in ["Clubs", "Spades"]else redcard)
        surface.blit(suittext, (self.x + cardw - suittext.get_width()-5, self.y+cardh - suittext.get_height()-5))

#Card Database
suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] 
deck = [f"{value} of {suit}" for suit in suits for value in values]

#Deal
currentcardsplayer = []
currentcardsdealer = []
currentcardsplayer2 = []
dealercardrevealed1 = False
dealercardrevealed2 = False
decktuples = [(v, s) for s in suits for v in values]
#remaining deck for hits 
shuffledeck = decktuples[:]
random.shuffle(shuffledeck)
def drawfromremain():
    if not shuffledeck:
        shuffledeck.extend(decktuples)
        random.shuffle(shuffledeck)
    return shuffledeck.pop()

#deal 2 cards to player
def dealthecardsplayer():
    sample = random.sample(decktuples, 2)
    gap = 50
    totalw = 4 * cardw + 3 * gap
    x0 = WIDTH // 2 + 175
    y  = HEIGHT // 2 
    dealtplayer = []
    for i, (v, s) in enumerate(sample):
        x = x0 + i * (cardw + gap)
        dealtplayer.append(card(s, v, x, y))
    return dealtplayer

def dealthecardsplayer2():
    sample = random.sample(decktuples, 2)
    gap = 50
    totalw = 4 * cardw + 3 * gap
    x0 = WIDTH // 2 - 400
    y  = HEIGHT // 2 
    dealtplayer = []
    for i, (v, s) in enumerate(sample):
        x = x0 + i * (cardw + gap)
        dealtplayer.append(card(s, v, x, y))
    return dealtplayer

#deal 5 cards to dealer
def dealthecardsdealer():
    sample = random.sample(decktuples, 5)
    dealt = []
    for i, (v, s) in enumerate(sample):
        x, y = nextdealerpos(i)
        dealt.append(card(s, v, x, y))
    return dealt

#hide the card before player finishes turn
def drawcardback(surface, x, y):
    rect = pygame.Rect(x, y, cardw, cardh)
    pygame.draw.rect(surface, (0, 0, 0), rect, border_radius=5)      
    pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=5)


dealergap = 50
dealerx0  = WIDTH // 2 - 125
dealery   = 150

def nextdealerpos(nalready):
    return (dealerx0 + nalready * (cardw + dealergap), dealery)

#start message
message = "Welcome to Poker - By Jackson Blellock"
gamestate = "start" 
#Main
while True:
    screen.fill(table)

    # Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # Start using button
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if gamestate == "start" and startbutton.collidepoint(e.pos):
                currentcardsplayer = dealthecardsplayer()
                currentcardsdealer = dealthecardsdealer()
                currentcardsplayer2 = dealthecardsplayer2()
                message = "Current game"
                gamestate = "playerturn1" # added for checking game state

            elif gamestate == "playerturn1":
                if checkbutton.collidepoint(e.pos):
                    dealercardrevealed1 = True
                    gamestate = "playerturn2"
            elif gamestate =="playerturn2":
                if checkbutton.collidepoint(e.pos):
                    dealercardrevealed2 = True
                    gamestate = "results"
            elif gamestate == "results":
                pass

    if gamestate == "dealer":

        gamestate = "results"

    # Drawing
    # Title
    title = font.render("Poker Simulation", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    status = smallfont.render(message, True, (255, 255, 255))
    screen.blit(status, (WIDTH // 2 - status.get_width() // 2, 90))

    if gamestate == "start":
        # Start button only
        pygame.draw.rect(screen, (245, 245, 245), startbutton, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), startbutton, 2, border_radius=12)
        starttxt = buttonfont.render("Start", True, (0, 0, 0))
        screen.blit(starttxt, (startbutton.centerx - starttxt.get_width() // 2, startbutton.centery - starttxt.get_height() // 2))

    else:
        # Dealer label + up-cards + face-down cards
        dealerlabel = buttonfont.render("Dealer", True, (255, 255, 255))
        screen.blit(dealerlabel, (WIDTH // 2 - dealerlabel.get_width() // 2, 120))

        if currentcardsdealer:
            for i, c in enumerate(currentcardsdealer):
                if i == 3 and not dealercardrevealed1:
                    drawcardback(screen, c.x, c.y)
                elif i == 4 and not dealercardrevealed2:
                    drawcardback(screen, c.x, c.y)
                else:
                    c.draw(screen)

        # Player label + cards + total
        playerlabel = buttonfont.render("Player1", True, (255, 255, 255))
        screen.blit(playerlabel, (WIDTH // 2 - playerlabel.get_width() // 2 + 300, HEIGHT // 2 - 50))

        for c in currentcardsplayer:
            c.draw(screen) 

        player2label = buttonfont.render("Player2", True, (255, 255, 255))
        screen.blit(player2label, (WIDTH // 2 - player2label.get_width() // 2 - 300, HEIGHT // 2 - 50))

        for c in currentcardsplayer2:
            c.draw(screen)

        # Draw Hit/Stand buttons during player's turn
        if gamestate == "playerturn1" or gamestate =="playerturn2":
            pygame.draw.rect(screen, (245, 245, 245), checkbutton, border_radius=12)
            pygame.draw.rect(screen, (0, 0, 0), checkbutton, 2, border_radius=12)
            hittxt = buttonfont.render("Check", True, (0, 0, 0))
            screen.blit(hittxt, (checkbutton.centerx - hittxt.get_width() // 2, checkbutton.centery - hittxt.get_height() // 2))

    pygame.display.flip()
