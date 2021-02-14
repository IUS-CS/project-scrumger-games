#Project Proposal
* Group Name: Scrumger Games
* Project Name: The Froggerithm

This project seeks to recreate the classic arcade game *Frogger* and teach a machine
learning AI to play the game with a genetic training algorithm and a neural network.
Using Python as the primary language, our plan is to build *Frogger* using Pygame
and teach the AI using Tensorflow. To teach the AI, we will use the evolutionary
algorithm NEAT (NeuroEvolution of Augmenting Topologies) with Python. 

In *Frogger*, the player has one basic objective: to get from the bottom of the 
screen to the top of the screen without getting hit by a car or falling into the
river. The player can move in four different directions to accomplish this: forwards,
backwards, left, and right. To train the AI when to move and what direction to move, 
the main parameters will be the distance from obstacles on all four sides. Those 
parameters will translate through the neural network into one of two outputs: jump or
don't jump. If the output is to jump, then it will be translated into one of the 
four directions.