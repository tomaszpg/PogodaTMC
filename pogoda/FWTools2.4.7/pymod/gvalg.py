###############################################################################
# $Id: gvalg.py,v 1.7 2004/11/19 23:59:37 gmwalter Exp $
#
# Project:  CIETMap/OpenEV
# Purpose:  Assorted algorithm python entry points.
# Author:   Frank Warmerdam, warmerda@home.com
#
###############################################################################
# Copyright (c) 2000, Frank Warmerdam, warmerda@home.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################
#
#  $Log: gvalg.py,v $
#  Revision 1.7  2004/11/19 23:59:37  gmwalter
#  Check in Aude's rasterization updates.
#
#  Revision 1.6  2002/12/13 21:21:04  warmerda
#  Fixed docs.
#
#  Revision 1.5  2002/12/13 21:13:33  warmerda
#  Added some user documentation.
#
#  Revision 1.4  2001/04/22 17:34:21  pgs
#  changed wid_interpolate to take variable exponent for d
#
#  Revision 1.3  2001/03/29 14:59:56  warmerda
#  added fill_short flag to control handling of slivers
#
#  Revision 1.2  2000/09/15 15:13:14  warmerda
#  flush raster
#
#  Revision 1.1  2000/09/15 01:44:12  warmerda
#  New
#
#

import _gv

"""
Python wrappers for various algorithms.
"""


###############################################################################

def rasterize_shapes( raster, shapes, burn_value, fill_short = 1 ):
    """Rasterize GvShape polygons into a GvRaster.

    A python list of GvShapes are burned into a GvRaster with a user supplied
    "burn value".  Only polygons are supported at this time.   The polygon
    coordinates must be in the same coordinate system as the GvRaster.  The
    polygons may have inner rings, or even multiple outer rings.

    Example:
     import gvalg, gview
     
     polygons = gview.GvShapes( shapefilename = poly_filename )

     rfile = gdal.GetDriverByName('GTiff').Create(filename,xsize,ysize,1)
     rfile.SetGeoTransform( geotransform )
     raster = gview.GvRaster( dataset = rfile )

     gvalg.rasterize_shapes( raster, polygons, 255 )


    raster -- a GvRaster with update access.
    shapes -- A GvShapes or list object containing the list of shapes to
              burn into the raster.
    burn_value -- The value to be assigned to pixels under the polygons.
    fill_short -- 1 to fill partial scanlines, or 0 to not do so.

    NEW: fill_short = 2: same algorithm as above but with less bugs
         fill_short = 3: a pixel is considered inside the shape if and only if its
         centre is inside the shape. 
               

    Returns 0 on failure, or a non-zero value on success.
    """
    
    shapes_o = []
    for shape in shapes:
        shapes_o.append( shape._o )

    ret = _gv.gv_raster_rasterize_shapes( raster._o, shapes_o, burn_value,
                                          fill_short )
    raster.get_band().FlushCache()
    return ret

###############################################################################

def wid_interpolate( raster, points, exponent = 2.0, progress_cb=None, cb_data=None ):

    """Weighted Inverse Distance Interpolation

    This algorithm interpolates the pixel values of a GvRaster using a simple
    inverse distance interpolator with an additional per point weighting
    factor.  The algorithm supports GDALProcessFunc style
    progress reporting, and user termination support.

    Note that the (x,y) values for the points must be in pixel/line coordinates
    on the raster, not georeferenced coordinates.  They may have subpixel
    accuracy. 
 
    points -- a list of (x,y,value,weight) tuples where each tuple is
    a point to interpolate.  
 
    raster -- the GvRaster representating the band to apply changes to.
    The GvRaster must be in update mode.
 
    exponent -- the exponent to apply to the distance calculate in the
    weighting formula
 
    progress_cb -- progress function, leave defaulted if no progress called
    is needed.

    cb_data -- a value to be passed into the progress_cb. 
 
    Returns a CPL error number on failure, or 0 on success.  Note that
    a user interrupt will result in CPLE_UserInterrupt being returned.
    """
    
    ret = _gv.WIDInterpolate( points, raster.get_band()._o,
                              exponent, progress_cb, cb_data )
    raster.get_band().FlushCache()
    return ret



