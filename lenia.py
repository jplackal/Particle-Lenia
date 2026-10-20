import pygame
import random

pygame.init()

WIDTH = 1440
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Lenia")

clock = pygame.time.Clock()
pos_and_vels = []
force_matrix = []
auto_create_matrix = 0
types = 3
if auto_create_matrix == 0:
    for i in range(0,types):
        force_matrix.append([random.randint(-1, 1) for _ in range(types)])
else:
    force_matrix = [
    [ 1,  1, -1],  # Type 0
    [-1,  1,  1],  # Type 1
    [ 1, -1, -1]   # Type 2
]
print(force_matrix)
matrix_colors = []

for i in range(len(force_matrix)):
    while True:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        if all(
            sum((color[j] - old[j])**2 for j in range(3)) > 10000
            for old in matrix_colors
        ):
            matrix_colors.append(color)
            break
min_range = 15
sense_dist = 100
speed = 0.15
speed_cap = 3
friction = 0.05
def calc_force(og, ch):
    global force
    force = force_matrix[og][ch]
def setup(count):
    global pos_and_vels, force_matrix
    for i in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        vx = 0
        vy = 0
        c = random.randint(0, int(len(force_matrix)-1))
        s = random.randint(4, 7)
        pos_and_vels.append([x, y, vx, vy, c, s])
setup(250)

def iterate():
    global speed, speed_cap, friction, force, sense_dist, min_range
    for i in range(len(pos_and_vels)):
        for o in range(len(pos_and_vels)):
            if i != o:
                dx = pos_and_vels[o][0] - pos_and_vels[i][0]
                dy = pos_and_vels[o][1] - pos_and_vels[i][1]

                if dx > WIDTH / 2:
                    dx -= WIDTH
                elif dx < -WIDTH / 2:
                    dx += WIDTH

                if dy > HEIGHT / 2:
                    dy -= HEIGHT
                elif dy < -HEIGHT / 2:
                    dy += HEIGHT

                dist = (dx**2 + dy**2)**0.5
                if dist <= min_range:
                    if dx != 0:
                        pos_and_vels[i][2] -= ((dx/dist)*speed)
                    if dy != 0:
                        pos_and_vels[i][3] -= ((dy/dist)*speed)
                elif dist <= sense_dist:
                    calc_force(pos_and_vels[i][4],pos_and_vels[o][4])
                    if dx != 0:
                        pos_and_vels[i][2] += ((dx/dist)*speed)*force
                    if dy != 0:
                        pos_and_vels[i][3] += ((dy/dist)*speed)*force


        pos_and_vels[i][2] *= (1-friction)
        pos_and_vels[i][3] *= (1-friction)
        if not(pos_and_vels[i][2] == 0 and pos_and_vels[i][3] == 0):
            curr_speed = speed_cap/((pos_and_vels[i][2]**2 + pos_and_vels[i][3]**2)**0.5)
            if curr_speed <= 1:
                pos_and_vels[i][2] *= curr_speed
                pos_and_vels[i][3] *= curr_speed
    for i in range(len(pos_and_vels)):
        pos_and_vels[i][0] += pos_and_vels[i][2]
        pos_and_vels[i][1] += pos_and_vels[i][3]
        pos_and_vels[i][0] %= (WIDTH+1)
        pos_and_vels[i][1] %= (HEIGHT+1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    iterate()
    for x, y, vx, vy, c, s in pos_and_vels:
        pygame.draw.circle(screen, matrix_colors[c], (x, y), s)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()