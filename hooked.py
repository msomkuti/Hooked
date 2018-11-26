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
from hookedfuns import *  # Import necessary functions and classes

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Start pygame and set up our display/screen
pg.init()  # Initialize pygame
screenDims = [412, 732]  # Specify our dimensions
screen = pg.display.set_mode((screenDims[0], screenDims[1]))  # Set our screen size
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Generate title screen
titlePos = title_screen(screen, screenDims)  # Function that generates screen
pg.display.update()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ENTER TITLE SCREEN
inTitle = 1  # Stay in the title screen until start clicked
while inTitle == 1:  # Enter title screen

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

# TEST ARC
# pg.draw.arc(screen, (255, 0, 0), (0, 100, 0, 20), 0, 0.7853982, 2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Hard code the dialogue for each character into dictionaries
convUnknown = {0: 'Hello Ashley',
               1: 'Look behind you',
               2: 'No',
               3: 'My mother was a scarecrow, my grandmother was a scarecrow, '
                  'but for some reason I was not born a scarecrow. I was born a pumpkin',
               4: 'Right? Like my mom and grandma are so cool and Im a pumpkin? WTF?',
               5: 'Btw Im going to murder you of course',
               6: 'Yeah, you ever get killed by a pumpkin Ashley? Huh?',
               7: 'Oh, you ok? Well I guess it doesnt matter because Im going to kill you',
               8: 'I mean I could kill you in, like a festive way if ya want. Like I could poison'
                  'you with a pumpkin spice latte',
               9: 'You right'}  # Pumpkin's lines

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
# Create our background, setup, then enter conversation
convoBG = background_creator((0, 0, 0), screen)  # Create bg for text conversation
screen.blit(convoBG, (0, 0))
pg.display.update()

[dialogue, bub_spacing] = setup(convAshley, convUnknown, screenDims)  # Add lines of dialogue to bubbles, and scale their surface

while 1:  # Enter main loop
    for event in pg.event.get():  # Event queue / catcher
        if event.type in (pg.KEYDOWN, pg.MOUSEBUTTONUP):  # Advance our conversation
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Advance conversation at different speeds based on if scroll or key press/click
            if event.button in (4, 5):
                for i in range(10):  # Scrolling
                    advance_conversation(dialogue, screen, screenDims, convoBG, bub_spacing)
                    pg.display.update()
                    pg.time.delay(12)  # Delay by small num of millisecs to make smooth animation
            else:
                for i in range(20):  # Click/key press, SHOULD I MAKE IT GO ONE BY ONE?
                    advance_conversation(dialogue, screen, screenDims, convoBG, bub_spacing)
                    pg.display.update()
                    pg.time.delay(12)

            pg.display.update()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
