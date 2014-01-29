import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

class figure_with_basemap:
    def __init__(self,lonsize,latsize,interval_lon=1,interval_lat=1):
        '''
        draw the Basemap
        '''
#        super(add_figure, self).__init__()
        self.lonsize, self.latsize = lonsize, latsize
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_left_button_down)
        self.dmap = Basemap(projection='cyl',llcrnrlat=min(self.latsize)-0.01,urcrnrlat=max(self.latsize)+0.01,
                            llcrnrlon=min(self.lonsize)-0.01,urcrnrlon=max(self.lonsize)+0.01,resolution='h')
        self.dmap.drawparallels(np.arange(int(min(self.latsize)),int(max(latsize))+1,interval_lat),labels=[1,0,0,0])
        self.dmap.drawmeridians(np.arange(int(min(lonsize))-1,int(max(lonsize))+1,interval_lon),labels=[0,0,0,1])
        self.dmap.drawcoastlines()
        self.dmap.fillcontinents(color='grey')
        self.dmap.drawmapboundary()
    def on_left_button_down(self, event):
        if event.button == 1:
            x, y = event.xdata, event.ydata
            print 'You clicked: %f, %f' % (x, y)
    def getSize(self):
        return self.lonsize, self.latsize
#    def setSize(self, size):
#        self.lonsize, self.latsize = size
    def show():
        self.fig.show()
    size = property(getSize)
class water:
    def __init__(self, startpoint, url):
        self.startpoint = startpoint
        self.url = url
        self.points = []
    def get_data(self):
        data = netCDF4.Dataset(url)
        lons = data.variables['lon_rho']
    def bbox2ij(self, lons, lats, bbox):
        """Return indices for i,j that will completely cover the specified bounding box.     
        i0,i1,j0,j1 = bbox2ij(lon,lat,bbox)
        lon,lat = 2D arrays that are the target of the subset, type: np.ndarray
        bbox = list containing the bounding box: [lon_min, lon_max, lat_min, lat_max]
    
        Example
        -------  
        >>> i0,i1,j0,j1 = bbox2ij(lat_rho,lon_rho,[-71, -63., 39., 46])
        >>> h_subset = nc.variables['h'][j0:j1,i0:i1]       
        """
        bbox = np.array(bbox)
        mypath = np.array([bbox[[0,1,1,0]],bbox[[2,2,3,3]]]).T
#        print mypath
        p = path.Path(mypath)
        points = np.vstack((lons.flatten(),lats.flatten())).T   
        n,m = np.shape(lons)
#        inside = p.contains_points(points).reshape((n,m))
        inside = []
        for i in range(len(points)):
            inside.append(p.contains_point(points[i]))
        inside = np.array(inside, dtype=bool).reshape((n, m))
#        ii,jj = np.meshgrid(xrange(m),xrange(n))
#        return min(ii[inside]),max(ii[inside]),min(jj[inside]),max(jj[inside])
#        return ii[inside].min(), ii[inside].max(), jj[inside].min(), jj[inside].max()
#        return np.min(ii[inside]), np.max(ii[inside]), np.min(jj[inside]), np.max(jj[inside])
        index = np.where(inside==True)
        if not index[0].tolist():
            print 'out of range.'
            return 10000,10000,10000,10000
        else:
            return min(index[1]), max(index[1]), min(index[0]), max(index[0])
     def nearest_point_index(lon, lat, lons, lats, length=(1, 1)):
        '''
        Return the index of the nearest rho point.
        lon, lat: the coordiation of original point, float
        lats, lons: the coordiation of points want to be calculated.
        length: the boundary box.
        '''
        bbox = [lon-length[0], lon+length[0], lat-length[1], lat+length[1]]
        i0, i1, j0, j1 = bbox2ij(lons, lats, bbox)
        if i0==10000:
            return None
        else:
            lon_covered = lons[j0:j1+1, i0:i1+1]
            lat_covered = lats[j0:j1+1, i0:i1+1]
            temp = np.arange((j1+1-j0)*(i1+1-i0)).reshape((j1+1-j0, i1+1-i0))
            cp = np.cos(lat_covered*np.pi/180.)
            dx=(lon-lon_covered)*cp
            dy=lat-lat_covered
            dist=dx*dx+dy*dy
            i=np.argmin(dist)
#            index = np.argwhere(temp=np.argmin(dist))
            index = np.where(temp==i)
            min_dist=np.sqrt(dist[index])
            return index[0]+j0, index[1]+i0
    
if __name__ == '__main__':
#    figure_with_basemap().show()
