# Architecture

## Game Architecture

Frogger is a fairly simple game, so overthinking it and making it overly
complex might only make it more difficult to make a functional game with
enough time left over to build the machine learning systems. So the game
architecture itself will be fairly simple. It will consist of three main
systems:

1. The main game loop
2. Game engine
3. Sprite objects

The main game loop will consist of the main while loop that runs the game
until the player requests to stop. In addition, it will set the frame
rate and call all the main functions of the game from the game engine.

The game engine will have functions in it that handle most of the core
game tasks that will need to be done from frame to frame. These core
tasks include, but are not necessarily limited to, sprite rendering,
sprite movements, animations, handling player input, and spawning
obstacles. It will also feed information back to the main game loop for 
the AI to interact with such as the score, the position of various sprites,
and information about what actions are available to the player.

The sprite objects will extend the Pygame sprite class and store the game
data of each individual sprite object. This data can then be manipulated
by the engine to produce animations, move the sprite, render it, or kill
it.

## AI Architecture

The AI architecture also need not be too complex. While deep-learning
AI itself can be incredibly complex in its implementation, we will rely
on the Tensorflow framework to do most of the heavy lifting here. As such,
our AI will only need two main systems:

1. A system to initialize and store a neural network
2. A system to train that neural network to play the game

The former is rather straightforward. It will be a neural network system
that provides functionality to initialize, alter, and store the numerical
values in a neural network that represent the "current state" of the AI.

The latter will perhaps be somewhat more complex in its implementation, but
is nonetheless rather simple in concept. The training system will
initialize a neural network if it has not been done yet, and once it has,
it will interact with the game systems to maximize the neural network's
score in the game. It will also have an option to play the game using the
AI as-is, without training it, instead simply using the neural network
as it currently exists to attempt to play the game.

With these two main systems complete and functioning as intended, the 
overall structure of the project will look something like this:

![Diagram](../doc/image/Froggerithm Architecture.png?raw=true "Froggerithm Architecture")