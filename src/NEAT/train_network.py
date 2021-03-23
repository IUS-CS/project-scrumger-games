import main
import neat

def eval_genomes(genomes, config):
    nets = []
    games = []
    genome_list = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        games.append(main.main())
        genome_list.append(genome)


