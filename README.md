# DataProcessingAndPlotting
Takes energy surfaces and finds equilibrium geometry

The user specifies a path in the console, which is a folder containing the Gaussian output files.
The program produces a plot of the energy surface and:
  - The equilibrium bond length
  - The polynomial coefficients used to find k_r
  - The equilibrium bond angle
  - The polynomial coefficients used to find k_theta
  - The normal mode frequencies in Hz and cm^-1

The program Ex2.py uses trisurf to plot the data, as this method seemed to be much less constrained in requirements on the input.
I effectively used it like a filled in scatter plot. This is the program that calculates all of the above.
Surface.py just demonstrates the manipulation required to get the data to work with a surface plot.

The biggest issue with the program is that it naively takes the minimum value of r and theta in the data and uses that
as the assumed equilibrium bond length and angle. This could be improved by finding a 2d polynomial for the data and finding
the minimum of that. I think this makes it more complicated to find the values of k_r and k_theta though.
