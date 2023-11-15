# Code written by Kyler Smith

# This code features a command line parser (argparse) that makes testing with different values easier.
# minimum command to run:
# python asmt5-5.py OR python3 asmt5-5.py

# Command with all (optional) arguments
# python asmt5-5.py --pm 0.001 --pc 0.7 --n 6 --gens 20 --graph True

import random
import argparse
import math
import matplotlib.pyplot as plt

# Generate and return a chromosome array
def createChromosome():
    binaryArr = []
    for x in range(16):
        binaryArr.append(random.random() >= 0.5)
    return binaryArr

# Assumes binary array is stored with LSB first (in backwards order) for convenience
def binaryToInt(binaryArr):
    intval = 0
    # translate from binary to int
    for idx in range(len(binaryArr)):
        intval = intval + 2**idx * binaryArr[idx]
    return (0.0235294 * intval) - 3

# Randomly choose whether to mutate a gene
def mutate(binaryArr):
    mutIndex = int(random.random() * len(binaryArr))
    binaryArr[mutIndex] = not binaryArr[mutIndex]

# An alternative function to mutate all genes in all chroms
def mutateAll(numChrom, probMut, chromosomeArr):
    for i in range(numChrom):
        for j in range(len(chromosomeArr[0])):
            if(random.random() < probMut):
                chromosomeArr[i][j] = not chromosomeArr[i][j]
    return chromosomeArr

def crossOver(binaryArr1, binaryArr2):
    crossPoint = int(random.random() * len(binaryArr1))
    if(crossPoint < 0):
        crossPoint = 0
    for x in range(crossPoint):
        tmp = binaryArr1[x]
        binaryArr1[x] = binaryArr2[x]
        binaryArr2[x] = tmp

def fitnessFunc(x, y):
    return ((1-x)**2)*math.exp(-(x**2) - ((y+1)**2)) - (x - (x**3) - (y**3)) * math.exp(-(x**2)-(y**2))

def getFitnessFromChrom(chrom):
    split = int(len(chrom) / 2)
    # Y is first, X is second in the chromosome array
    y = binaryToInt(chrom[:split])
    x = binaryToInt(chrom[split:])
    return fitnessFunc(x,y)

def newGeneration(numChrom, chromosomeArr):
    rouletteArr = []
    fitnesses = []
    chromSortedbyFitness = chromosomeArr

    # Set up the roulette Wheel
    # Start Preparing Fitnesses
    fitnessSum = 0
    minFitIdx = 0
    for idx in range(numChrom):
        fitnesses.append(getFitnessFromChrom(chromosomeArr[idx]))
        if(fitnesses[idx] < fitnesses[minFitIdx]):
            minFitIdx = idx

    posOffset = 0

    if fitnesses[minFitIdx] < 0:
        posOffset = -fitnesses[minFitIdx]

    # Offset and sum the fitnesses
    for idx in range(numChrom):
        fitnesses[idx] += posOffset
        fitnessSum += fitnesses[idx]

    # sort the fitness and chromSortedbyFitness Array (together, w/ fitness as key)
    for i in range(numChrom):
        for j in range(numChrom - i):
            j += i
            if(fitnesses[j] < fitnesses[i]):
                tmpFit = fitnesses[i]
                fitnesses[i] = fitnesses[j]
                fitnesses[j] = tmpFit

                tmpChrom = chromSortedbyFitness[i]
                chromSortedbyFitness[i] = chromSortedbyFitness[j]
                chromSortedbyFitness[j] = tmpChrom
        rouletteArr.append(fitnesses[i] / fitnessSum)

    for x in range(numChrom - 1):
        x += 1
        rouletteArr[x] += rouletteArr[x-1]
        
    newChromArr = []
    chromPick = 0
    # Pick new chromosomes
    for x in range(numChrom):
        randPick = random.random()
        for y in range(numChrom):
            if(rouletteArr[y] < randPick):
                chromPick = y
        newChromArr.append(chromSortedbyFitness[chromPick])

    return newChromArr

def geneticCycle(numChrom, probCross, probMut, chromosomeArr, maxes, maxPlotArr, avgPlotArr):
    chromosomeArr = newGeneration(numChrom, chromosomeArr)

    # Crossover
    for i in range(int(numChrom / 2)):
        if(random.random() < probCross):
            crossOver(chromosomeArr[i], chromosomeArr[i*2])

    # Mutate
    # for i in range(numChrom):
    #     if(random.random() < probMut):
    #         mutate(chromosomeArr[i])

    chromosomeArr = mutateAll(numChrom, probMut, chromosomeArr)

    # calculate output values
    rouletteArr = []
    fitnessSum = 0
    maxFitIdx = 0
    for idx in range(numChrom):
        fitness = getFitnessFromChrom(chromosomeArr[idx])
        fitnessSum += fitness
        rouletteArr.append(fitness)
        if fitness > rouletteArr[maxFitIdx]:
            maxFitIdx = idx

    if((rouletteArr[maxFitIdx]) > maxes[0]):
        maxes[0] = (rouletteArr[maxFitIdx])
        split = int(len(chromosomeArr[maxFitIdx]) / 2)
        # Y is first, X is second in the chromosome array
        maxes[2] = binaryToInt(chromosomeArr[maxFitIdx][:split])
        maxes[1] = binaryToInt(chromosomeArr[maxFitIdx][split:])
    
    output = "Max Fitness: " + str(maxes[0])

    # Finish Calculating Fitnesses (need the sum first)
    for idx in range(numChrom):
        rouletteArr[idx] = rouletteArr[idx] / fitnessSum

    output += " with x = " + str(maxes[1])
    output += " and y = " + str(maxes[2])
    output += "\n Average Fitness: " + str(fitnessSum / numChrom)

    maxPlotArr.append(maxes[0])
    avgPlotArr.append(fitnessSum / numChrom)

    return output

    

parser = argparse.ArgumentParser(prog='TheraGen', 
								 description='A Python Script to Generate Bark and Pant Audio for Therabot')
# The arguments used to produce audio
# Mood Pattern: pattern of letters to translate into  
parser.add_argument('--pm', default=0.001, type=float,
					help="the probability of mutation")
parser.add_argument('--pc', default=0.7, type=float,
                    help="the probability of crossover")
parser.add_argument('--n', default=10, type=int,
                    help="the number of chromosomes, this is preferably even")
parser.add_argument('--gens', default=20, type=int,
                    help="the number of generations")
parser.add_argument('--graph', default=True, type=bool,
                    help="a flag to determine whether or not to show the graph of fitnesses")

args = parser.parse_args()

probMut = args.pm #probability of mutation
probCross = args.pc #probability of crossover
numChrom = args.n #number of chromosomes
numGenerations = args.gens #number of generations
graphFlag = args.graph

chromosomeArr = []

# Initialize Chromosomes
for x in range(numChrom):
    newChrom = createChromosome()
    chromosomeArr.append(newChrom)

# Arrary of maxFit, maxX, and maxY, in that order
maxes = [0.0, 0.0, 0.0]
maxPlotArr = []
avgPlotArr = []

# Run and print for each Generation
for x in range(numGenerations):
    output = geneticCycle(numChrom, probCross, probMut, chromosomeArr, maxes, maxPlotArr, avgPlotArr)
    print("Generation " + str(x+1) + ": " + output + "\n")

if(graphFlag):
    plt.plot(range(len(maxPlotArr)), maxPlotArr, label = "Max Fitness") 
    
    # plotting the line 2 points  
    plt.plot(range(len(avgPlotArr)), avgPlotArr, label = "Average Fitness Value")
    
    plt.xlabel('Generation')
    plt.ylabel('Fitness Value')
    plt.title('Fitness Value Comparison')

    # show a legend on the plot 
    plt.legend() 
    
    # function to show the plot 
    plt.show() 