# import libraries
import numpy as np
import matplotlib.pyplot as plt

# constants
mu0 = 4*np.pi*1e-7 # []

# setup grid parameters [m]
xstart = -775
xend   =  800
xstep  =  10 

ystart = -775
yend   =  800
ystep  =   25

# target parameters
a = 200 # target radius [m]
k = 0.05 # target susceptibility

# location. Right hand coordinate system. [m]
xp   =   200 # NORTHING
yp   =   0   # EASTING
zp   =   250

# Inducing field strength
B0  = 50000 # nano Tesla
inc = 45    # degrees
dec = 25    # degrees

# Convert degrees to radians
inc = np.deg2rad(inc)
dec = np.deg2rad(dec)

B = B0*np.array([np.cos(inc)*np.cos(dec), 
                 np.cos(inc)*np.sin(dec),
                 np.sin(inc)])

Bhat = B/np.linalg.norm(B) # Sanity check: Denom = B0

# Magnetization
M = k*B/mu0

# make the grid
x = np.arange(xstart, xend+xstep, xstep)
y = np.arange(ystart, yend+ystep, ystep)
z = 0

xv, yv = np.meshgrid(x, y)

# Calculate the Tensor
# vectorized notation
Rdist = np.sqrt((xp-xv)**2 + (yp-yv)**2 + (zp-z)**2)

Txx = 3*(xp-xv)**2/(Rdist**5) - 1/Rdist**3
Tyy = 3*(yp-yv)**2/(Rdist**5) - 1/Rdist**3
Tzz = 3*(zp-z )**2/(Rdist**5) - 1/Rdist**3

Txy = 3*(xp-xv)*(yp-yv)/Rdist**5
Txz = 3*(xp-xv)*(zp-z )/Rdist**5
Tyz = 3*(yp-yv)*(zp-z )/Rdist**5

T = np.array([[Txx, Txy, Txz],
              [Txy, Tyy, Tyz],
              [Txz, Tyz, Tzz]])

# Calculate the magnetic anomaly
# Transpose to get axes of T to match axes of M for multiplication
Ba = mu0*a**3/3 * np.dot(M, T.transpose())

# Calculate total field anomaly
# Transpose to match the meshgrid
dT = np.dot(Ba, Bhat).transpose()

# PLOTTING
substr = 'radius=%.0f m k=%.0f at (%.0f, %.0f, %.0f)m'%(a,k,xp,yp,zp)
cmap = plt.get_cmap('jet')

plt.figure()
plt.pcolor(yv,xv,dT, cmap=cmap)
plt.colorbar().set_label('[nT]')
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')
plt.title(' Total Magnetic Field Anomaly [nT]\n'+substr)



plt.show()
