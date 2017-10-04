import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
from PolygonInteracter import PolygonInteractor

fig = plt.figure()
dataSubplot = fig.add_subplot(2,2,1)
dataSubplot.set_ylabel("G_z [mGals]")
modelSubplot = fig.add_subplot(2,2,3,sharex=dataSubplot)
modelSubplot.invert_yaxis()
modelSubplot.set_ylabel("Depth [m]")
modelSubplot.set_xlabel("x distance [m]")
# p = newPoly()

#theta = np.arange(0, 2*np.pi, 2.0)
#r = 0.2
#xs = r*np.cos(theta)+0.25
#zs = r*np.sin(theta)+0.25
xs = [2.,3.,3.,2.]
zs = [3.,3.,4.,4.]
poly = patches.Polygon(list(zip(xs, zs)), animated=True)
modelSubplot.add_patch(poly)

density = 1
xplot = np.linspace(0,10,101)
nplot = len(xplot)
obs = np.zeros((nplot,2))
obs[:,0] = xplot
xdata = np.linspace(0,10,11)
gravdata = [0.000, 0.001, 0.002, 0.003, 0.0035, 0.004, 0.0035, 0.003, 0.002, 0.001, 0.000]
ndata = len(gravdata)
data = np.zeros((ndata,2))
data[:,0] = xdata
data[:,1] = gravdata
error = np.ones(ndata)*0.0005
modxmin = min(xs)
modxmax = max(xs)
modzmin = min(zs)
modzmax = max(zs)

# p = PolygonInteractor(modelSubplot, dataSubplot, poly, density, obs, data, error)
p = PolygonInteractor(modelSubplot, dataSubplot, poly, density, obs)

# buttons
# load data
def loadData(self):
    5
    p.update_data(data,error)
ax0=plt.axes([.55,.85,.175,.1])
loadDataButton=Button(ax0,'Load Data')
loadDataButton.on_clicked(loadData)
# load model
def loadModel(self):
    5
ax1=plt.axes([.775,.85,.175,.1])
loadModelButton=Button(ax1,'Load Model')
loadModelButton.on_clicked(loadModel)
# new model
def newPoly(self):
    5
ax2=plt.axes([.55,.7,.175,.1])
newModelButton=Button(ax2,'New Model')
newModelButton.on_clicked(newPoly)
# save model
def saveModel(self):
    5
ax3=plt.axes([.775,.7,.175,.1])
saveModelButton=Button(ax3,'Save Model')
saveModelButton.on_clicked(saveModel)
# density value
def updateDensity(val):
    p.update_density(val)
fig.text(.55,.6,'Density value (g/cm^3)',fontsize=14, transform=fig.transFigure)
ax4=plt.axes([.55,.48,.38,.1])
densSlider = Slider(ax4,'',-3,3,valinit=0)
densSlider.set_val(density)
densSlider.on_changed(updateDensity)


def updateDepth(val):
    maxDepth = 10**val
    # p.update_depth(val)
fig.text(.55,.41,'Depth value (log scale exponent)',fontsize=14, transform=fig.transFigure)
ax5=plt.axes([.55,.29,.38,.1])
depthSlider = Slider(ax5,'',0,4,valinit=1)
depthSlider.set_val(1)
depthSlider.on_changed(updateDepth)

def updateXAxis(val):
    xbuffer = 10**val
    # p.update_xaxis(val)
fig.text(.55,.22,'x-axis buffer (log scale exponent)',fontsize=14, transform=fig.transFigure)
ax6=plt.axes([.55,.10,.38,.1])
xaxisSlider = Slider(ax6,'',0,4,valinit=1)
xaxisSlider.set_val(1)
xaxisSlider.on_changed(updateDepth)

plt.show()
