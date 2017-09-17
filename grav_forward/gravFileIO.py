import numpy as np
from gpoly import gpoly
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from builtins import range

def ReadInpFile(filename):
    # Require Input file "poly.inp" in the following format:
    #-------------------------------------------------------
    # title            <---- Title/Name of the model
    # plot.ps          <---- Output file name for the plot
    # xmin xmax delx   <---- end and interval of profile
    # npoly            <---- # of polygons
    #
    # nc1 rho1         <---- # of vertices and density
    # xc(1) zc(1)      <---- vertices ordered clockwise (IMPORTANT)
    # xc(2) zc(2)
    # ...
    # xc(nc) zc(nc)
    #
    # nc2 rho2
    # xc(1) zc(1)
    # xc(2) zc(2)
    # ...
    # xc(nc2) zc(nc2)
    #
    # ....
    #--------------------------------------------------------
    #
    # Author: Andy McAliley
    # Date:   9/16/2017
    # Adapted from poly.m by Yaoguo Li
    # Written for the GPGN304 lab
    f = open(filename,'r')
    lines=f.read().splitlines()
    f.close()

    # parse header info
    title = lines[0]
    # output file name is unused
    outfile = lines[1]
    [xmin, xmax, xstep] = [float(i) for i in lines[2].split()]
    nobs = int((xmax-xmin)/xstep)+1
    xobs = np.linspace(xmin,xmax,nobs)
    obs = np.zeros((nobs,2))
    obs[:,0] = xobs
    npoly = int(lines[3])

    # prepare figure
    fig = plt.figure()
    axData = fig.add_subplot(2,1,1)
    axModel = fig.add_subplot(2,1,2,sharex=axData)
    axModel.invert_yaxis()

    # read polygon corners and plot
    grav = np.zeros(nobs)
    nextLine = 4
    for ipoly in range(npoly):
        headerNums = lines[nextLine].split()
        nextLine = nextLine + 1
        nc = int(headerNums[0])
        density = float(headerNums[1])
        nodes = np.zeros((nc,2))
        for ic in range(nc):
            nodes[ic] = [float(i) for i in lines[nextLine].split()]
            nextLine = nextLine + 1
        # compute gravity anomaly for this polygon
        grav = grav + gpoly(obs,nodes,density)
        # plot polygon
        polygon = patches.Polygon(list(zip(nodes[:,0],nodes[:,1])))
        axModel.add_patch(polygon)
    # reset model axes limits
    axModel.use_sticky_edges = False
    axModel.set_ymargin(0.1)
    axModel.autoscale()
    # plot data and show figure
    axData.plot(xobs,grav)
    fig.show()

