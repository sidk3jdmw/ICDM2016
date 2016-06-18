import random
import sys
from random import randint
from deap import base
from deap import creator
from deap import tools
from evaluator import Evaluater
from multiprocessing import Pool
from hospital import HospitalList
from patient import PatientList, week_filter
from helper import Huff
from position import PositionList, Position
import numpy as np
import time

process = 4

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()


# algorithm arguments init
CXPB, MUTPB, NGEN, NPOP = 0.5, 0.4, 1, 10
TERMINATE = 10

# evaluator arguments init
total_capacity = 3000
window_size = 3
tmp_num = 8
tmp_max_list = [90] * tmp_num

# huff arguments init
alpha = 1
beta = 1
ignore_prob = 0.01
reachable_dist = 0.02
huff = Huff(alpha, beta, reachable_dist, ignore_prob)


def get_init_pos_list(x_r, y_r, d):
    pos_list = PositionList()
    pos_list.xnum = len(np.arange(x_r[0], x_r[1], d))
    pos_list.ynum = len(np.arange(y_r[0], y_r[1], d))
    for y in np.arange(y_r[0], y_r[1], d):
        for x in np.arange(x_r[0], x_r[1], d):
            pos_list.append(Position(x, y))
    return pos_list


# init
hospital_list = HospitalList()
hospital_list.read_file("hospital_high_capacity.tsv")

pat_list = PatientList()
pat_list.read_file("sorted.tsv")
pat_list.build_relations(hospital_list, huff)


pos_list = get_init_pos_list((pat_list.xmin, pat_list.xmax), (pat_list.ymin, pat_list.ymax), 0.005)
e = Evaluater(hospital_list, pat_list, total_capacity, window_size, tmp_max_list, huff, "DP")


def randPosition(pos_list=pos_list):
    r = random.randint(0, len(pos_list) - 1)
    return pos_list[r]

def randGene(ind):
    m = [randPosition() for i in range(len(e.t_list))]

    return ind(m)

def mutGene(ind):
    for i in range(len(ind)):
        r = randint(0, len(e.t_list) - 1)
        if r < 0.8:
            # ind[i][j] = (randrange(e.xmin, e.xmax), randrange(e.ymin, e.ymax))
            ind[i] = randPosition()
    return ind


def cxCapacity(ind1, ind2):
    ind1, ind2 = tools.cxTwoPoint(ind1, ind2)
    return ind1, ind2

toolbox.register("individual", randGene, creator.Individual)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", e.eval)

toolbox.register("mate", tools.cxTwoPoint)

toolbox.register("mutate", mutGene)

toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    # multiprocesssing pool
    p = Pool(process)
    pop = toolbox.population(n=NPOP)
    terminate_count = 0
    pre_best = 0
    start_time = time.time()

    print("Start of evolution")
    toolbox.evaluate(pop[0])
    fitnesses = list(p.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit


    # Begin the evolution
    for g in range(NGEN):
        # print("-- Generation %i --" % g)

        offspring = toolbox.select(pop, len(pop))
        offspring = list(p.map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = p.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        max_fits = max(fits)
        print(g, max_fits)
        if max_fits <= pre_best:
            terminal_count += 1
        else:
            pre_best = max_fits
            terminate_count = 0
        if terminate_count > TERMINATE:
            break
        # print("  Max %s" % max(fits))

    best_ind = tools.selBest(pop, 1)[0]
    print("Time: ", time.time() - start_time)
    print(best_ind.fitness.values, [(pos.x, pos.y) for pos in best_ind])

if __name__ == "__main__":
    main()