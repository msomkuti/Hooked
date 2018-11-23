# This file holds the functions and classes for the Hooked game

import pygame as pg
import sys, os
from pygame.locals import *
pg.init()

class Bubble:  # NEED TO MAKE IT SO TEXT IS IN BUBBLES
    font = pg.font.SysFont(None, 32)  # Set our font

    # def __init__(self, image, sent, screenDims, chatDims):
    def __init__(self, image, sent, screenDims):
        self.image = image
        self.horz_marg = int(screenDims[0] * 0.175)  # Horizontal margin for msgs from edge of screen
        self.vert_marg = int(screenDims[1] * 0.15)  # Vertical margin to start scrolling from
        self.scrollH = [self.horz_marg, screenDims[1] - self.vert_marg]  # Scroll upwards from here, default (x,y) of bubbles

        # INITIALIZE CHAT SURFACES
        max_chat_dims = [int(screenDims[0] - self.horz_marg * 2), int(screenDims[1] - self.vert_marg * 2)]
        print(max_chat_dims)
        self.chat_bg = pg.Surface((max_chat_dims[0], max_chat_dims[1]))  # Create the background for our chats

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # NEED TO FIX FORMATTING FOR SENT VS RECIEVED
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if sent != 1:  # Formatting for sent v.s. received messages
            self.position = image.get_rect().move(self.scrollH[0], self.scrollH[1])  # Position bubbles
            self.image = pg.transform.flip(self.image, 1, 0)  # Flip our chat bubble on xaxis to face the correct way
        if sent == 1:
            self.scrollH[0] = screenDims[0] - chatDims[0] - self.scrollH[0]
            self.position = image.get_rect().move(self.scrollH[0], self.scrollH[1])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SCALE SHOULD BE CALLED FOR CHAT_BG AFTER GETTING RENDER SIZE FOR TEXT
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def scale(self, input_surface, width, height):  # Scale our bubble to size
        # FIX THIS
        pg.transform.scale(input_surface, (width, height))

    def addtext(self, chat_surface, text):

        imcors = chat_surface.get_rect()  # Get rect values of chat
        self.text = text.split()  # Text inside chat bubble
        lines = []  # Hold our new lines of text

        numwords = len(self.text)  # Get num of words in msg
        num_words = 0  # Index to keep track of words already used

        done = 0  # Exit condition
        while done == 0:
            cut_off = numwords  # Start indx at end of list
            texttemp = self.text[num_words: cut_off]
            #print(texttemp)
            rendercheck = ' '.join(texttemp)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # JOIN ALL WORDS WITH A SPACE IN BETWEEN
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            rendersize = Bubble.font.size(rendercheck)  # Check how much space it will take to render msg

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # STILL NOT WORKING CORRECTLY
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            if rendersize[0] > imcors[2]:  # If len of words > width of chat_surface
                while rendersize[0] > imcors[2]:  # If the len of the msg is greater than width of bubble, split the msg

                    cut_off = cut_off - 1  # Keep track of indx of # of words we cut off
                    texttemp = texttemp[num_words: cut_off]  # Cut off words until short enough, stop at cut_off
                    # NOTE: text[2,3] will only get the 2nd word

                    rendercheck = ''.join(texttemp)
                    rendersize = Bubble.font.size(rendercheck)  # See if our sliced text will fit

                texttemp = texttemp[num_words: cut_off]

            num_words = cut_off
            line = rendercheck
            lines.append(line)

            if num_words == numwords:  # Stop when we have gone through all words
                                    # NOTE: if a = '123' len(a) = 3 and a[3:3] returns ''
                done = 1

        offset = 0  # Offset our lines of text when rendering

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GET TEXT TO BE SPACED EVENLY IN MSG, MAKE SURE IT DOES NOT GO PAST BOTTOM OF MSG
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        text_xcors = []  # Hold the x coordinates of our text, each tuple contains beg/end coordinates of each line
        text_ycors = []  # Hold the y coordinates of our text

        render_imcors = imcors
        sample_line = ''.join(lines[0])
        rendersize = Bubble.font.size(sample_line)  # Every line will have same height
        render_imcors[1] = rendersize[1] * .4  # Establish top margin, by offsetting text render

        text_xcors.append(render_imcors[0])  # The horizontal starting point will be same for each line
        text_ycors.append(render_imcors[1])  # Start with y coordinate of topmost line

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for line in lines:
            line = ''.join(line)
            rendersize = Bubble.font.size(line)  # Render size of each line
            imcorstemp = render_imcors

            text_xcors.append(imcorstemp[0] + rendersize[0])
            imcorstemp[1] = render_imcors[1] + rendersize[1] * 1.25  # change y cor of new line of txt down by
                                                                     # height of txt * num of lines

            text_ycors.append(imcorstemp[1])  # Append tuple containing old and new y coordinate

        # EDIT THIS SO IT DRAWS TO chat_bg
        self.bubble_draw(self.chat_bg, text_xcors, text_ycors)  # Draw our message box before blitting text

        for i in range(len(lines)):
            lines[i] = ''.join(lines[i])
            good_line = Bubble.font.render(lines[i], True, (255, 0, 255))  # Render font to surface
            chat_surface.blit(good_line, [text_xcors[0], text_ycors[i]])

        # ####################################################################
        # # THIS IS THE OLD VERSION
        # for line in lines:
        #     line = ''.join(line)
        #     rendersize = Bubble.font.size(line)  # Render size of each line
        #     offset += 1
        #     imcorstemp = imcors
        #     y_cord_old = imcorstemp[1]  # Get beginning y coordinate
        #     #text_xcors.append([imcorstemp[0], imcorstemp[0] + rendersize[0]])
        #     text_xcors.append(imcorstemp[0] + rendersize[0])
        #     #print(imcors)
        #     imcorstemp[1] = imcors[1] + rendersize[1] * 1.25 #* offset  # change y cor of new line of txt down by
        #                                                             # height of txt * num of lines
        #
        #     #text_ycors.append([y_cord_old, imcorstemp[1]])  # Append tuple containing old and new y coordinate
        #     text_ycors.append(imcorstemp[1])  # Append tuple containing old and new y coordinate
        #     good_line = Bubble.font.render(line, True, (255, 0, 255))  # Render font to surface
        #     chat_surface.blit(good_line, imcorstemp)  # Blit our lines of text to chat surface
        #
        # ####################################################################

        return [text_xcors, text_ycors]


    def bubble_draw(self, chat_surface, text_xcors, text_ycors):  # SHOULD I ADD SCREEN DIMS?

        horz_cords = [min(text_xcors), max(text_xcors)]
        vert_cords = [min(text_ycors), max(text_ycors)]

        # print('ok')
        # print(horz_cords)
        # print(vert_cords)
        #
        # print('ok')
        # print(text_xcors)
        # print(text_ycors)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # NEED TO ACCOUNT FOR MARGINS BEFORE DRAWING ARCS, NEED TO TEST THIS
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # SCALE chat_bg surface TO CORRECT LENGTH BEFORE RENDERING TEXT!!
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        chat_surface.fill((255,255,255), (horz_cords[0], 0, horz_cords[1], vert_cords[1]))

        # Draw horizontal lines above and below our text
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], 0), (horz_cords[1], 0)], 5)
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], vert_cords[1]), (horz_cords[1], vert_cords[1])], 3)

        # Draw vertical lines besides our text
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[0], 0), (horz_cords[0], vert_cords[1])], 3)
        pg.draw.lines(chat_surface, (255, 0, 0), 0, [(horz_cords[1], 0), (horz_cords[1], vert_cords[1])], 3)


    def scroll(self, screen, background, text):  # NEED TO MAKE THIS SMOOTH??
        screen.blit(background, self.position, self.position)
        self.scrollH[1] -= 8
        self.position = self.image.get_rect().move(self.scrollH[0], self.scrollH[1])
        screen.blit(self.chat_bg, self.position)

        #screen.blit(self.image, self.position)  # Update the screen
        #self.addtext(self.image, text)  # Add text on top of chat bubbles (blit in function)

        self.addtext(self.chat_bg, text)
        pg.display.update()
        # DO I NEED TO BLIT OVER TEXT AREA????
        return self.scrollH[1]  # Update our bubble object's y cor


# def advance_conversation():  #  Advance the conversation forward by moving old texts up, erasing ones off-screen


def background_creator(input_color, screen):  # Create a simple background
    bg = pg.Surface(screen.get_size())  # Create a surface the size of our screen
                                        # that will serve as background
    bg.convert()
    bg.fill(input_color)  # Fill bg with color
    return bg

