from dpongpy.model import Pong, Config
from dpongpy.view import PongView
from dpongpy.controller import PongController
import pygame
from dataclasses import dataclass, field


@dataclass
class Settings:
    config: Config = field(default_factory=Config)
    debug: bool = False
    size: tuple = (800, 600)
    fps: int = 60


def main(settings: Settings = None):
    if settings is None:
        settings = Settings()

    pong = Pong(size=settings.size, config=settings.config)
    view = PongView(pong, debug=settings.debug)
    controller = PongController(pong)
    clock = pygame.time.Clock()
    running = True

    def stop(_):
        nonlocal running
        running = False

    controller.on_quit = stop

    dt = 0
    pygame.init()
    while running:
        controller.update(dt)
        view.render()
        pygame.display.flip()
        dt = clock.tick(settings.fps) / 1000
    pygame.quit()
