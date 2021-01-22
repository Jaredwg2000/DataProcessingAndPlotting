"""Program to calculate energy surfaces.

Takes a folder path as input, extracts the data
from the files in the folder, then produces an energy
surface, and calculates the normal mode frequencies.
"""

from numpy import *
import matplotlib.pyplot as plt
import os
# from mpl_toolkits import mplot3d

# Take the path from input into the console
path = input()

# Initialize vairables
r = []
theta = []
E = []
tempr = 0.0
temptheta = 0.0
tempE = 0.0
molecule = ""

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

    r.append(tempr)
    theta.append(temptheta)
    E.append(tempE)

fig = plt.figure()

# Plotting the energy surface in degrees, angstrom and hartree, as it looks
# nicest and the plotting function doesn't seem to like very small values of r
ax = plt.axes(projection='3d')
trisurf = ax.plot_trisurf(r, theta, E, cmap='hsv', edgecolor='none',
                          norm=plt.Normalize(min(E)-0.06, min(E) + 0.5))

# Converting to SI units
r = [i * pow(10, -10) for i in r]
E = [i * 4.356*pow(10, -18) for i in E]
theta = [i * pi/180 for i in theta]

# Find the minimum energy geometry
minEIndex = E.index(min(E))
minr = r[minEIndex]
mintheta = theta[minEIndex]

# More variables, for the polynomial fits.
xr = []
xtheta = []
yr = []
ytheta = []

# Take the points closest to the energy minimum in each direction for use
# in the fit
for i in range(len(E)):
    if(r[i] == minr):
        if(abs(theta[i]-mintheta) <= pi/45):
            xtheta.append(theta[i])
            ytheta.append(E[i])
    if(theta[i] == mintheta):
        if(abs(r[i]-minr) <= 3 * pow(10, -11)):
            xr.append(r[i])
            yr.append(E[i])

# Do the fits
pr = polyfit(xr, yr, 2)
ptheta = polyfit(xtheta, ytheta, 2)

# Output the polynomial fits, mostly as a sanity check
print("Polynomial fit to find k_r at θ = " + str(mintheta * 180/pi) + "°")
print(pr)
print("Polynomial fit to find k_θ at r = " + str(minr * pow(10, 10)) + " Å")
print(ptheta)

# Calculate the frequency in Hz and cm^-1 via k
kr = 2.0*pr[0]
ktheta = 2.0*ptheta[0]

vr = (1/(2*pi))*sqrt(kr/(2*1.66*pow(10, -27)))
vtheta = (1/(2*pi))*sqrt(ktheta/(pow(minr, 2)*0.5*1.66*pow(10, -27)))

vbarr = vr * (3.3356 * pow(10, -11))
vbartheta = vtheta * (3.3356 * pow(10, -11))


# Output the answers for the user
print("From the polynomial fit, ν_r = " + str(vr) + " Hz; or " + str(vbarr)
      + " cm^-1")
print("From the polynomial fit, ν_θ = " + str(vtheta) + " Hz; or "
      + str(vbartheta) + " cm^-1")


# Lebels for the graph
ax.set_xlabel("r/Å")
ax.set_ylabel("θ/degrees")
ax.set_zlabel("E/hartree")
ax.set_title("Energy surface for " + molecule)

# Put a point on the graph at the minimum energy
ax.scatter(minr*pow(10, 10), mintheta * 180/pi, min(E)/(4.356*pow(10, -18)),
           s=25, facecolor="black")

plt.show()
