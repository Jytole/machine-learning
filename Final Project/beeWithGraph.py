# Documentation for the Pandas library was consulted for data preprocessing:
# https://pandas.pydata.org/docs/user_guide/
# Documentation for the bees_algorithm library was consulted for algorithm execution
# 

# Change these variables to change the number of iterations run or the hyperparameter "number of scouts"
iterations = 10
scouts = 10

from bees_algorithm import BeesAlgorithm
import pandas as pd
import matplotlib.pyplot as plt
import random
import pathlib

filePath = str(pathlib.Path(__file__).parent.resolve().absolute())

dataPath = filePath + '/data.csv'

# use pandas to import the csv file of the dataset
dataset = pd.read_csv(dataPath)

# pre-process the dataset (just set up usable series: one for all the inputs, and one for each decay coefficient)
inputs = dataset.drop(['index', 'GT Compressor decay state coefficient\xa0 ','GT Turbine decay state coefficient '],axis=1)

compressorDecay = dataset.filter(items=['GT Compressor decay state coefficient\xa0 '])

turbineDecay = dataset.filter(items=['GT Turbine decay state coefficient '])

# Create a basic dataset size variable for iteration purposes
dataPoints = turbineDecay.size

# estimate the decay given the inputs and weights
# returns a decimal value which represents the estimated decay
# INPUTS:
#   x: input values
#   w: input weights
# OUTPUT:
#   decimal estimate of the decay
def estimate(x, w):
    sum = 0
    for idx in range(len(x)):
        sum += x[idx] * w[idx]
    return sum

# calculate the fitness of a given weights array
# this is the version for the turbine decay values -- it compares to turbine decay
# INPUTS:
#   w: input weights
# OUTPUT:
#   fitness value
def fitness_turbine(w):
    # iterate through 1000 random data points, calculating error
    sumSqErr = 0
    for idx in range(1000):
        randIdx = random.randrange(dataPoints)
        x = inputs.iloc[randIdx].to_list()
        # calculate the estimate and grab the actual
        est = estimate(x, w)
        actual = turbineDecay.iat[randIdx, 0]
        # calculate error and square it, add it to the sumSqErr
        err = (actual - est) / actual
        sumSqErr += (err**2)

    # Return the negative of the sumSqErr so that the bees algorithm package
    # runs this as a minimization problem
    return -sumSqErr

# calculate the fitness of a given weights array
# this is the version for the compressor decay values -- it compares to compressor decay
# INPUTS:
#   w: input weights
# OUTPUT:
#   decimal fitness value, negative to represent the minimization of error
def fitness_compressor(w):
    # iterate through 1000 random data points, calculating error
    sumSqErr = 0
    for idx in range(1000):
        randIdx = random.randrange(dataPoints)
        x = inputs.iloc[randIdx].to_list()
        # calculate the estimate and grab the actual
        est = estimate(x, w)
        actual = compressorDecay.iat[randIdx, 0]
        # calculate error and square it, add it to the sumSqErr
        err = (actual - est) / actual
        sumSqErr += (err**2)

    # Return the negative of the sumSqErr so that the bees algorithm package
    # runs this as a minimization problem
    return -sumSqErr

search_boundaries=([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

turbineAlg = BeesAlgorithm(fitness_turbine,search_boundaries[0],search_boundaries[1],ns=scouts,nb=14,ne=1,nrb=5,nre=30,stlim=10,shrink_factor=0.2)
compressorAlg = BeesAlgorithm(fitness_compressor,search_boundaries[0],search_boundaries[1],ns=scouts,nb=14,ne=1,nrb=5,nre=30,stlim=10,shrink_factor=0.2)

# Establish a loop so that the user can run the algorithm as many times as they like
# while True:
#     userInput = input("Press Enter to continue or Q then enter to quit...")
#     if(userInput == 'q'):
#         break
#     turbineAlg.performSingleStep()
#     compressorAlg.performSingleStep()
#     bestTurbine = turbineAlg.best_solution
#     bestCompressor = compressorAlg.best_solution

#     print("Turbine Best: " + str(bestTurbine.score))
#     print(bestTurbine.values)
#     print("Compressor Best: " + str(bestCompressor.score))
#     print(bestCompressor.values)

turbBestArr = []
compBestArr = []

for idx in range(iterations):
    turbineAlg.performSingleStep()
    compressorAlg.performSingleStep()
    bestTurbine = turbineAlg.best_solution
    bestCompressor = compressorAlg.best_solution

    turbBestArr.append(bestTurbine.score)
    compBestArr.append(bestCompressor.score)
    print(idx)

print(estimate(inputs.iloc[0].to_list(), turbineAlg.best_solution.values))
print(estimate(inputs.iloc[0].to_list(), compressorAlg.best_solution.values))

plt.figure(1)
plt.plot(range(iterations), turbBestArr, label = "Turbine Decay Fitness") 
    
# plotting the line 2 points  
plt.plot(range(iterations), compBestArr, label = "Compressor Decay Fitness")

plt.xlabel('Cycle')
plt.ylabel('Fitness Value')
plt.title('Fitness Value Comparison')

# show a legend on the plot 
plt.legend()

plt.show()

plt.figure(2)
plt.plot(range(int(iterations / 2), iterations), turbBestArr[(int(iterations / 2)):], label = "Turbine Decay Fitness") 
    
# plotting the line 2 points  
plt.plot(range(int(iterations / 2), iterations), compBestArr[int(iterations / 2):], label = "Compressor Decay Fitness")

plt.xlabel('Cycle')
plt.ylabel('Fitness Value')
plt.title('Second Half Fitness Value Comparison')

# show a legend on the plot 
plt.legend() 

# function to show the plot 
plt.show()