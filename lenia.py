import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Lenia")

clock = pygame.time.Clock()
dots = []
min_range = 5
sense_dist = 200
speed = 1
speed_cap = 20
def setup(count):
    for i in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        dots.append((x, y))
setup(20)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x, y in dots:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()