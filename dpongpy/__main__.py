from dpongpy.model import *
from dpongpy.view import PongView
from dpongpy.controller import PongController
import pygame


pygame.init()
pong = Pong(size=(1280, 720))
view = PongView(pong, debug=True)
controller = PongController(pong)
clock = pygame.time.Clock()
running = True
dt = 0


def stop(pong: Pong):
    global running
    running = False


controller.on_quit = stop
while running:
    controller.update(dt)
    view.render()
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
