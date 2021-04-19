# The Froggerithm

![The Froggerithm Logo](doc/image/The_Froggerithm_Logo.png?raw=true "The Froggerithm Logo")

As machine learning has become more and more ubiquitous over recent years,
it has come to play a greater and greater role in our lives. From the social
media posts we see, to the systems that monitor bank accounts for financial
fraud, this technology plays an important role in many of the technological
systems of the day. This project has no such high-minded goals, however. Our
algorithm will learn to do one thing, and one thing only.

Play Frogger.

This project will seek to recreate the classic arcade game Frogger, and then
build a machine learning AI to play it through the use of a genetic training
algorithm and neural network. The game and the AI will be built in Python,
using Pygame and the NEAT-python library.

# Prerequisites

- Python 3.7 (Note: newer versions will not work)

# Initial Setup

- Clone repository
- Open terminal on repository root directory
- `python --version` to verify python 3.7
- `python -m venv venv && "venv\Scripts\activate.bat" && pip install -r requirements.txt`
  to install dependencies
- `python src\main.py -train <generations>` to train the neural network
- `<generations>` determines the number of generations the neural network will be trained for using the NEAT algorithm

# AI Training

This project makes use of the NEAT-python library to handle most of the heavy lifting for the neural network. The documentation
for the NEAT-python library can be found [here](https://neat-python.readthedocs.io/en/latest/). The NEAT configuration
settings are stored in src/neat_config.txt. Descriptions of the config parameters and what they do can be found in the
NEAT-python documentation. Population checkpoints are saved every 100 generations and every 20 minutes in src/Checkpoints.
If you wish to load a population checkpoint rather than train from scratch, you can do so by uncommenting the line in
`run_neat()` inside the main method in main.py, which is labelled with a comment.

# Documentation

This project includes pydocs for all major functions and classes. The pdoc3 Python tool was used to auto-generate an HTML
tree containing all of the pydocs in the project which can be viewed in any major web browser by loading doc/src/index.html.
Any time a pydoc is changed in the project, ensure that this tree is re-generated using pydoc3. There is no need to rebuild
for folders that do not contain changes to the pydoc.

# Unit Testing

This project will primarily make use of the built-in Python unit testing framework.
All unit testing source should be placed in src\Unittests.

## Extra Credits

Logo created by Azariah Emond