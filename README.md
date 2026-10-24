# Particle-Lenia

How to play!
first run the code then you will have a small screen showing the game itself.
to go to the website version then go to jplackal.itch.io
there you can also run the code

keybinds:

Space bar = pause
e  = editing mode
r = reset
l = larger select during Editing mode
k = smaller select during Editing mode
t = turn trail off and on
s = while paused use this to step one iteration forward

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