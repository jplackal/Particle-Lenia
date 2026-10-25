#initializes the imports
import asyncio
import pygame
import random

pygame.init()
random.seed()
#sets the window width and height
WIDTH = 1300
HEIGHT = 750
#sets some simple variables like map sizes and camera location
game_width = int(2 * WIDTH)
game_height = int(2 * HEIGHT)
maxwidth = 0
maxheight = 0
minwidth = -game_width+WIDTH
minheight = -game_height+HEIGHT
stext2 = 0
cam_x = (WIDTH-game_width)/2
cam_y = (HEIGHT-game_height)/2
border = 1
uniform = 0
uniform_colors = 0

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
pentext = font.render("", True, (255, 255, 255))
pentext.set_alpha(256)

#this sets some more variables such as the setup lists
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
cam_speed = 10
pen = "drag"
#this function creates the force matrix which dictates how all the particles interact with eachother
def create_matrix():
    if auto_create_matrix == 0:
        return [
            [random.randint(-1, 1) for _ in range(types)]
            for _ in range(types)
        ]
    #paste the save code below in the square brackets
    return [[1, 1, -1], [0, -1, 1], [1, 1, -1]]
#sets up the matrix
force_matrix = create_matrix()
#prints the matrix so you can save it for later
print(force_matrix)

matrix_colors = []
#this function deletes all the particles in range of the dwidth
def delete():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(len(pos_and_vels) - 1, -1, -1):
        x, y, vx, vy, c, s = pos_and_vels[i]

        dist = ((mouse_x - (x + cam_x))**2 +
                (mouse_y - (y + cam_y))**2)**0.5

        if dist < dwidth:
            pos_and_vels.pop(i)
            drag.pop(i)
#this function creates the color matrix it sets the count of colors to the lenght of force matrix so it can match up nicely
def create_colors():
    colors = []

    for i in range(len(force_matrix)):
        while True:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            #this code makes sure that all the colors are diffrent from eachother
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
#this sets up some game variables like the speed and speed cap and more
min_range = 30
sense_dist = 200
speed = 0.30
speed_cap = 6
friction = 0.05
#this function finds distance in the drag function useing the mouse x and y so you can check the ones being dragged
def find_dist():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global pos_and_vels, dwidth, drag
    for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
        dist = ((mouse_x-(x+cam_x))**2+(mouse_y-(y+cam_y))**2)**0.5
        if dist <= dwidth:
            pos_and_vels[i][0] = 0-(mouse_x - pos_and_vels[i][0]) + WIDTH/2
            pos_and_vels[i][1] = 0-(mouse_y - pos_and_vels[i][1]) + HEIGHT/2
            drag[i] = True
#this function at the end of the drag function sets the positions of the particles after drag
def fix_dist():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global pos_and_vels, dwidth, drag, WIDTH, HEIGHT
    for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
        if drag[i]==True:
            pos_and_vels[i][0] = int(x+(mouse_x-WIDTH/2))
            pos_and_vels[i][1] = int(y+(mouse_y-HEIGHT/2))
            drag[i] = False
    
#this code should be longer but instead was one line 
def calc_force(og, ch):
    return force_matrix[og][ch]

#this setup makes all of the positons and velocities species/types and drag
def setup(count):
    global pos_and_vels, drag
    for i in range(count):
        x = random.randint(10, game_width - 10)
        y = random.randint(10, game_height - 10)
        vx = 0
        vy = 0
        c = random.randint(0, len(force_matrix) - 1)
        s = random.randint(4, 7)

        pos_and_vels.append([x, y, vx, vy, c, s])
        drag.append(False)


#this is the main code this code runs the checks for every one of particles and checks to force ofr each particle to each other particle that are in range
# so thats why this code is so laggy in the code there is a nested repeat look whcih compares every particle to every other
#thats 300 * 300 which is quite a lot
def iterate():
    for i in range(len(pos_and_vels)):
        for o in range(len(pos_and_vels)):
            if i == o:
                continue

            dx = pos_and_vels[o][0] - pos_and_vels[i][0]
            dy = pos_and_vels[o][1] - pos_and_vels[i][1]

            # Wrap distances around screen edges
            if dx > game_width / 2:
                dx -= game_width
            elif dx < -game_width / 2:
                dx += game_width

            if dy > game_height / 2:
                dy -= game_height
            elif dy < -game_height / 2:
                dy += game_height

            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Avoid division by zero
            if dist == 0:
                continue
            #min range is a variable that dictates wether if a particle is to close to another particle it repels no matter what
            if dist <= min_range:
                pos_and_vels[i][2] -= (dx / dist) * speed
                pos_and_vels[i][3] -= (dy / dist) * speed
            #checking wether the particles are in sensing distance
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
        #THIS code applies the speed cap
        if curr_speed > speed_cap:
            pos_and_vels[i][2] *= speed_cap / curr_speed
            pos_and_vels[i][3] *= speed_cap / curr_speed

    # Move particles and wrap around screen edges
    for particle in pos_and_vels:
        particle[0] = (particle[0] + particle[2]) % game_width
        particle[1] = (particle[1] + particle[3]) % game_height

#this is the main setup
setup(300)

#this is the main loop
async def main():
    global paused, text, force_matrix, matrix_colors, stext, textreset, editing, edit, dwidth, change, drag, trail, cam_speed, cam_x, cam_y, maxheight, maxwidth, minheight, minwidt, stext2, pen, uniform, border, uniform_colors

    running = True

    while running:

        #all this huge amount of code below its all of the keybinds for the editor camera and QOL improvements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                #these are all the keybinds which help all the features to run

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
                    setup(300)

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
                #this decreases the selection size
                elif event.key == pygame.K_k and editing:
                    dwidth -= change
                    dwidth = ((dwidth-change)%100)+change
                #this code increases the selection size
                elif event.key == pygame.K_l and editing:
                    dwidth += change
                    dwidth = ((dwidth-change)%100)+change
                #this code turns trial on and off
                elif event.key == pygame.K_t:
                    trail = 1-trail
                #this code helps the editor choose the drag setting
                elif event.key == pygame.K_1 and editing:
                    pen = "drag"
                    stext2 = 1
                #this code helps the editor choose the type 1 setting or species 1 for the particle
                elif event.key == pygame.K_2 and editing:
                    pen = "type 1"
                    stext2 = 1
                #this code helps the editor choose the type 2 setting or species 2 for the particles
                elif event.key == pygame.K_3 and editing:
                    pen = "type 2"
                    stext2 = 1
                #this code helps the editor choose the type 3 setting or species 3 for the particles
                elif event.key == pygame.K_4 and editing:
                    pen = "type 3"
                    stext2 = 1
                #this code selects the delete button and works with the selection sizes
                elif event.key == pygame.K_5 and editing:
                    pen = "delete"
                    stext2 = 1
                #this code helps change the sizes of the particles to all be set to 5.5 or they have their own sizes
                elif event.key == pygame.K_u:
                    uniform = 1-uniform
                #this code helps change whether the border shows or whether it hides
                elif event.key == pygame.K_b:
                    border = 1-border
                #this code helps change whether the particles share a similar color
                elif event.key == pygame.K_y:
                    uniform_colors = 1-uniform_colors
            #this code edits and adds diffrent species of particles or types of particles
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and editing:
                #this code helps dictate which type they add
                if pen == "type 1":
                    #this one adds type 1 or species 1
                    pos_and_vels.append([mouse_x-cam_x,mouse_y-cam_y,0,0,0,random.randint(4, 7)])
                elif pen == "type 2":
                    #this one adds type 2 or species 2
                    pos_and_vels.append([mouse_x-cam_x,mouse_y-cam_y,0,0,1,random.randint(4, 7)])
                elif pen == "type 3":
                    #this one adds type 3 or species 3
                    pos_and_vels.append([mouse_x-cam_x,mouse_y-cam_y,0,0,2,random.randint(4, 7)])

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
        #this dictates whether a trail appears or not
        if trail == 1:
            fade.fill((0, 0, 0, 45))
            screen.blit(fade, (0, 0))
        else:
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))

        #this code below writes the draggin code 

        if pygame.mouse.get_pressed()[0] and editing and pen == "drag":
            find_dist()
            while pygame.mouse.get_pressed()[0]:
                screen.fill((0, 0, 0))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
                    if uniform == 0:
                        #this code helps set the color
                        if uniform_colors:
                            color = (155,155,155)
                        else:
                            color = matrix_colors[c]
                        #this code uses the type or species color
                        if drag[i] == False:
                            #this code draws the circle while drag is not running
                            pygame.draw.circle(
                                screen,
                                color,
                                (int((x+cam_x)), int((y+cam_y))),
                                s
                                )
                        else:
                            #this code draws the circle with the offset of the mouse x and y  and draws it
                            pygame.draw.circle(
                                screen,
                                color,
                                (int(x+(mouse_x-WIDTH/2)+cam_x), int(y+(mouse_y-HEIGHT/2)+cam_y)),
                                s
                                )
                    else:
                        #this code draws the circles with a fixed size
                        #this code draws it when you are not dragging
                        if drag[i] == False:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int((x+cam_x)), int((y+cam_y))),
                                5.5
                                )
                        #this code draws the circle with the offset of mouse x and mouse y
                        else:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int(x+(mouse_x-WIDTH/2)+cam_x), int(y+(mouse_y-HEIGHT/2)+cam_y)),
                                5.5
                                )
                if editing:
                    pygame.draw.circle(screen, (255, 255, 255), (mouse_x,mouse_y), dwidth, 2)
                #this code draws all of the other features
                pygame.draw.rect(screen, (255, 255, 255), (0+cam_x, 0+cam_y, game_width, game_height), 2)
                pygame.display.flip()
                await asyncio.sleep(0)
                pygame.event.pump()
            fix_dist()

        #this code writes the delete particles code
        
        if pygame.mouse.get_pressed()[0] and editing and pen == "delete":
            while pygame.mouse.get_pressed()[0]:
                #this code is the loop that happens to delete the particles in range
                screen.fill((0, 0, 0))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                #this is the function that serves to delete the particles 
                delete()
                for i, (x, y, vx, vy, c, s) in enumerate(pos_and_vels):
                    #this code fixes the color
                    if uniform_colors:
                        color = (155,155,155)
                    else:
                        color = matrix_colors[c]
                    if uniform == 0:
                    #this code has random size not fixed
                    #this code does not work while dragging
                        if drag[i] == False:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int((x+cam_x)), int((y+cam_y))),
                                s
                                )
                    #this code helps with the dragging
                        else:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int(x+(mouse_x-WIDTH/2)+cam_x), int(y+(mouse_y-HEIGHT/2)+cam_y)),
                                s
                                )
                    else:
                    #this code has fixed sizes so the particles appear uniform 
                    #this one does not conform to the dragging
                        if drag[i] == False:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int((x+cam_x)), int((y+cam_y))),
                                5.5
                                )
                    #this one does work with the dragging so while dragging it shows correctly
                        else:
                            pygame.draw.circle(
                                screen,
                                color,
                                (int(x+(mouse_x-WIDTH/2)+cam_x), int(y+(mouse_y-HEIGHT/2)+cam_y)),
                                5.5
                                )
                
                if editing:
                    pygame.draw.circle(screen, (255, 255, 255), (mouse_x,mouse_y), dwidth, 2)
                if border == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (0+cam_x, 0+cam_y, game_width, game_height), 5)
                pygame.display.flip()
                await asyncio.sleep(0)
                pygame.event.pump()

        keys = pygame.key.get_pressed()

        #this code below changes the view of the camera
        #if any key is pressedit changes cam x and y and also limits it so you cant go past the game view
        if keys[pygame.K_UP]:
            cam_y+=cam_speed
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
            if cam_y > maxheight:
                cam_y = maxheight
        if keys[pygame.K_DOWN]:
            cam_y-=cam_speed
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
            if cam_y < minheight:
                cam_y = minheight
        if keys[pygame.K_LEFT]:
            cam_x+=cam_speed
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
            if cam_x > maxwidth:
                cam_x = maxwidth
        if keys[pygame.K_RIGHT]:
            cam_x-=cam_speed
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
            if cam_x < minwidth:
                cam_x = minwidth
        # Run continuously only when unpaused
        if paused == 0:
            iterate()

        if editing == 1:
            fade.fill((0, 0, 0, 255))
            screen.blit(fade, (0, 0))
        # Draw particles
        for x, y, vx, vy, c, s in pos_and_vels:
            if uniform_colors:
                color = (155,155,155)
            else:
                color = matrix_colors[c]
            if uniform == 1:
                pygame.draw.circle(
                    screen,
                    color,
                    (int(((x)+cam_x)), int(((y)+cam_y))),
                    5.5
                )
            else:
                pygame.draw.circle(
                    screen,
                    color,
                    (int(((x)+cam_x)), int(((y)+cam_y))),
                    s
                )
        #this shows the selection range only if your pen is "drag" or "delete"
        if editing == 1 and (pen == "drag" or pen == "delete"):
            pygame.draw.circle(screen, (255, 255, 255), (mouse_x,mouse_y), dwidth, 2)
        #this shows if the border is showing
        if border == 1:
            pygame.draw.rect(screen, (255, 255, 255), (0+cam_x, 0+cam_y, game_width, game_height), 5)
        screen.blit(text, (10, HEIGHT - 50))
        screen.blit(textreset, (10, HEIGHT - 50))
        screen.blit(edit, (WIDTH-150, HEIGHT - 50))
        if stext2 != 0:
            pentext = font.render(
                f"Pen set to {pen}", True, (255, 255, 255)
            )
            stext2 += 1
            screen.blit(pentext, (10, 10))
        if stext2 > 30:
            stext2 = 0
        pygame.display.flip()
        clock.tick(60)

        # Allows asyncio-based environments to continue running
        await asyncio.sleep(0)

asyncio.run(main())
#the end
# Saved patterns:
#[1, 1, -1], [0, -1, 1], [1, 1, -1] a cool cross looking thing
#[0, 1, 0], [1, -1, 1], [-1, -1, 1] some string like lifeforms
#[0, 0, 1], [1, -1, 1], [0, 1, 0] circles