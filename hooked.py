# Hooked Clone for Fries

# Elements that are necessary for the Hooked story
# Start menu
# Window to hold text
# Array(s) that holds dialogue
# Event that adds new messages, and erases ones at the top of the screen
# Ability of text bubbles to move upwards
# Practice importing from other files (funcs, defns, classes)

# RESOURCES:
    # https://www.pygame.org/docs/
    # https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidepoint
    # https://www.pygame.org/docs/ref/font.html
    # https://www.pygame.org/docs/tut/SurfarrayIntro.html
    # https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/

import pygame as pg
import sys, os
from pygame.locals import *
from hookedfuns import *  # Import functions from another file, GET OTHER ONES WORKING

pg.init()  # Initialize pygame

screenDims = [412, 732]  # Specify our dimensions
screen = pg.display.set_mode((screenDims[0], screenDims[1]))  # Set our screen size

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATION OF TITLE SCREEN / PLACE THIS IN A WHILE LOOP OR FUNCTION

titlePos = title_screen(screen, screenDims)  # Function that generates screen
pg.display.update()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENTER TITLE SCREEN
inTitle = 1  # Stay in the title screen until they start game
while inTitle == 1:  # Enter title screen, stay there until start is clicked

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CAN I MAKE ANIMATION WHERE CLICKED? EXTRA
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            mouse = pg.mouse.get_pos()  # Get our mouse position

            if titlePos.collidepoint(mouse):
                inTitle = 0  # Exit loop when we click start

        if event.type == pg.QUIT:  # Quit if we want to
            pg.quit()
            sys.exit()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HERE WE WILL DRAW A RECTANGLE THAT WILL BE ESSENTIALLY A VECTOR IMAGE OF A CHAT BUBBLE
# ESSENTIALLY WILL HAVE TO DRAW AN ELIPSES, LOOK INTO PG.DRAW.ARC()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TEST ARC
# pg.draw.arc(screen, (255, 0, 0), (0, 100, 0, 20), 0, 0.7853982, 2)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# NEED TO MAKE A DICTIONARY FOR THE CREATION OF INDIVIDUAL CHAT BUBBLES AND THEIR DESTRUCTION
# ESSENTIALLY, MAKE THE SURFACE NOT BLIT TO SCREEN IN THE NEXT ITERATION OF THE DRAW LOOP

convUnknown = {0: 'Hello Ashley',
               1: 'Look behind you',
               2: 'No',
               3: 'My mother was a scarecrow, my grandmother was a scarecrow, '
                  'but for some reason I was not born a scarecrow. I was born a pumpkin',
               4: 'Right? Like my mom and grandma are so cool and Im a fucking pumpkin? WTF?',
               5: 'Btw Im going to murder you of course',
               6: 'Yeah, you ever get killed by a pumpkin Ashley? Huh?',
               7: 'Oh shit, you ok? Well I guess it doesnt matter because Im going to kill you',
               8: 'I mean I could kill you in, like a festive way if ya want. Like I could poison'
                  'you with a pumpkin spice latte',
               9: 'Damn, you right'}  # Pumpkin's lines


convAshley = {0: "Hi, who's this?",
              1: "Are you a scarecrow?",
              2: "That's the scariest part about this. Genetics... ",
              3: "Don't worry, you're still cool to me.",
              4: "Wait, what?",
              5: "Well I was stabbed last week and I survived, so at least try a different way.",
              6: "True...",
              7: "But that'd be like eating ur fam, right? Kinda weird."}  # Ashley's lines

# Ending line: They all die from climate change  # Lol
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Instantiate dictionaries of chat bubbles

ashleyBubbles = dict.fromkeys(range(0, len(convAshley.keys())), Bubble(0, screenDims))  # SHOULD BE SENT
unknownBubbles = dict.fromkeys(range(0, len(convUnknown.keys())), Bubble(0, screenDims))  # SHOULD BE RECIEVED

ashleyBubbles[1].position[1] = ashleyBubbles[1].position[1] + ashleyBubbles[0].position[3]

print(ashleyBubbles[0])
print(ashleyBubbles[1].position)
print(ashleyBubbles[0].position)

# WORKING ORIGINAL CHAT BUBBLES
chatBubble = Bubble(0, screenDims)  # Instantiate chat bubbles
chatBubble1 = Bubble(0, screenDims)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATE OUR BACKGROUND, THEN ENTER THE CONVERSATION LOOP

convoBG = background_creator((0, 0, 0), screen)  # Create bg for text conversation
screen.blit(convoBG, (0, 0))
pg.display.update()

while 1:  # Enter main game loop
    for event in pg.event.get():  # Event queue
        if event.type in (pg.KEYDOWN, pg.MOUSEBUTTONUP):  # Advance our conversation   # conversation.spawnNext()

            for i in range(8):
                print(chatBubble.position)
                print(chatBubble1.position)

                chatBubble1.scroll(screen, convoBG, convAshley[5])  # Move messages upwards when enter is pushed
                chatBubble.scroll(screen, convoBG, convAshley[1])  # Move messages upwards when enter is pushed

                chatBubble1.position[1] = chatBubble.position[1] + chatBubble.position[3] * 1.25

                screen.blit(chatBubble.chat_bg, chatBubble.position)
                screen.blit(chatBubble1.chat_bg, chatBubble1.position)

                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # SCROLL FUNCTION DOES NOT WORK WELL WITH 2 BUBBLES FROM DICTIONARIES
                # print(ashleyBubbles[1].position)
                # print(ashleyBubbles[0].position)
                #
                # #print(ashleyBubbles[0].position)
                # ashleyBubbles[1].scroll(screen, convoBG, convAshley[5])  # Move messages upwards when enter is pushed
                # ashleyBubbles[0].scroll(screen, convoBG, convAshley[0])  # Move messages upwards when enter is pushed
                #
                #
                # #ashleyBubbles[0].scroll(screen, convoBG, convAshley[0])  # Move messages upwards when enter is pushed
                #
                #
                # screen.blit(ashleyBubbles[0].chat_bg, ashleyBubbles[0].position)
                # screen.blit(ashleyBubbles[1].chat_bg, ashleyBubbles[1].position)
                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                pg.display.update()
                pg.time.delay(10)

            pg.display.update()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # MAKE A WAY OF DELETING OLD CHATS
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # if chatBubble.position[1] < -chatDims[1]:  # If height of chat bubble off screen, destroy it
            #     del chatBubble  # need to fix the way this erases, remove from dictionary?
            #                     # or move it to a new one of past conversations
            #     pass

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
