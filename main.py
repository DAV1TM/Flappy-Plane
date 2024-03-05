import pygame
from pygame.locals import *
import sys
import random

class FlappyPlane:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((400, 708))
        self.Plane = pygame.Rect(40, 40, 170, 70)
        self.background = pygame.image.load("src/city.png").convert()
        self.PlaneSprites = [pygame.image.load("src/plane.png").convert_alpha(),
                            pygame.image.load("src/deadplane.png")]
        self.wallUp = pygame.image.load("src/tower_top.png").convert_alpha()
        self.wallDown = pygame.image.load("src/tower_down.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.PlaneY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.high_score = 0
        self.offset = random.randint(-110, 110)
        self.crash_sound = pygame.mixer.Sound("sounds/crash.mp3")

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            if self.counter > self.high_score:
                self.high_score = self.counter
            self.offset = random.randint(-110, 110)

    def PlaneUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.PlaneY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.PlaneY += self.gravity
            self.gravity += 0.2
        self.Plane[1] = self.PlaneY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.Plane) or downRect.colliderect(self.Plane):
            self.dead = True
            self.crash_sound.play()

        if not 0 < self.Plane[1] < 720:
            self.Plane[1] = 50
            self.PlaneY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font_size = 30 
        font = pygame.font.SysFont("Arial", font_size)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(f"Score: {self.counter}",
                                         -1,
                                         (255, 255, 255)),
                             ((self.screen.get_width() - font.size(f"Score: {self.counter}")[0]) // 2, 50))
            high_score_text = font.render(f"High Score: {self.high_score}",
                                          -1,
                                          (255, 255, 255))
            self.screen.blit(high_score_text,
                             ((self.screen.get_width() - high_score_text.get_width()) // 2, 120))
            if self.dead:
                self.sprite = 1 
            elif self.jump:
                self.sprite = 0 
            if not self.dead:
                self.sprite = 0
            self.screen.blit(self.PlaneSprites[self.sprite], (70, self.PlaneY))
            self.updateWalls()
            self.PlaneUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyPlane().run()
