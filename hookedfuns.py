# This file holds the functions and classes for the Hooked game

import pygame as pg
import sys, os
from pygame.locals import *
from operator import attrgetter

pg.init()


class Bubble:
    font = pg.font.SysFont(None, 32)  # Set our font, GET A NICER ONE IN HERE THOOOO

    def __init__(self, sent, screenDims, text):
        self.horz_marg = int(screenDims[0] * 0.12)  # Horizontal margin for msgs from edge of screen
        self.vert_marg = int(screenDims[1] * 0.15)  # Vertical margin to start scrolling from
        self.scrollH = [self.horz_marg, screenDims[1] - self.vert_marg]  # Scroll up from default (x,y) of bubbles
        self.text = text.split()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Initialize chat surfaces
        max_chat_dims = [int(screenDims[0] - self.horz_marg * 2), int(screenDims[1] - self.vert_marg * 2)]

        # Create the surface to hold background for our chats
        self.chat_bg = pg.Surface((max_chat_dims[0], max_chat_dims[1]))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # NEED TO FIX FORMATTING FOR SENT VS RECIEVED
        if sent != 1:  # Formatting for sent v.s. received messages
            self.position = self.chat_bg.get_rect().move(self.scrollH[0], self.scrollH[1])  # Position bubbles

        if sent == 1:
            # Left cord of message account for right marg
            self.scrollH[0] = screenDims[0] - self.horz_marg - max_chat_dims[0]
            self.position = self.chat_bg.get_rect().move(self.scrollH[0], self.scrollH[1])
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addtext(self, chat_surface):
        imcors = chat_surface.get_rect()  # Get rect values of chat
        txt_h_marg = int(imcors[2] * 0.02)  # Offset our text by horizontal margins
        lines = []  # Hold our new lines of text
        total_words = len(self.text)  # Get num of words in msg
        used = 0  # Index to keep track of words already used
        # cut_off = 0  # Start slice at start of array

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Enter word slicing loop
        done = 0  # Exit condition
        while done == 0:
            texttemp = self.text[used: total_words]  # Slice our text starting at num words used, ending at end of array

            cut_off = len(texttemp)  # Start slicing at end of remaining words
            rendercheck = " ".join(texttemp)
            rendersize = Bubble.font.size(rendercheck)  # Check render size of possible line of dialogue

            if rendersize[0] > imcors[2] - txt_h_marg * 2:  # If width(dialogue) > width(chat_surface) + margins
                while rendersize[0] > imcors[2] - txt_h_marg * 2:
                    cut_off = cut_off - 1
                    texttemp = texttemp[0: cut_off]  # Cut off last word in array, track indx
                                                     # Note: if a = '123' len(a) = 3, a[3:3] returns ''
                    rendercheck = " ".join(texttemp)
                    rendersize = Bubble.font.size(rendercheck)  # Check render size of newly sliced array

            line = rendercheck  # Append well formatted line of dialogue
            lines.append(line)

            used = used + cut_off  # Sum num of words used in each appended line of dialogue
            if used == total_words:  # Stop when sum of words in lines = total num words in self.text
                done = 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GET TEXT TO BE SPACED EVENLY IN MSG AND THEN RENDER
        text_xcors = [0]  # Hold x coordinates of text, each tuple contains beg/end coordinates of each line
        text_ycors = [0]  # Hold y coordinates of text

        render_imcors = imcors
        sample_line = lines[0]
        rendersize = Bubble.font.size(sample_line)  # Every line has equal height
        render_imcors[1] = rendersize[1] * .4  # Establish top margin, by offsetting text render

        text_xcors.append(render_imcors[0] + txt_h_marg)  # Horizontal starting point is same for each line
        text_ycors.append(render_imcors[1])  # Start with y coordinate of topmost line

        for line in lines:
            rendersize = Bubble.font.size(line)  # Render size of each line
            imcorstemp = render_imcors

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # ADDING MARGIN IS NOT A GOOD FIX??????
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            text_xcors.append(imcorstemp[0] + rendersize[0] + txt_h_marg)  # Account for right margin

            # Change y cor of new line of txt down by height of txt * num of lines
            imcorstemp[1] = render_imcors[1] + rendersize[1] * 1.25

            text_ycors.append(imcorstemp[1])  # Append new y cord

        # Draw msg box before blitting text
        chat_surface = self.bubble_draw(self.chat_bg, text_xcors, text_ycors, txt_h_marg)

        for i in range(len(lines)):
            good_line = Bubble.font.render(lines[i], True, (255, 0, 255))  # Render font to surface
            chat_surface.blit(good_line, [text_xcors[1], text_ycors[i+1]])

        return chat_surface
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bubble_draw(self, chat_surface, text_xcors, text_ycors, txt_h_marg):  # SHOULD I ADD SCREEN DIMS?

        horz_cords = [min(text_xcors), max(text_xcors) + txt_h_marg]  # WHY DOES THIS KEEP IT FROM SCALING DOWN
        vert_cords = [min(text_ycors), max(text_ycors)]

        print(horz_cords)
        print(vert_cords)

        # print('ok')
        # print(text_xcors)
        # print(text_ycors)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # NEED TO ACCOUNT FOR MARGINS BEFORE DRAWING ARCS, NEED TO TEST THIS
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # SCALE chat_bg surface TO CORRECT LENGTH BEFORE RENDERING TEXT!!
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        scale_dims = [horz_cords[1], vert_cords[1]]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # SCALING IS NOT WORKING CORRECTLY
        # DO I FULLY UNDERSTAND WHAT HAPPENS HERE?, WEIRD STUFF STILL HAPPENING

        chat_surface = self.scale(chat_surface, scale_dims[0], scale_dims[1])
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        chat_surface.fill((255, 255, 255), (horz_cords[0], 0, horz_cords[1], vert_cords[1]))

        # Draw horizontal lines above and below our text
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], 0), (horz_cords[1], 0)], 3)
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], vert_cords[1]), (horz_cords[1], vert_cords[1])], 3)

        # Draw vertical lines besides our text
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], 0), (horz_cords[0], vert_cords[1])], 3)
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[1], 0), (horz_cords[1], vert_cords[1])], 3)

        return chat_surface

    def scale(self, input_surface, width, height):  # Scale our bubble to nicely hold rendered text
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # SCALE SHOULD BE CALLED FOR CHAT_BG AFTER GETTING RENDER SIZE FOR TEXT
        input_surface = pg.transform.scale(input_surface, (width, height))
        self.position[2] = width  # Update surface's rect with accurate dims
        self.position[3] = height

        return input_surface
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def scroll(self, screen, background):  # NEED TO MAKE THIS SMOOTHER??
        screen.blit(background, self.position)  # Draw over old position
        self.position[1] -= 8  # Move chat upwards
        return


def background_creator(input_color, screen):  # Create a simple background
    bg = pg.Surface(screen.get_size())  # Create a surface the size of our screen
    bg.convert()  # FORGOT WHY I HAVE THIS
    bg.fill(input_color)  # Fill surface with color
    return bg


def title_screen(screen, screen_dimensions):
    tBG = background_creator((0, 0, 255), screen)  # Make title screen's background

    titleBox = pg.Surface((200, 100))  # Create title box

    titleBox.convert()
    titleBox.fill((255, 255, 255))
    titlePos = titleBox.get_rect()

    titlePos.centerx = screen_dimensions[0] / 2  # Center title box
    titlePos.centery = screen_dimensions[1] / 2

    # CAN I MAKE A FONT FUNCTION???
    font = pg.font.SysFont(None, 48)  # Set our font

    titleText = font.render('Hooked', True, (0, 0, 0))  # Render font to a surface
    ttPos = titleText.get_rect()  # Get coordinates of text
    ttPos.center = titlePos.center  # Center text in the title box

    # Update our screen to show the title
    screen.blit(tBG, (0, 0))
    screen.blit(titleBox, titlePos)
    screen.blit(titleText, ttPos)
    return titlePos  # Return position of title box, used to start game


def setup(ashleyBubbles, unknownBubbles, screenDims):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Add text and scale our bubbles
    for bub in ashleyBubbles:
        bub.chat_bg = bub.addtext(bub.chat_bg)

    for bub in unknownBubbles:
        bub.chat_bg = bub.addtext(bub.chat_bg)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Calculate the spacing between texts
    all_bubs = ashleyBubbles + unknownBubbles
    min_size = min(all_bubs, key=attrgetter('position'))  # HOW DOES MIN WORK WITH RECT????
    max_fit = int(screenDims[1] / min_size.position[3])  # Screen height / height of smallest text
    good_fit = int(max_fit * (5/9))  # Only want to show 3/4 of max num bubbles that fit on screen

    # Spacing calculated by finding height(bubbles) if only int(good_fit) fit on screen,
    # then take difference between height(good_fit bubbles) and height(min bubble size)
    bub_spacing = (screenDims[1] / good_fit) - min_size.position[3]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Create our dialogue in the proper order
    # ACCOUNT FOR STAGE DIRECTIONS. MAYBE DRAW IMAGES?
    page_0 = [unknownBubbles[0], ashleyBubbles[0], unknownBubbles[1], ashleyBubbles[1], unknownBubbles[2]]
    page_1 = [unknownBubbles[3], ashleyBubbles[2]]
    page_2 = [unknownBubbles[4], unknownBubbles[5], ashleyBubbles[3], ashleyBubbles[4], unknownBubbles[6]]
    page_3 = [ashleyBubbles[5], unknownBubbles[7], ashleyBubbles[6]]
    page_4 = [unknownBubbles[8], ashleyBubbles[7], unknownBubbles[9]]
    dialogue = page_0 + page_1 + page_2 + page_3 + page_4
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Space out our bubbles
    # For each bubble, move it down by adding (height of prev bubble + spacing) to current y coordinate
    for i in range(1, len(dialogue)):
        y_coordinate = dialogue[i-1].position[1] + dialogue[i-1].position[3]
        dialogue[i].position[1] = y_coordinate + bub_spacing
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return dialogue


def advance_conversation(dialogue, screen, screenDims, background):
    for bub in dialogue:
        bub.scroll(screen, background)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Improve erasure of msgs!
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if 0 < bub.position[1] < screenDims[1]:  # Only blit msgs that are on screen
            screen.blit(bub.chat_bg, bub.position)
