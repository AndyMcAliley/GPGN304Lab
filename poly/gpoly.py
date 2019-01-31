# compute gravity response of a polygon
# Andy McAliley, 9/16/2017
import numpy as np
from builtins import range

def gpoly(obs,nodes,density):
    #Blakely, 1996
    gamma = 6.672E-03;
    numobs = len(obs)
    numnodes = len(nodes)
    grav = np.zeros(numobs)
    for iobs in range(numobs):
        shiftNodes = nodes - obs[iobs]
        su = 0
        for i1 in range(numnodes):
            i2 = i1+1
            # last node must wrap around to first node
            i2 = np.mod(i2,numnodes)
            x1 = shiftNodes[i1,0]
            x2 = shiftNodes[i2,0]
            z1 = shiftNodes[i1,1]
            z2 = shiftNodes[i2,1]

            dx = x2 - x1
            dz = z2 - z1
            # avoid zero division
            if abs(dz) < 1E-8:
                # move on if points are identical
                if abs(dx) < 1E-8:
                    continue
                dz = dz - dx*(1E-7)
            alpha = dx/dz
            beta = x1-alpha*z1
            r1 = np.sqrt(x1**2+z1**2)
            r2 = np.sqrt(x2**2+z2**2)
            theta1 = np.arctan2(z1,x1)
            theta2 = np.arctan2(z2,x2)

            term1 = np.log(r2/r1)
            term2 = alpha*(theta2-theta1)
            factor = beta/(1+alpha**2)
            su = su + factor*(term1-term2)
        grav[iobs] = 2*gamma*density*su
    return grav

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    xmin = 0.
    xmax = 10.
    nx = 201

    obs = np.zeros((nx,2))
    obs[:,0] = np.linspace(xmin,xmax,nx)

    nodes = np.zeros((4,2))
    nodes[0] = [2.,1.5]
    nodes[1] = [3.,1.5]
    nodes[2] = [3.,2.5]
    nodes[3] = [2.,2.5]

    density = 1

    grav = gpoly(obs,nodes,density)

    plt.plot(obs[:,0],grav)
    plt.show()
