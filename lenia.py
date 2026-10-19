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
friction = 0.1
def setup(count):
    for i in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        vx = 0
        vy = 0
        dots.append([x, y, vx, vy])
setup(20)

def iterate():
    for i in range(len(dots)):
        dots[i][2] += 1
        dots[i][3] += 0
        dots[i][2] *= (1-friction)
        dots[i][3] *= (1-friction)
        speed = speed_cap/((dots[i][2]**2 + dots[i][3]**2)**0.5)
        if speed <= 1:
            dots[i][2] *= speed
            dots[i][3] *= speed
        dots[i][2] *= (1-friction)
        dots[i][3] *= (1-friction)
    for i in range(len(dots)):
        dots[i][0] += dots[i][2]
        dots[i][1] += dots[i][3]
        dots[i][0] %= (WIDTH+1)
        dots[i][1] %= (HEIGHT+1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    iterate()
    for x, y, vx, vy in dots:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()