#!/usr/bin/env python

import numpy as np
import xarray as xr

class PolarVortex():
    '''This module contains functions to calculate equivalent latitude and edge of a polar vortex 
      according to Nash criteria.
    '''
    def __init__(self, pv, uwind, npoints=90, elat=np.arange(0, 90)):
        self.pv = pv
        self.elat = elat
        self.uwind = uwind
        self.ylat = pv.latitude.values
        self.xlon = pv.longitude.values
        self.zlev = pv.level.values
        self.time = pv.time.values
        self.nlat = self.ylat.size
        self.nlon = self.xlon.size
        self.ntim = self.time.size
        self.nlev = self.zlev.size
        self.nelat = self.elat.size
        self.npoints = npoints

    def get_edge(self, min_eql=30):
        eq = self.get_eql()
        ulat = self._eql_wind(eq)
        pvlat = self._equivalent_relation()
        pvv = np.reshape(pvlat.values, (self.ntim*self.nlev, self.nelat))
        uuu = np.reshape(ulat.values, (self.ntim*self.nlev, self.nelat))
        edge = np.zeros(self.ntim*self.nlev)
        for i in np.arange(self.ntim*self.nlev):
            egrad = uuu[i, :]*np.gradient(pvv[i, :], self.elat)
            egrad *= self._sloping_filter()
            edge[i] = np.argmax(egrad[min_eql:]) + min_eql
        edge = np.reshape(edge, (self.ntim, self.nlev))
        edge = xr.DataArray(edge, dims=['time', 'level'], \
                            coords=[self.time, self.zlev])
        edge.attrs['long_name'] = 'Polar Vortex Edge (in degree)'
        eqlat = xr.Dataset({'vedge':edge, 'eql':eq['eql']})
        return eqlat

    def get_eql(self):
        area = self._get_area(self.ylat, self.xlon)
        ds = self.pv.values.reshape([self.ntim*self.nlev, \
                                     self.nlat, self.nlon])
        eq = np.zeros_like(ds)
        for i in np.arange(ds.shape[0]):
            q_part_u, lat_part = self._eqvlat(ds[i], area, self.npoints)
            eq[i] = np.interp(ds[i], q_part_u, lat_part)
        eq = eq.reshape(self.ntim, self.nlev, self.nlat, self.nlon)
        eq = xr.DataArray(eq, dims=['time', 'level', 'lat', 'lon'], \
                          coords=[self.time, self.zlev, self.ylat, self.xlon])
        eq.attrs['long_name'] = 'Equivalent Latitude'
        ds = xr.Dataset({'eql':eq})
        return ds

    def _eql_wind(self, eq):
        eql = np.reshape(eq.eql.values, (self.ntim*self.nlev, \
                                         self.nlat*self.nlon))
        u = np.reshape(self.uwind.values, (self.ntim*self.nlev,\
                                           self.nlat*self.nlon))

        ul = np.zeros((self.ntim*self.nlev, self.nelat))
        for i in np.arange(eql.shape[0]):
            idx = np.digitize(eql[i, :], self.elat)
            for j in self.elat:
                ul[i, j] = np.nanmean(u[i, idx==j])
        ul = np.reshape(ul, (self.ntim, self.nlev, self.nelat))
        eq = xr.DataArray(ul, dims=['time', 'level', 'lat'],\
                          coords=[self.time, self.zlev, self.elat])
        eq.attrs['long_name'] = 'Equivalent Latitude Relationship'
        return eq

    def _equivalent_relation(self):
        ds = self.pv.values.reshape([self.ntim*self.nlev,\
                                     self.nlat, self.nlon])
        area = self._get_area(self.ylat, self.xlon)
        ulat = np.zeros((self.ntim*self.nlev, len(self.elat)))
        for i in np.arange(self.ntim*self.nlev):
            q_part_u, lat_part = self._eqvlat(ds[i, ...], area, self.npoints)
            ulat[i, :] = np.interp(self.elat, lat_part, q_part_u)
        ulat = np.reshape(ulat, (self.ntim, self.nlev, self.nelat))
        eq = xr.DataArray(ulat, dims=['time', 'level', 'lat'],\
                          coords=[self.time, self.zlev, self.elat])
        eq.attrs['long_name'] = 'Equivalent Latitude Relationship'
        return eq

    def _sloping_filter(self):
        fil = pd.Series(np.ones_like(self.elat), index=self.elat).astype('float')
	fil[elat>=80] = np.linspace(1, 0, np.sum(elat>=80))    
	return fil.values

    @staticmethod
    def _get_area(ylat, xlon, planet_radius=6.378e+6):
        nlon = xlon.size
        nlat = ylat.size
        k = 2*np.pi*planet_radius**2
        dphi = (ylat[2]-ylat[1])*np.pi/180.
        area = dphi/float(nlon) * np.ones((nlat, nlon))
        area = k*(np.cos(ylat[:, np.newaxis]*np.pi/180.)*area)
        return np.abs(area)

    @staticmethod
    def _eqvlat(vort, area, n_points, planet_radius=6.378e+6):
        q_part_u = np.linspace(vort.min(), vort.max(), n_points, endpoint=True)
        aa = np.zeros(q_part_u.size)  # to sum up area
        vort_flat = vort.flatten()  # Flatten the 2D arrays to 1D
        area_flat = area.flatten()
        inds = np.digitize(vort_flat, q_part_u)
        for i in np.arange(0, aa.size):  # Sum up area in each bin
            aa[i] = np.sum(area_flat[np.where(inds == i)])
        aq = np.sort(np.cumsum(aa))[::-1]
        y_part = 1.0 - aq/(2*np.pi*planet_radius**2)
        lat_part = np.rad2deg(np.arcsin(y_part))
        return q_part_u, lat_part
