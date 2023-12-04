# Smith and Javorsky Supplemental Materials

This repository contains materials utilized by Smith and Javorsky to supplement the paper and presentation "Condition-Based Maintenance of a Naval Gas Turbine Propulsion Plant Using The Bees Algorithm" prepared for Dr. Shahram Rahimi's "Machine Learning and Soft Computing" class at Mississippi State University.

## File Descriptions

Execution Graphs - png format images of the graphs of the executions used in the paper, including runs of 0, 10, and 100 scouts for 100 iterations.

beeTest.py - a python file to test that the bees algorithm worked as expected before allowing it to run for all of the desired iterations.

beeWithGraph.py - a python file to run the bees algorithm for a given number of iterations with any number of scout bees. This produces the plots used in the paper.

condition+based+maintenance+of+naval+propulsion+plants.zip - a zip file containing the dataset as it was downloaded from the source.

data.csv - the data file from the source that is necessary for execution.

FinalPresentation.mp4 - the recording submitted of our presentation.

README.md - this document.

## Running the Files

To run beeTest.py or beeWithGraph.py, ensure that all dependencies are installed:

- main packages: python3; pip
- pip packages: bees_algorithm; pandas

### beeTest.py

To run this file, use a command-line terminal in the supplemental materials directory to enter:

python beeTest.py

OR

python3 beeTest.py

depending on how python is installed on your system.

Then, wait for text to prompt you for input. Press "enter" to run one cycle of the bees algorithm and prove that all dependencies are installed and it works. Press "q" then "enter" to submit the input "q" and signal to quit the (infinite loop) program.

### beeWithGraph.py

Before running this file, first check that the parameters at the top of the file are set as you wish. They should default to 10 iterations and 10 scouts. Increasing iterations will make the execution take longer but may result in a more useful graph. Increasing the number of scouts will increase the speed of finding a maximum.

To run this file, run the same as beeTest.py:

python beeWithGraph.py

OR

python3 beeWithGraph.py

depending on how python is installed on your system.

Then, each iteration should print its graph index number to the command line to signal that it has completed. This might take a significant amount of time. As reported in the paper, 100 iterations on a recent MacBook Pro took an entire 7 minutes.
