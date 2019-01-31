# import libraries
import numpy as np
import matplotlib.pyplot as plt

# constants
gamma = 6.67408e-11 # [m^3 kg^-1 s^-2]
conv  = 100000 # [m/s^2] to [mGal]

# setup grid parameters [m]
xstart = -500
xend   =  500
xstep  =   25

ystart = -500
yend   =  500
ystep  =  10 

# target parameters
mass = 1000 # mass [kg]

# location. Right hand coordinate system. [m]
xp   =   0 # NORTHING
yp   =   250   # EASTING
zp   =   100


# make the grid
x = np.arange(xstart, xend+xstep, xstep) # NORTHING
y = np.arange(ystart, yend+ystep, ystep) # EASTING
z = 0

# helpful parameters
nx = len(x)
ny = len(y)

xv, yv = np.meshgrid(x, y)

# vectorized notation (PREFERRED)
Rdist = np.sqrt((xp-xv)**2 + (yp-yv)**2 + (zp-z)**2)
Gv = conv*gamma*mass*(zp-z)/Rdist**3

# index notation (ACCEPTABLE)
Gi = np.zeros([ny,nx])
for ix in range(nx):
    for iy in range(ny):
        Gi[iy,ix] = conv*gamma*mass*(zp-z)/((xp-x[ix])**2 
                                          + (yp-y[iy])**2 
                                          + (zp-z    )**2)**(3./2.)


# PLOTTING
substr = '%.0f kg at (%.0f, %.0f, %.0f)m'%(mass,xp,yp,zp)
cmap = plt.get_cmap('jet')

plt.figure()
plt.pcolor(yv,xv,Gv, cmap=cmap)
plt.colorbar().set_label('[mGal]')
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')
plt.title('Gravity Response of a Point Source [mGal]\n'+substr)

# Transpose Gi to get on same grid as x and y
plt.figure()
plt.pcolor(y,x,Gi.transpose(), cmap=cmap)
plt.colorbar().set_label('[mGal]')
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')
plt.title('Gravity Response of a Point Source [mGal]\n'+substr)


plt.show()
