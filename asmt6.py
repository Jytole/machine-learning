# Kyler Smith's Machine Scheduling Genetic Algorithm Code for Assignment 6

# Base Command: python asmt6.py

# Arguments: --n <int> --gens <int> --pc <float> --pm <float>

# Schedule Encoding
## For the machines with time intervals of 2 (machines 1 and 2)
## 0 => 1100
## 1 => 0110
## 2 => 0011

## For the machines with time intervals of 1 (machines 3 through 7)
## 0 => 1000
## 1 => 0100
## 2 => 0010
## 3 => 0001

import random
import argparse
import matplotlib.pyplot as plt

capacities = [20, 15, 35, 40, 15, 15, 10]
maxLoad = [80, 90, 65, 70]

# Generate and return a random binary array of size "size"
def createChromosome():
    newChrom = []
    while(True):
        # The 2 machines with two-season intervals
        for x in range(2):
            newChrom.append(int(random.random() * 3))
        # The 5 machines with one-season intervals
        for x in range(5):
            newChrom.append(int(random.random() * 4))
        if(isChromValid(newChrom)):
            return newChrom
        else:
            newChrom = []

def isChromValid(chrom):
    return fitnessFunc(chrom) >= 0

def fitnessFunc(chrom):
    minPowReserve = 150
    for season in range(4):
        powReserve = 150
        powReserve -= maxLoad[season]
        # Check the first two machines' encodings
        for machine in range(2):
            # Subtract machine capacity from reserve if it is offline during season
            if(season == 0 and chrom[machine] == 0):
                powReserve -= capacities[machine]
            elif(season == 1 and (chrom[machine] == 0 or chrom[machine] == 1)):
                powReserve -= capacities[machine]
            elif(season == 2 and (chrom[machine] == 1 or chrom[machine] == 2)):
                powReserve -= capacities[machine]
            elif(season == 3 and chrom[machine] == 2):
                powReserve -= capacities[machine]
        for machine in range(5):
            machine += 2
            # This one is much easier! the encoding of machines 3-7 are the same as season
            if(season == chrom[machine]):
                powReserve -= capacities[machine]
        if(powReserve < minPowReserve):
            minPowReserve = powReserve
    return minPowReserve

# Randomly choose which element in a gene to mutate
def mutateChrom(chrom):
    mutIndex = int(random.random() * len(chrom))
    # If mutIndex is 0 or 1, let the new gene be 0, 1, or 2 (but not what it started as)
    if(mutIndex < 2):
        chrom[mutIndex] = (int(random.random() * 2) + chrom[mutIndex]) % 3
    # Otherwise, let it be 0, 1, 2, or 3 (but not the intial val)
    else:
        chrom[mutIndex] = (int(random.random() * 3) + chrom[mutIndex]) % 4

def crossOverChrom(chrom1, chrom2):
    crossPoint = int(random.random() * (len(chrom1) - 2)) + 1
    if(crossPoint < 0):
        crossPoint = 0
    tmp = chrom1[:crossPoint]
    chrom1[:crossPoint] = chrom2[:crossPoint]
    chrom2[:crossPoint] = tmp

def generateOffspring(n, pc, pm, chromosomeArr):
    rouletteArr = []
    fitnesses = []
    chromSortedbyFitness = chromosomeArr

    # Set up the roulette Wheel
    # Start Preparing Fitnesses
    fitnessSum = 0
    for idx in range(n):
        fitnesses.append(fitnessFunc(chromosomeArr[idx]))
        fitnessSum += fitnesses[idx]

    # sort the fitness and chromSortedbyFitness Array (together, w/ fitness as key)
    for i in range(n):
        for j in range(n - i):
            j += i
            if(fitnesses[j] < fitnesses[i]):
                tmpFit = fitnesses[i]
                fitnesses[i] = fitnesses[j]
                fitnesses[j] = tmpFit

                tmpChrom = chromSortedbyFitness[i]
                chromSortedbyFitness[i] = chromSortedbyFitness[j]
                chromSortedbyFitness[j] = tmpChrom
        if(fitnessSum == 0): # Caught an error for divide by zero
            rouletteArr.append(fitnesses[i])
        else:
            rouletteArr.append(fitnesses[i] / fitnessSum)

    for x in range(n - 1):
        x += 1
        rouletteArr[x] += rouletteArr[x-1]
        
    newChromArr = []
    # Pick new chromosomes, but only allow valid chromosomes
    while(len(newChromArr) < n):
        # Pick 2 chromosome indices at random
        chromPickIdx1 = 0
        chromPickIdx2 = 0
        randPick1 = random.random()
        randPick2 = random.random()
        for y in range(n):
            if(rouletteArr[y] < randPick1):
                chromPickIdx1 = y
            if(rouletteArr[y] < randPick2):
                chromPickIdx2 = y

        chromPick1 = chromSortedbyFitness[chromPickIdx1]
        chromPick2 = chromSortedbyFitness[chromPickIdx2]

        # Allow crossover and mutation of chromosomes
        if(random.random() < pc):
            crossOverChrom(chromPick1, chromPick2)
        if(random.random() < pm):
            mutateChrom(chromPick1)
        if(random.random() < pm):
            mutateChrom(chromPick2)

        if(isChromValid(chromPick1) and isChromValid(chromPick2)):
            newChromArr.append(chromPick1)
            newChromArr.append(chromPick2)

    return newChromArr

def calculateMaxandAvg(n, chromosomeArr):
    fitnesses = []
    outputArr = []

    fitnessSum = 0
    maxFitIdx = 0
    for idx in range(n):
        fitnesses.append(fitnessFunc(chromosomeArr[idx]))
        fitnessSum += fitnesses[idx]
        if(fitnesses[idx] > fitnesses[maxFitIdx]):
            maxFitIdx = idx
    
    avgFitness = fitnessSum / n

    outputArr.append(avgFitness)
    outputArr.append(fitnesses[maxFitIdx])

    return outputArr

# Run the genetic process; returns an array of
# [avgFitness, maxFitness, maxX, maxY]
def geneticCycle(n, pc, pm, chromosomeArr):
    chromosomeArr = generateOffspring(n, pc, pm, chromosomeArr)
    
    return calculateMaxandAvg(n, chromosomeArr)

parser = argparse.ArgumentParser(prog='GeneticAlg', 
								 description='A Python Script to Run a Genetic Algorithm')
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

args = parser.parse_args()

pm = args.pm #probability of mutation
pc = args.pc #probability of crossover
n = args.n #number of chromosomes
gens = args.gens #number of generations

chromosomeArr = []

# Initialize Chromosomes
for x in range(n):
    newChrom = createChromosome()
    chromosomeArr.append(newChrom)

maxPlotArr = []
avgPlotArr = []
maxFit = 0.0

# Run and print for each Generation
for x in range(gens):
    # geneticCycle Returns [avgFit, maxFit, maxX, maxY]
    output = geneticCycle(n, pc, pm, chromosomeArr)
    if(output[1] > maxFit):
        maxFit = output[1]
    maxPlotArr.append(maxFit)
    avgPlotArr.append(output[0])
    print("Generation " + str(x+1) + ": Max Fitness = " + str(maxFit) + "\nAverage Fitness = " + str(output[0]) + "\n")


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