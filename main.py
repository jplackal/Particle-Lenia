
import asyncio
import pygame
import random

pygame.init()
random.seed()

WIDTH = 1300
HEIGHT = 750

fade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Lenia")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

text = font.render("", True, (255, 255, 255))
text.set_alpha(256)

textreset = font.render("", True, (255, 255, 255))
textreset.set_alpha(256)
edit = font.render("", True, (255, 255, 255))
edit.set_alpha(256)

pos_and_vels = []
force_matrix = []
drag = []
auto_create_matrix = 0
types = 3
paused = 0
stext = 0
editing = 0
dwidth = 20
change = 10
trail = 1

def create_matrix():
    if auto_create_matrix == 0:
        return [
            [random.randint(-1, 1) for _ in range(types)]
            for _ in range(types)
        ]

    return [
        [1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1]
    ]


force_matrix = create_matrix()
print(force_matrix)

matrix_colors = []


def create_colors():
    colors = []

    for i in range(len(force_matrix)):
        while True:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            if all(
                sum(
                    (color[j] - old[j]) ** 2
                    for j in range(3)
                ) > 10000
                for old in colors
            ):
                colors.append(color)
                break

    return colors


matrix_colors = create_colors()

min_range = 15
sense_dist = 100
speed = 0.15
speed_cap = 3
friction = 0.05

def find_dist():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global pos_and_vels, dwidth, drag
    for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
        dist = ((mouse_x-x)**2+(mouse_y-y)**2)**0.5
        if dist <= dwidth:
            pos_and_vels[i][0] = 0-(mouse_x - pos_and_vels[i][0]) + WIDTH/2
            pos_and_vels[i][1] = 0-(mouse_y - pos_and_vels[i][1]) + HEIGHT/2
            drag[i] = True
def fix_dist():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global pos_and_vels, dwidth, drag, WIDTH, HEIGHT
    for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
        if drag[i]==True:
            pos_and_vels[i][0] = int(x+(mouse_x-WIDTH/2))
            pos_and_vels[i][1] = int(y+(mouse_y-HEIGHT/2))
            drag[i] = False
    

def calc_force(og, ch):
    return force_matrix[og][ch]


def setup(count):
    global pos_and_vels, drag
    for i in range(count):
        x = random.randint(10, WIDTH - 10)
        y = random.randint(10, HEIGHT - 10)
        vx = 0
        vy = 0
        c = random.randint(0, len(force_matrix) - 1)
        s = random.randint(4, 7)

        pos_and_vels.append([x, y, vx, vy, c, s])
        drag.append(False)



def iterate():
    for i in range(len(pos_and_vels)):
        for o in range(len(pos_and_vels)):
            if i == o:
                continue

            dx = pos_and_vels[o][0] - pos_and_vels[i][0]
            dy = pos_and_vels[o][1] - pos_and_vels[i][1]

            # Wrap distances around screen edges
            if dx > WIDTH / 2:
                dx -= WIDTH
            elif dx < -WIDTH / 2:
                dx += WIDTH

            if dy > HEIGHT / 2:
                dy -= HEIGHT
            elif dy < -HEIGHT / 2:
                dy += HEIGHT

            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Avoid division by zero
            if dist == 0:
                continue

            if dist <= min_range:
                pos_and_vels[i][2] -= (dx / dist) * speed
                pos_and_vels[i][3] -= (dy / dist) * speed

            elif dist <= sense_dist:
                force = calc_force(
                    pos_and_vels[i][4],
                    pos_and_vels[o][4]
                )

                pos_and_vels[i][2] += (dx / dist) * speed * force
                pos_and_vels[i][3] += (dy / dist) * speed * force

        # Apply friction
        pos_and_vels[i][2] *= (1 - friction)
        pos_and_vels[i][3] *= (1 - friction)

        # Limit speed
        vx = pos_and_vels[i][2]
        vy = pos_and_vels[i][3]
        curr_speed = (vx ** 2 + vy ** 2) ** 0.5

        if curr_speed > speed_cap:
            pos_and_vels[i][2] *= speed_cap / curr_speed
            pos_and_vels[i][3] *= speed_cap / curr_speed

    # Move particles and wrap around screen edges
    for particle in pos_and_vels:
        particle[0] = (particle[0] + particle[2]) % WIDTH
        particle[1] = (particle[1] + particle[3]) % HEIGHT


setup(250)


async def main():
    global paused, text, force_matrix, matrix_colors, stext, textreset, editing, edit, dwidth, change, drag, trail

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Space: pause or resume
                if event.key == pygame.K_SPACE and editing == 0:
                    paused = 1 - paused
                    stext = 0

                    if paused:
                        text = font.render(
                            "Paused", True, (255, 255, 255)
                        )
                    else:
                        text = font.render(
                            "", True, (255, 255, 255)
                        )

                # R: reset the simulation
                elif event.key == pygame.K_r:
                    stext = 1
                    editing = 0
                    edit = font.render(
                "", True, (255, 255, 255)
            )
                    if editing == 0:
                        paused = 0
                    text = font.render("", True, (255, 255, 255))

                    force_matrix = create_matrix()
                    print(force_matrix)

                    matrix_colors = create_colors()

                    pos_and_vels.clear()
                    drag.clear()
                    setup(250)

                # S: advance one step while paused
                elif event.key == pygame.K_s and paused:
                    iterate()
                elif event.key == pygame.K_e:
                    paused = 1
                    editing = 1-editing
                    if editing == 0:
                        edit = font.render(
                "", True, (255, 255, 255)
            )
                    else:
                        edit = font.render(
                "Editing", True, (255, 255, 255)
            )
                    if paused:
                        text = font.render(
                            "Paused", True, (255, 255, 255)
                        )
                    else:
                        text = font.render(
                            "", True, (255, 255, 255)
                        )
                elif event.key == pygame.K_k and editing:
                    dwidth -= change
                    dwidth = ((dwidth-change)%100)+change
                elif event.key == pygame.K_l and editing:
                    dwidth += change
                    dwidth = ((dwidth-change)%100)+change
                elif event.key == pygame.K_t:
                    trail = 1-trail



        # Show the reset message briefly
        if stext != 0:
            textreset = font.render(
                "Reset", True, (255, 255, 255)
            )
            stext += 1
        else:
            textreset = font.render("", True, (255, 255, 255))

        if stext >= 20:
            stext = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if trail == 1:
            fade.fill((0, 0, 0, 45))
            screen.blit(fade, (0, 0))
        else:
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))

        if pygame.mouse.get_pressed()[0] and editing:
            find_dist()
            while pygame.mouse.get_pressed()[0]:
                screen.fill((0, 0, 0))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
                    if drag[i] == False:
                        pygame.draw.circle(
                            screen,
                            matrix_colors[c],
                            (int(x), int(y)),
                            s
                            )
                    else:
                        pygame.draw.circle(
                            screen,
                            matrix_colors[c],
                            (int(x+(mouse_x-WIDTH/2)), int(y+(mouse_y-HEIGHT/2))),
                            s
                            )
                if editing:
                    pygame.draw.circle(screen, (255, 255, 255), (mouse_x,mouse_y), dwidth, 2)

                pygame.display.flip()
                await asyncio.sleep(0)
                pygame.event.pump()
            fix_dist()


        # Run continuously only when unpaused
        if paused == 0:
            iterate()

        if editing == 1:
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
        # Draw particles
        for x, y, vx, vy, c, s in pos_and_vels:
            pygame.draw.circle(
                screen,
                matrix_colors[c],
                (int(x), int(y)),
                s
            )
        if editing == 1:
            pygame.draw.circle(screen, (255, 255, 255), (mouse_x,mouse_y), dwidth, 2)

        screen.blit(text, (10, HEIGHT - 50))
        screen.blit(textreset, (10, HEIGHT - 50))
        screen.blit(edit, (WIDTH-150, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

        # Allows asyncio-based environments to continue running
        await asyncio.sleep(0)


asyncio.run(main())


# Saved patterns:
# [[1, 1, 1], [-1, 1, 0], [0, 0, -1]]
