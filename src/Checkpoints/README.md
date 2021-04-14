#Checkpoints
This folder exists to hold NEAT checkpoints for resuming a simulation in case of a crash
or other stoppage during training. The training algorithm will save a checkpoint every
25 generations and save them to this folder under `neat-checkpoint-<generation>`.