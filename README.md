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
as the assumed equilibrium bond length and angle.

To code this, one would have to do a fit in one direction (e.g. r) then use those fits in the other direction (i.e. theta) to get a 
new set of values with finer steps between theta values. From here, the new theta values could be used to find new r values, etc.

From these new values for r and theta with corresponding E, a new minimum energy can be found and the same process can be done as
used in Ex2.py to find a more precise geometry, and therefore more precise normal mode frequencies.

04/2/21 - I implemented the interpolation by:
  - Finding 5 points in each direction surrounding the minimum calculated energy
  - Find 5 polyfits going in one axis from these points
  - Use these polyfits to find a 41 polyfits in the orthogonal axis
  - Find the minimum minimum energy from these polyfits and report the value of r and theta that gave that energy.
This ended up moving the results away from the actual values, not towards, but the code is in Surface.py.
I did not use these values to calculate new normal mode frequencies - this would require another polyfit in the
first axis.
