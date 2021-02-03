""" Program to calculate energy surfaces.

Takes a folder path as input, extracts the data
from the files in the folder, then produces an energy
surface, and calculates the normal mode frequencies.
"""
from numpy import *
import matplotlib.pyplot as plt
import os
import math
from matplotlib import cm
# from mpl_toolkits import mplot3d

# Take the path from input into the console
print("Path: ")
path = input()

# Initialize vairables
r = []
theta = []
E = []
tempr = 0.0
temptheta = 0.0
tempE = 0.0
molecule = ""

Inputs = []

# Get a list of the files in the path given
files = os.listdir(path)

# Read through the files, extract the data
for file in files:
    f = open(path + "\\" + file, "r")

    for line in f:
        linesplit = line.split()

        # Extract the angle and bond length
        if(len(linesplit) == 5):
            if(linesplit[0] == "H" and linesplit[1] == "1"):
                tempr = float(linesplit[2])
                temptheta = float(linesplit[4])

        # Extract the energy
        if "A.U. after" in line:
            tempE = float(linesplit[4])

        # Extract the name of the molecule for the title of the plot
        if "Stoichiometry" in line:
            molecule = linesplit[1]

    f.close()

    # Adding the inputs to a list of tuples to sort them
    Inputs.append((tempr, temptheta, tempE))

Inputs.sort()

# Goes from list of tuples to multiple lists
r, theta, E = map(list, zip(*Inputs))

R = []
Theta = []

# Extract the *different* inputs for r and theta
for i in r:
    if(i not in R):
        R.append(i)
for i in theta:
    if(i not in Theta):
        Theta.append(i)

Energy = ndarray((len(Theta), len(R)))

# Sort the energy values into an array to plot using plot_surface
for i, j in enumerate(E):
    Energy[i % len(Theta), math.floor(i / len(Theta))] = j

# Making the x/y inputs for plot_surface
R, Theta = meshgrid(R, Theta)

# Plot the data using plot_surface
fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(R, Theta, Energy, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel("r/Å")
ax.set_ylabel("θ/degrees")
ax.set_zlabel("E/hartree")
ax.set_title("Energy surface for " + molecule)
ax.set_xlim(r[0], r[-1])
ax.set_ylim(theta[0], theta[-1])

plt.show()
