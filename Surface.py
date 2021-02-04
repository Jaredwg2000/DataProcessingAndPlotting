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

# Making the x/y inputs for plot_surface
Rs, Thetas = meshgrid(R, Theta)

Energy = ndarray((len(Theta), len(R)))

tempr = 0.0
temptheta = 0.0
tempE = 0.0

# Sort the energy values into an array to plot using plot_surface
for i, j in enumerate(E):
    Energy[i % len(Theta), math.floor(i / len(Theta))] = j
    if(j < tempE):
        tempE = j
        tempr = R[math.floor(i / len(Theta))]
        temptheta = Theta[i % len(Theta)]

temprIndex = R.index(tempr)
tempthetaIndex = Theta.index(temptheta)

scaledEnergy = Energy*4.356*pow(10, -18)
R = [i * pow(10, -10) for i in R]
Theta = [i * pi/180 for i in Theta]

polyfitlistThetas = []

for i in range(temprIndex - 2, temprIndex + 3):
    fitx = []
    fity = []
    for j in range(tempthetaIndex - 2, tempthetaIndex + 3):
        fitx.append(Theta[j])
        fity.append(scaledEnergy[j, i])
    polyfitlistThetas.append(polyfit(fitx, fity, 2))

polyfitlistRs = []

# ^ this works
# v numbers are close

for i in linspace(Theta[tempthetaIndex-2], Theta[tempthetaIndex+2], 41):
    fitx = []
    fity = []
    for j, p in enumerate(polyfitlistThetas):
        fitx.append(R[temprIndex - 2 + j])
        fity.append(p[0]*i**2 + p[1]*i + p[2])
    polyfitlistRs.append(polyfit(fitx, fity, 2))

# find value of r corresponding to minimum i.e. -p[1]/2p[0]
eqbmE = 0
eqbmR = 0
tempR = []
tempE = []

for i, f in enumerate(polyfitlistRs):
    tempR.append(-f[1] / (2*f[0]))
    tempE.append(f[0]*tempR[i]**2 + f[1]*tempR[i] + f[2])

tempEIndex = tempE.index(min(tempE))
eqbmR = tempR[tempEIndex]
print(eqbmR)

eqbmTheta = Theta[tempthetaIndex-2]
eqbmTheta += tempEIndex*(Theta[tempthetaIndex+2] - Theta[tempthetaIndex-2])/40
eqbmTheta *= 180/pi
print(eqbmTheta)

# Plot the data using plot_surface
fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_surface(Rs, Thetas, Energy, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_xlabel("r/Å")
ax.set_ylabel("θ/degrees")
ax.set_zlabel("E/hartree")
ax.set_title("Energy surface for " + molecule)









plt.show()
