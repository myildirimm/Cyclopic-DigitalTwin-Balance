import os
import pygame
import time
import random
import main
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
from utils import plotData

LEARN = True  # enable learn if true


def init_pygame():
    x = 0
    y = 300
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
    pygame.init()

    X = 800  # Width of the window
    Y = 600  # Height of the window
    ds = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("Cyclopic Balance Test")

    return ds


class Scenario():
    def __init__(self):

        self.running = True
        self.timestep = 1 / 25
        self.start_time = 0
        self.t_count = 1
        self.white = (255, 255, 255)


        # add the agent car
        self.agent = main.Cyclopic(width=WIDTH, height=HEIGHT, track=INIT_TRACK, speed=INIT_SPEED,
                                    direction=INIT_DIRECTION, eps=0)


    def plot_scenario(self,display_surface):
        print('scenario start')
        self.start_time = time.time()
        avg_losses = []
        i = 0

        while self.running:
            display_surface.fill(self.white)
            display_surface.blit(self.image, (0, 0))
            rect_list = []
            velocities = []

            i += 1

            # update and draw the agent
            reset, _  = self.agent.update( self.timestep, rect_list, velocities, display_surface, learn=LEARN )
            self.agent.draw( display_surface )

            avg_losses.append( np.average( self.agent.dq_agent.losses ) )
            self.agent.dq_agent.losses = []

            pygame.display.update()
            if i==int(self.frame_len):
                pygame.QUIT
                self.running=False

                self.agent.dq_agent.net.save_weights("weights/test_weights")
                plotData( avg_losses, 'Loss', 'Episode', 'Loss', 'fig_Q_validateion_Loss.png' )

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    self.running = False

                    # save weight file
                    if LEARN:
                        self.agent.dq_agent.net.save_weights("weights/weights")
                        # plot the losses
                        plotData( avg_losses, 'Loss', 'Episode', 'Loss', 'fig_Q_validateion_Loss.png' )

            self.sleep()
            self.t_count = self.t_count + 1

            if self.t_count == len( self.frame_list ):
                self.t_count = 1

        pygame.quit()

    def sleep(self):
        local_time = time.time() - self.start_time
        sleep_time = self.t_count * self.timestep - local_time
        if sleep_time > 0.1:
            sleep_time = 0.1
        elif sleep_time > 0:
            time.sleep(sleep_time)

    def close(self):
        self.running = False

if __name__ == '__main__':
    display_surface = init_pygame()
    scenario_data = Scenario()
    scenario_data.plot_scenario(display_surface)
