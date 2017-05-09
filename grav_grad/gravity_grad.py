# import libraries
import numpy as np
import matplotlib.pyplot as plt

# constants
gamma = 6.67408e-11 # [m^3 kg^-1 s^-2]
conv  = 100000. # [m/s^2] to [mGal]

# setup grid parameters [m]
xstart = -500.
xend   =  500.
xstep  =  10.

ystart = -500.
yend   =  500.
ystep  =   10.

# target parameters
mass = 10000. # mass [kg]

# location. Right hand coordinate system. [m]
xp   =   0.
yp   =   0.
zp   =   200.

# make the grid
x = np.arange(xstart, xend+xstep, xstep)
y = np.arange(ystart, yend+ystep, ystep)
z = 0.

# helpful parameters
nx = len(x)
ny = len(y)

xv, yv = np.meshgrid(x, y)

# vectorized notation
Rdist = np.sqrt((xp-xv)**2 + (yp-yv)**2 + (zp-z)**2)

Gv = conv*gamma*mass*(zp-z)/(Rdist**3)

Gxz = 3*conv*gamma*mass*(xp-xv)*(zp-z ) / (Rdist**5)
Gxy = 3*conv*gamma*mass*(xp-xv)*(yp-yv) / (Rdist**5)
Gyz = 3*conv*gamma*mass*(yp-yv)*(zp-z ) / (Rdist**5)

Gxx = 3*conv*gamma*mass*( (xp-xv)**2/(Rdist**5) - 1./Rdist**3)
Gyy = 3*conv*gamma*mass*( (yp-yv)**2/(Rdist**5) - 1./Rdist**3)
Gzz = 3*conv*gamma*mass*( (zp-z )**2/(Rdist**5) - 1./Rdist**3)

# PLOTTING

f, axarr = plt.subplots(3,3, sharex=True, sharey=True)
cmap = plt.get_cmap('jet')
f.delaxes(axarr[1,0])
f.delaxes(axarr[2,1])
substr = '%.0f kg at (%.0f, %.0f, %.0f)m'%(mass,xp,yp,zp)
f.suptitle('Gravity Gradient of a Point Source [Eotvos]\n'+substr)

# Plot Gxx
p = axarr[0,0]
im = p.pcolor(yv,xv,Gxx, cmap=cmap)
p.set_ylabel('y [m]')
p.set_xlabel('x [m]')
p.set_title('Gxx')
f.colorbar(im, ax=p).set_label('[Eotvos]')

# Plot Gxy
p = axarr[0,1]
im = p.pcolor(yv,xv,Gxy, cmap=cmap)
p.set_title('Gxy')
f.colorbar(im, ax=p).set_label('[Eotvos]')

# Plot Gxz
p = axarr[0,2]
im = p.pcolor(yv,xv,Gxz, cmap=cmap)
p.set_title('Gxz')
f.colorbar(im, ax=p).set_label('[Eotvos]')

# Plot Gyy
p = axarr[1,1]
im = p.pcolor(yv,xv,Gyy, cmap=cmap)
p.set_title('Gyy')
p.set_ylabel('y [m]')
p.set_xlabel('x [m]')
f.colorbar(im, ax=p).set_label('[Eotvos]')

# Plot Gyz
p = axarr[1,2]
im = p.pcolor(yv,xv,Gyz, cmap=cmap)
p.set_title('Gyz')
f.colorbar(im, ax=p).set_label('[Eotvos]')

# Plot G
p = axarr[2,0]
im = p.pcolor(yv,xv,Gv, cmap=cmap)
p.set_ylabel('y [m]')
p.set_xlabel('x [m]')
p.set_title('G')
f.colorbar(im, ax=p).set_label('[mGal]')

# Plot Gzz
p = axarr[2,2]
im = p.pcolor(yv,xv,Gzz, cmap=cmap)
p.set_ylabel('y [m]')
p.set_xlabel('x [m]')
p.set_title('Gzz')
f.colorbar(im, ax=p).set_label('[Eotvos]')

plt.show()
