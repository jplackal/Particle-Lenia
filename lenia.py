import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Lenia")

clock = pygame.time.Clock()
dots = []
forces = [[1,-1],[-1,1]]
min_range = 50
sense_dist = 200
speed = 1
speed_cap = 3
friction = 0.3
force = 1
def calc_force(og, ch):
    global force
    force = forces[og][ch]
def setup(count):
    global dots, forces
    #for i in range(0,2):
        #forces.append([-1,-1])
    for i in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        vx = 0
        vy = 0
        c = random.randint(0, 1)
        s = random.randint(4, 7)
        dots.append([x, y, vx, vy, c, s])
setup(250)

def iterate():
    global speed, speed_cap, friction, force, sense_dist, min_range
    for i in range(len(dots)):
        for o in range(len(dots)):
            if i != o:
                dx = dots[o][0]-dots[i][0]
                dy = dots[o][1]-dots[i][1] 
                dist = (dx**2 + dy**2)**0.5
                if dist <= min_range:
                    if dx != 0:
                        dots[i][2] -= ((dx/dist)*speed)
                    if dy != 0:
                        dots[i][3] -= ((dy/dist)*speed)
                elif dist <= sense_dist:
                    calc_force(dots[i][4],dots[o][4])
                    if dx != 0:
                        dots[i][2] += ((dx/dist)*speed)*force
                    if dy != 0:
                        dots[i][3] += ((dy/dist)*speed)*force


        dots[i][2] *= (1-friction)
        dots[i][3] *= (1-friction)
        if not(dots[i][2] == 0 and dots[i][3] == 0):
            curr_speed = speed_cap/((dots[i][2]**2 + dots[i][3]**2)**0.5)
            if curr_speed <= 1:
                dots[i][2] *= curr_speed
                dots[i][3] *= curr_speed
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
    for x, y, vx, vy, c, s in dots:
        if c == 0:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), s)
        elif c == 1:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), s)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()