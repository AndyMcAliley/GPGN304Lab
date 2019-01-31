"""
Edited January 31, 2019
Edits made by Brett Bernstein

1. matplotlib.axes_grid.anchored_artists is deprecated. Changed to matplotlib.offsetbox for importing AnchoredText
2. Implemented dist_point_to_segment function, import is deprecated
3. Removed the damn line. In the compute_grav() function, grav was being plotted not only as a function of the self.preloc
   x values (which we want), but also as a function of the self.preloc y values. Sliced self.preloc in the plot function so 
   only the first column, the x values, are used.
"""



"""
This is an example to show how to build cross-GUI applications using
matplotlib event handling to interact with objects on the canvas

http://matplotlib.org/2.0.0/examples/event_handling/poly_editor.html
"""
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
#from matplotlib.mlab import dist_point_to_segment 
from matplotlib.offsetbox import AnchoredText # https://github.com/ioam/holoviews/commit/0a8974ab1dcd88cf0900059c7148a943d4dccb01
from gpoly import gpoly

########## NEW ##########
def dist_point_to_segment(P,S0,S1):
    """
    The original function from matplotlib.mlab is deprecated, to be removed.
    matplotlib docs linked algorithm: http://geomalgorithms.com/a02-_lines.html
    """
    d = lambda u,v: np.linalg.norm(u-v)
    v = S1 - S0
    w = P - S0
    print("hi")
    c1 = np.dot(w,v)
    if c1 <= 0:
         return d(P, S0)
    
    c2 = np.dot(v,v)
    if c2 <= c1:
         return d(P, S1)

    b = c1 / c2;
    Pb = S0 + b * v
    return d(P, Pb)

class PolygonInteractor(object):
    """
    An polygon editor.

    Key-bindings

      't' toggle vertex markers on and off.  When vertex markers are on,
          you can move them, delete them

      'd' delete the vertex under point

      'i' insert a vertex at point.  You must be within epsilon of the
          line connecting two existing vertices

    """

    showverts = True
    epsilon = 5  # max pixel distance to count as a vertex hit

    def __init__(self, model_ax, data_ax, poly, density=1, preloc=[], data=[], error=[]):
        if poly.figure is None:
            raise RuntimeError('You must first add the polygon to a figure or canvas before defining the interactor')
        self.ax = model_ax
        self.dax = data_ax
        self.density = density
        self.preloc = preloc
        self.opreloc = preloc
        self.data = data
        self.error = error
        canvas = poly.figure.canvas
        self.poly = poly
        at = AnchoredText(r'$\Delta\rho = $' + "%.2f"%(self.density),
                  prop=dict(size=12), frameon=True,
                  loc=1,
                  )
        self.at = at
        self.dax.add_artist(at)
        
        x, y = zip(*self.poly.xy)
        self.line = Line2D(x, y, marker='o', markerfacecolor='r', animated=True)
        self.ax.add_line(self.line)
        #self._update_line(poly)

        cid = self.poly.add_callback(self.poly_changed)
        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas
        self.compute_grav()
        # self.ax.autoscale()
        if min(y)>0:
            self.ax.set_ylim(top=0)

    def reset_poly(self, poly, density=1):
        self.density = density
        
        self.poly.xy = poly.xy
        x, y = zip(*self.poly.xy)
        self.line = Line2D(x, y, marker="o", markerfacecolor='r', animated=True)
        self.ax.add_line(self.line)
        self.ax.autoscale(axis='y')
        self.compute_grav()


    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def poly_changed(self, poly):
        'this method is called whenever the polygon object is called'
        # only copy the artist props to the line (except visibility)
        vis = self.line.get_visible()
        Artist.update_from(self.line, poly)
        self.line.set_visible(vis)  # don't use the poly visibility state

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
        xy = np.asarray(self.poly.xy)
        xyt = self.poly.get_transform().transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]

        if d[ind] >= self.epsilon:
            ind = None
        #print(ind)
        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None
        self.compute_grav()


    def key_press_callback(self, event):
        'whenever a key is pressed'
        if not event.inaxes:
            return
        if event.key == 't':
            self.showverts = not self.showverts
            self.line.set_visible(self.showverts)
            if not self.showverts:
                self._ind = None
        elif event.key == 'd':
            ind = self.get_ind_under_point(event)
            if ind is not None:
                self.poly.xy = [tup for i, tup in enumerate(self.poly.xy) if i != ind]
                self.line.set_data(zip(*self.poly.xy))
        elif event.key == 'i':
            xys = self.poly.get_transform().transform(self.poly.xy)
            p = event.x, event.y  # display coords
            for i in range(len(xys) - 1):
                s0 = xys[i]
                s1 = xys[i + 1]
                d = dist_point_to_segment(p, s0, s1)
                if d <= self.epsilon:
                    self.poly.xy = np.array(
                        list(self.poly.xy[:i+1]) +
                        [(event.xdata, event.ydata)] +
                        list(self.poly.xy[i+1:]))
                    self.line.set_data(zip(*self.poly.xy))
                    break

        self.canvas.draw()
        self.compute_grav()

    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata

        self.poly.xy[self._ind] = x, y
        if self._ind == 0:
            self.poly.xy[-1] = x, y
        elif self._ind == len(self.poly.xy) - 1:
            self.poly.xy[0] = x, y
        self.line.set_data(zip(*self.poly.xy))

        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def compute_grav(self):
        grav = gpoly(self.preloc,self.poly.xy,self.density)
        self.dax.lines = []
        self.dax.text = []
        self.at.remove()
        #print(self.preloc[0:,1].shape, grav.shape)
        #self.dax.plot(self.preloc.T[0],grav,'g-')
        ### self.preloc is a (101,2) array, 101 rows by 2 colums. We want just the first column: the x values.
        self.dax.plot(self.preloc[:,0:1],grav,'g-')
        
        at = AnchoredText(r'$\Delta\rho = $' + "%.2f"%(self.density),
                  prop=dict(size=12), frameon=True,
                  loc=1,
                  )
        self.at = at
        self.dax.add_artist(at)


        if self.data != []:
            if self.error != []:
                self.dax.errorbar(self.data[:,0],self.data[:,1], yerr=self.error,fmt='b-')
            else:
                self.dax.plot(self.preloc,self.data,'g-')
            sf = 0.1*max(abs(max(self.data[:,1])), abs(min(self.data[:,1])))
            #print(sf)
            ymin = min(self.data[:,1]) - sf
            ymax = max(self.data[:,1]) + sf
            self.dax.set_ylim((ymin,ymax))
            
        self.canvas.draw()
        

    def update_data(self,data=[],error=[]):
        #self.preloc = preloc
        self.data = data
        self.error = error
        self.compute_grav()
        
    def update_preloc(self,preloc):
        self.preloc = preloc
        self.compute_grav()

    def update_density(self,density):
        self.density = density
        self.compute_grav()



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    theta = np.arange(0, 2*np.pi, 1.0)
    r = 1.5

    xs = r*np.cos(theta)
    ys = r*np.sin(theta)

    poly = Polygon(list(zip(xs, ys)), animated=True)

    fig, ax = plt.subplots()
    ax.add_patch(poly)
    p = PolygonInteractor(ax, poly)

    #ax.add_line(p.line)
    ax.set_title('Click and drag a point to move it')
    ax.set_xlim((-2, 2))
    ax.set_ylim((-2, 2))
    plt.show()
