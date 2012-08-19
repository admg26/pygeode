from wrappers import AxesWrapper, PlotOp, Contour, Contourf, make_plot_func, make_plot_member

from mpl_toolkits.basemap import Basemap
class BasemapAxes(AxesWrapper):
  def _build_axes(self, fig, root):
# {{{
    AxesWrapper._build_axes(self, fig, root)

    proj = {'projection':'cyl', 'resolution':'c'}
    proj.update(self.axes_args)
    self.bm = Basemap(ax = self.ax, **proj)
# }}}

  def setp(self, **kwargs):
# {{{
    proj = self.axes_args.get('projection', 'cyl')
    if proj in ['cyl', 'merc', 'mill', 'gall']:
      bnds = {}
      if kwargs.has_key('xlim'):
        x0, x1 = kwargs.pop('xlim')
        bnds['llcrnrlon'] = x0
        bnds['urcrnrlon'] = x1
      if kwargs.has_key('ylim'):
        y0, y1 = kwargs.pop('ylim')
        bnds['llcrnrlat'] = y0
        bnds['urcrnrlat'] = y1
      self.axes_args.update(bnds)

    kwargs.pop('xscale', None)
    kwargs.pop('yscale', None)

    self.args.update(kwargs)
# }}}

  def setp_xaxis(self, **kwargs):
# {{{
    kwargs.pop('major_locator', None)
    kwargs.pop('minor_locator', None)
    kwargs.pop('major_formatter', None)
    kwargs.pop('minor_formatter', None)
    AxesWrapper.setp_xaxis(self, **kwargs)
# }}}

  def setp_yaxis(self, **kwargs):
# {{{
    kwargs.pop('major_locator', None)
    kwargs.pop('minor_locator', None)
    kwargs.pop('major_formatter', None)
    kwargs.pop('minor_formatter', None)
    AxesWrapper.setp_yaxis(self, **kwargs)
# }}}

# Contour
class BMContour(Contour):
# {{{
  @staticmethod
  def transform(bm, args):
    from numpy import meshgrid, ndarray
    from warnings import warn
    # Z
    if len(args) == 1: return args
    # X, Y, Z
    if len(args) == 3:
      X, Y, Z = args
      X, Y = meshgrid(X, Y)
      X, Y = bm(X, Y)
      return X, Y, Z
    # Z, N
    if len(args) == 2 and isinstance(args[1],(int,list,tuple,ndarray)): return args
    # X, Y, Z, N
    if len(args) == 4 and isinstance(args[3],(int,list,tuple,ndarray)):
      X, Y, Z, N = args
      X, Y = meshgrid(X, Y)
      X, Y = bm(X, Y)
      return X, Y, Z, N
    #TODO: finish the rest of the cases
    warn("Don't know what to do for the coordinate transformation")
    return args

  def render (self, axes):
    bm = self.axes.bm
    args = BMContour.transform(bm, self.plot_args)
    self._cnt = bm.contour (*args, **self.plot_kwargs)
# }}}

class BMContourf(Contourf):
# {{{
  def render (self, axes):
    bm = self.axes.bm
    args = BMContour.transform(bm, self.plot_args)
    self._cnt = bm.contourf (*args, **self.plot_kwargs)
# }}}

class BMDrawCoast(PlotOp):
# {{{
  def render (self, axes):
    bm = self.axes.bm
    bm.drawcoastlines(*self.plot_args, ax = axes, **self.plot_kwargs)
# }}}

class BMDrawMeridians(PlotOp):
# {{{
  def render (self, axes):
    bm = self.axes.bm
    bm.drawmeridians(*self.plot_args, ax = axes, **self.plot_kwargs)
# }}}

class BMDrawParallels(PlotOp):
# {{{
  def render (self, axes):
    bm = self.axes.bm
    bm.drawparallels(*self.plot_args, ax = axes, **self.plot_kwargs)
# }}}

bmcontour = make_plot_func(BMContour)
bmcontourf = make_plot_func(BMContourf)
drawcoastlines = make_plot_func(BMDrawCoast)
drawmeridians = make_plot_func(BMDrawMeridians)
drawparallels = make_plot_func(BMDrawParallels)

BasemapAxes.contour = make_plot_member(bmcontour)
BasemapAxes.contourf = make_plot_member(bmcontourf)
BasemapAxes.drawcoastlines = make_plot_member(drawcoastlines)
BasemapAxes.drawmeridians = make_plot_member(drawmeridians)
BasemapAxes.drawparallels = make_plot_member(drawparallels)

__all__ = ['BasemapAxes', 'bmcontour', 'bmcontourf', 'drawcoastlines', 'drawmeridians', 'drawparallels']
