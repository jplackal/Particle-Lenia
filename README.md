# Particle-Lenia

How to play!
first run the code then you will have a small screen showing the game itself.
to go to the website version then go to jplackal.itch.io
there you can also run the code

basic keybinds!
    these are the basic keybinds that are used 
    Space bar = pause
    e  = editing mode
    r = reset
    l = larger select during Editing mode
    k = smaller select during Editing mode
    t = turn trail off and on
    s = while paused use this to step one iteration forward


editor keybinds!
    these keybinds h
    1 = drag mode 
            drag particles around that are in the selection range use this to pit your creatures against eachother say if you have two you can move them closer and see what happens
    2 = type 1 spawn
            this keybind when mouse clicked spawns a type 1 particle or species 1 particle use this to slowly build up your creature
    3 = type 2 spawn
            this keybind when mouse clicked spawns a type 2 particle or species 2 particle use this to slowly build up your creature
    4 = type 3 spawn
            this keybind when mouse clicked spawns a type 3 particle or species 3 particle use this to slowly build up your creature
    5 = delete
            this tool lets you delete creatures and extra particles

view keybinds!
    these keybinds help you navigate the map!
    actoully they are straightforward just use the arrow keys to traverse
    left, right, up, down, arrow keys

how it works!
for this explanation im going to skip how the keybinds work instead go straight to how each particle behaves
each particle has their own type or species
at the start the code generates a force matrix which dictates how particle species interact such as 
how the blue species interect with red species.
then there are also some starting variables that go for all particles like sensing distance
sensing distance is how a close a particle has to be to sense another particle
and there also other variables like min dist
min dist tells if particles are to close they always repel. this helps avoid particles to combine/merge and just make the project more laggy
the other variables are self explanatory
every frame the iterate function calculates the new position and velocities for each particle and then after that displays them
so thats how particle lenia works

the rest of the project are just side features such as pausing editing and more