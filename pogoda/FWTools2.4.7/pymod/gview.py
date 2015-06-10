###############################################################################
# $Id: gview.py,v 1.213 2006/01/06 19:00:01 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  Shadow classes for OpenEV C to Python bindings
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2000, Atlantis Scientific Inc. (www.atlsci.com)
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
#  $Log: gview.py,v $
#  Revision 1.213  2006/01/06 19:00:01  gmwalter
#  Set locale after gtk is imported (gtk resets otherwise).
#
#  Revision 1.212  2005/10/17 19:19:15  gmwalter
#  Wrap gvshape delete_ring function.
#
#  Revision 1.211  2005/09/12 15:33:10  gmwalter
#  Update autopan tool for line paths.
#
#  Revision 1.210  2005/07/06 18:16:47  gmwalter
#  Set translation directly in opening projects
#  (using relative translations was causing
#  problems in some applications when view
#  translation wasn't 0,0 to start with).
#
#  Revision 1.209  2005/04/06 14:08:46  gmwalter
#  Bring gvdata freeze/thaw functions up to Python level.
#
#  Revision 1.208  2005/02/22 13:22:38  gmwalter
#  Add autopan tool.
#
#  Revision 1.207  2005/01/17 18:37:51  gmwalter
#  Add ability to reset tool cursor type.
#
#  Revision 1.206  2005/01/14 16:51:51  gmwalter
#  Checked in Aude's gv_shapes_add_shape_last function
#  (allows shapes to be added without repeating
#  indices if others have been deleted).
#
#  Revision 1.205  2005/01/14 15:30:16  warmerda
#  Added flip flag access, and save/restore in project file
#
#  Revision 1.204  2005/01/04 18:50:31  gmwalter
#  Checked in Aude's new gvshape function changes.
#
#  Revision 1.203  2004/09/30 21:10:51  warmerda
#  added sink() in lots of appropriate places
#
#  Revision 1.202  2004/08/20 13:58:30  warmerda
#  GvPqueryLayer: GvShapes in constructor, serialize/deserialize support
#
#  Revision 1.201  2004/08/18 17:27:50  warmerda
#  Don't blow a gasket if the histogram is empty in
#  GvRasterLayer.equalize().
#
#  Revision 1.200  2004/07/02 16:40:51  dem
#  - Implement project files portability
#  - last_strech restored in projects reloading
#  - add a "File/Save Project as..." menu
#
#  Revision 1.199  2004/06/23 14:35:06  gmwalter
#  Added support for multi-band complex imagery.
#
#  Revision 1.198  2004/04/21 14:44:29  andrey_kiselev
#  Fixed problem with reading NODATA value from the project file.
#
#  Revision 1.197  2004/04/13 15:07:13  gmwalter
#  Fix raster layer set_source so that it
#  gets min/max values from raster rather
#  than uninitialized sources in itself.
#
#  Revision 1.196  2004/02/27 14:17:05  warmerda
#  applied fix to preserve no-data value when stretching
#
#  Revision 1.195  2004/02/18 16:59:51  andrey_kiselev
#  Determine real mix/max values in GvRasterLayer.set_source().
#
#  Revision 1.194  2004/02/12 22:36:07  gmwalter
#  Add functions for easily creating a line from three
#  lists of nodes (x,y,z), avoiding python-level for
#  loop.
#
#  Revision 1.193  2004/02/10 15:49:59  andrey_kiselev
#  Added GvManager.add_dataset method.
#
#  Revision 1.192  2004/01/22 20:54:58  andrey_kiselev
#  New methods in GvRasterLayer class: nodata_get(), nodata_set(), type_get().
#  get_nodata() method now deprecated (though, it does the same as nodata_get).
#
#  Revision 1.191  2003/10/03 13:58:58  gmwalter
#  Avoid deprecation warning.
#
#  Revision 1.190  2003/09/16 15:43:12  gmwalter
#  Add single selection mode to select tool, checked in developer tutorials.
#
#  Revision 1.189  2003/09/12 18:32:32  pgs
#  modified get_preference to return default, added set_default_preferences
#
#  Revision 1.188  2003/09/11 20:00:32  gmwalter
#  Add ability to specify a preferred polynomial order for warping a raster,
#  and add "safe mode" (only used if ATLANTIS_BUILD is defined).
#
#  Revision 1.187  2003/09/02 17:27:11  warmerda
#  Added GvSymbolManager support on the GvShapesLayer.
#  Added has_symbol() and get_names() methods on symbol manager.
#  Added serialize/deserialize support for symbol manager.
#
#  Revision 1.186  2003/08/29 20:53:51  warmerda
#  use C GvShape xml serialize/deserialize version
#
#  Revision 1.185  2003/08/26 17:36:03  warmerda
#  added recode()
#
#  Revision 1.184  2003/08/20 20:02:32  warmerda
#  Added collection support to GvShape.
#  Fixed integer type support in GvRecords.add_field().
#
#  Revision 1.183  2003/08/14 19:07:27  warmerda
#  added MultiStratifiedCollect()method on GvRecords
#
#  Revision 1.182  2003/08/11 15:34:34  warmerda
#  don't save nodata attribute for raster layer sources if not set
#
#  Revision 1.181  2003/08/06 22:25:15  warmerda
#  added progress monitor to gv_records load/save funcs
#
#  Revision 1.180  2003/08/06 17:10:20  warmerda
#  added selection option to GvRecords.save_to_dbf()
#
#  Revision 1.179  2003/08/05 16:21:58  warmerda
#  fleshed out GvRecords implementation
#
#  Revision 1.178  2003/06/25 17:08:57  warmerda
#  added rotate tool
#
#  Revision 1.177  2003/05/23 16:18:17  warmerda
#  added GvRecords for CIETMap
#
#  Revision 1.176  2003/04/13 04:24:05  warmerda
#  dont flake out on none shapes when serializing
#
#  Revision 1.175  2003/04/08 11:59:47  andrey_kiselev
#  Added save_vector_symbol() wrapper for gv_symbol_manager_save_vector_symbol().
#
#  Revision 1.174  2003/04/02 15:47:00  pgs
#  added wrapper for gv_format_point_query
#
#  Revision 1.173  2003/03/07 17:03:03  gmwalter
#  Move last_complex_lut property setting down to c-level, fix magphase indeterminate
#  phase colour setting.
#
#  Revision 1.172  2003/02/28 16:50:28  warmerda
#  Added GvSymbolManager support
#
#  Revision 1.171  2003/02/20 19:27:20  gmwalter
#  Updated link tool to include Diana's ghost cursor code, and added functions
#  to allow the cursor and link mechanism to use different gcps
#  than the display for georeferencing.  Updated raster properties
#  dialog for multi-band case.  Added some signals to layerdlg.py and
#  oeattedit.py to make it easier for tools to interact with them.
#  A few random bug fixes.
#
#  Revision 1.170  2002/10/30 21:26:47  warmerda
#  Paul added pick_shape
#
#  Revision 1.169  2002/09/11 20:40:50  warmerda
#  fixed so that 3d views can be saved
#
#  Revision 1.168  2002/09/10 21:17:46  warmerda
#  change strstr() to str() in 3d view stuff
#
#  Revision 1.167  2002/09/10 13:27:28  warmerda
#  added get_height_scale method
#
#  Revision 1.166  2002/08/01 22:01:05  warmerda
#  removed debug print
#
#  Revision 1.165  2002/08/01 20:11:45  warmerda
#  minor changes for vector capable classifications
#
#  Revision 1.164  2002/08/01 14:53:17  pgs
#  removed superfluous XMLFind in gvviewarea initialize_from_xml
#
#  Revision 1.163  2002/07/25 15:49:14  warmerda
#  fix int overflow problem with equalize()
#
#  Revision 1.162  2002/07/24 20:33:22  warmerda
#  added gv_shape_get_property
#
#  Revision 1.161  2002/07/24 14:49:33  warmerda
#  added one-field option to get_schema
#
#  Revision 1.160  2002/07/23 16:39:50  pgs
#  minor bug fix in gvshapeslayer serialize
#
#  Revision 1.159  2002/07/18 19:43:53  warmerda
#  added gv_shapes_get_typed_properties
#
#  Revision 1.158  2002/07/18 19:35:16  pgs
#  added GvShapes.save_to_dbf()
#
#  Revision 1.157  2002/07/18 17:46:42  warmerda
#  Added get_layout() on GvShapes
#
#  Revision 1.156  2002/07/16 14:51:30  warmerda
#  serialize all shapes if there is no _filename
#
#  Revision 1.155  2002/07/16 14:31:23  warmerda
#  removed serialization of selection, made stuff Python 2.0 compatible
#
#  Revision 1.154  2002/07/16 14:17:31  warmerda
#  added support for getting background color
#
#  Revision 1.153  2002/07/15 20:27:12  pgs
#  added XML serialization support for GvShapesLayer and ancestors\nand added restoration of raster layer classifications
#
#  Revision 1.152  2002/07/12 12:46:05  warmerda
#  expanded tabs
#
#  Revision 1.151  2002/07/08 19:46:03  warmerda
#  added project save/load capability
#
#  Revision 1.150  2002/07/07 21:06:14  warmerda
#  preliminary addition of project saving
#
#  Revision 1.149  2002/06/27 15:43:51  warmerda
#  added preliminary serialize() support
#
#  Revision 1.148  2002/04/12 14:40:37  gmwalter
#  Removed the gvmesh rescale function (not needed because of view area
#  rescaling).
#
#  Revision 1.146  2002/03/07 18:31:56  warmerda
#  added preliminary gv_shape_clip_to_rect() implementation
#
#  Revision 1.145  2002/03/07 02:31:56  warmerda
#  added default_height to add_height functions
#
#  Revision 1.144  2002/03/04 16:00:09  warmerda
#  fixed autoscaling with equalization
#
#  Revision 1.143  2002/02/28 18:52:22  gmwalter
#  Added a point-of-interest tool similar to the region-of-interest
#  tool (allows a user to select a temporary point without having to add a
#  new layer).  Added a mechanism to allow some customization of openev
#  via a textfile defining external modules.
#
#  Revision 1.142  2002/01/18 05:48:13  warmerda
#  added GvShapes.get_extents() method in python
#
#  Revision 1.141  2001/12/11 17:51:13  warmerda
#  fixed GvRasterLayer.autoscale() to call self.autoscale_view() when appr.
#
#  Revision 1.140  2001/12/11 15:12:03  gmwalter
#  Increased default cache sizes for openev, updated mkdist to
#  copy files under their original rather than linked names.
#
#  Revision 1.139  2001/12/08 04:49:39  warmerda
#  added point in polygon test
#
#  Revision 1.138  2001/11/28 19:21:33  warmerda
#  Added set_gcps(), and get_gcps() on GvRaster.
#  Added info on geotransform-changed signal on GvRaster.
#
#  Revision 1.137  2001/10/17 16:25:58  warmerda
#  added support for appling complex luts
#
#  Revision 1.136  2001/10/16 18:51:18  warmerda
#  added raster layer histogram, autoscale, and various enhancements
#
#  Revision 1.135  2001/10/02 20:30:06  warmerda
#  update code for establishing .openev file to work on win98
#
#  Revision 1.134  2001/08/14 17:03:24  warmerda
#  added standard deviation autoscaling support
#
#  Revision 1.133  2001/08/08 17:46:52  warmerda
#  added GvShape reference counting support
#
#  Revision 1.132  2001/08/08 02:59:04  warmerda
#  added gv_data_registry_dump()
#
#  Revision 1.131  2001/08/07 18:40:45  warmerda
#  fixed get_view() for unset views on GvTool
#
#  Revision 1.130  2001/07/24 21:21:45  warmerda
#  added EV style phase colormap
#
#  Revision 1.129  2001/07/24 02:59:25  warmerda
#  added force_load method on GvRaster
#
#  Revision 1.128  2001/07/24 02:21:54  warmerda
#  added 8bit phase averaging
#
#  Revision 1.127  2001/07/16 15:04:41  warmerda
#  added get_height and build_skirt on GvRasterLayer
#

import gtk; _gtk = gtk; del gtk
import _gtkmissing
import _gv
import gvutils
import os.path, sys
import os
import string
import pgu
import gdal
from gvconst import *
from gdalconst import *
import pathutils

# Force standard c settings for floating point (. rather than ,)
# Note: this import must be done AFTER gtk is imported, as gtk
#       sets the locale during initialization.
import locale
locale.setlocale(locale.LC_NUMERIC,'C')

"""
Classes for viewing and interacting with geographic image and vector data.
"""

###############################################################################
# A few notes on gview.py
#
# obj2inst():
#
# The GtkObject derived OpenEV classes are automatically registered with
# the gtk name2cls mechanism by some startup code at the bottom of this
# module (search for name2cls).  Basically any class in this module starting
# with Gv is assumed to:
#  - Be derived from GtkObject
#  - Have a get_type attributes which is the _gv get type method.
#
# Based on this, the _gtk._obj2inst() method can be used to create a
# Python shadow class for any of the raw object handles (_o).  It will
# create the correct type based on the name to class translation and the
# name returned by the get_type attribute.
#
# Note that two obj2inst() calls with one GtkObject will result in two
# Python shadow objects for the same underlying GtkObject.
###############################################################################

SMAverage = 0
SMSample = 1
SMAverage8bitPhase = 2

###############################################################################
class GvViewArea(_gtk.GtkDrawingArea):
    """Gtk geographic view area.

    Signals:

    gldraw -- This signal is emitted after all layers have drawn themselves
    but before the result is displayed to the user.  It provides a hook
    whereby application code can do additional drawing.

    active-changed -- This signal is emitted after the active layer has been
    modified, or when a layer is added or removed from the view.  It can be
    used to update tools that depend on the active layer.

    view-state-changed -- This signal is emitted after the view state changes.
    This includes flipping, zooming and roaming.  It does not include mouse
    position changes.

    Note that the GvViewArea is a GtkWidget, and application code may attach
    callbacks to the motion-notify-event, button-press-event, key-press-event
    and other similar events.  The map_pointer() method should be used
    to translate raw GtkWidget coordinates to georeferenced positions.
    """
        
    get_type = _gv.gv_view_area_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_view_area_new()
        if self._o is None:
            raise ValueError, "Failed to create GvViewArea, is OpenGL working?"

    def serialize(self, filename=None ):
        tree = [gdal.CXT_Element, 'GvViewArea']

        tree.append( [CXT_Attribute, 'Mode',
                    [CXT_Text, str(self.get_mode())]] )
        tree.append( [CXT_Attribute, 'Raw',
                      [CXT_Text, str(self.get_raw())]] )

        translation = self.get_translation()
        tree.append( [CXT_Element, 'Translation',
                      [CXT_Attribute, 'x',
                       [CXT_Text, str(translation[0])]],
                      [CXT_Attribute, 'y',
                       [CXT_Text, str(translation[1])]]] )

        tree.append( [CXT_Element, 'Zoom',
                      [CXT_Text, str(self.get_zoom())]] )
        tree.append( [CXT_Element, 'FlipX', 
                      [CXT_Text, str(self.get_flip_x())]] )
        tree.append( [CXT_Element, 'FlipY', 
                      [CXT_Text, str(self.get_flip_y())]] )

        projection = self.get_projection()
        if projection is not None and len(projection) > 0:
            tree.append( [CXT_Element, 'Projection',
                          [CXT_Text, str(self.get_projection())]] )

        background = self.get_background_color()
        tree.append( [CXT_Element, 'Background',
                    [CXT_Attribute, 'red',
                     [CXT_Text, str(background[0])]],
                    [CXT_Attribute, 'green',
                     [CXT_Text, str(background[1])]],
                    [CXT_Attribute, 'blue',
                     [CXT_Text, str(background[2])]],
                    [CXT_Attribute, 'alpha',
                     [CXT_Text, str(background[3])]]] )

        if self.get_mode() == MODE_3D:
            eye_pos = self.get_eye_pos()
            tree.append( [CXT_Element, 'EyePos',
                        [CXT_Attribute, 'x',
                         [CXT_Text, str(eye_pos[0])]],
                        [CXT_Attribute, 'y',
                         [CXT_Text, str(eye_pos[1])]],
                        [CXT_Attribute, 'z',
                         [CXT_Text, str(eye_pos[2])]]] )
            eye_dir = self.get_eye_dir()
            tree.append( [CXT_Element, 'EyeDir',
                        [CXT_Attribute, 'x',
                         [CXT_Text, str(eye_dir[0])]],
                        [CXT_Attribute, 'y',
                         [CXT_Text, str(eye_dir[1])]],
                        [CXT_Attribute, 'z',
                         [CXT_Text, str(eye_dir[2])]]] )
            height_scale = self.get_height_scale()
            tree.append( [CXT_Element, 'HeightScale',
                          [CXT_Text, str(height_scale)]] )

        layer_tree = [CXT_Element, 'Layers']
        tree.append( layer_tree )

        layers = self.list_layers()
        for layer in layers:
            layer_tree.append( layer.serialize( filename=filename ) )

        return tree

    def initialize_from_xml( self, tree, filename=None ):
        self.set_property( '_supress_realize_auto_fit', 'on' )

        layer_trees = gvutils.XMLFind( tree, 'Layers')
        if layer_trees is not None:
            for layer_tree in layer_trees[2:]:
                layer = gvutils.XMLInstantiate( layer_tree, self, filename=filename )
                if layer is not None:
                    self.add_layer( layer )
                    self.set_active_layer( layer )
                else:
                    print 'Failed to instantiate layer:', layer_tree

        tr = gvutils.XMLFind( tree, 'Translation')
        if tr is not None:
            x = float(gvutils.XMLFindValue( tr, 'x', '0.0'))
            y = float(gvutils.XMLFindValue( tr, 'y', '0.0'))
            self.set_translation(x,y)

        zm = float(gvutils.XMLFindValue( tree, 'Zoom', 
                                         str(self.get_zoom()) ))
        self.zoom( zm - self.get_zoom() )

        flip_x = int(gvutils.XMLFindValue( tree, 'FlipX','1'))
        flip_y = int(gvutils.XMLFindValue( tree, 'FlipY','1'))
        self.set_flip_xy( flip_x, flip_y )

        bg = gvutils.XMLFind( tree, 'Background')
        if bg is not None:
            self.set_background_color(
                (float(gvutils.XMLFindValue( bg, 'red', '0.0')),
                 float(gvutils.XMLFindValue( bg, 'green', '0.0')),
                 float(gvutils.XMLFindValue( bg, 'blue', '0.0')),
                 float(gvutils.XMLFindValue( bg, 'alpha', '1.0'))) )

        eye_pos_xml = gvutils.XMLFind( tree, 'EyePos' )
        if eye_pos_xml is not None:
            eye_pos = (float(gvutils.XMLFindValue( eye_pos_xml, 'x', '0.0')),
                       float(gvutils.XMLFindValue( eye_pos_xml, 'y', '0.0')),
                       float(gvutils.XMLFindValue( eye_pos_xml, 'z', '1.0')))
            eye_dir_xml = gvutils.XMLFind( tree, 'EyeDir' )
            eye_dir = (float(gvutils.XMLFindValue( eye_dir_xml, 'x', '0.0')),
                       float(gvutils.XMLFindValue( eye_dir_xml, 'y', '0.0')),
                       float(gvutils.XMLFindValue( eye_dir_xml, 'z', '-1.0')))
            self.set_3d_view( eye_pos, eye_dir )

            self.height_scale(
                float(gvutils.XMLFindValue( tree, 'HeightScale', '1.0' )) )
            
            self.set_mode( MODE_3D )
                
    def get_width(self):
        """Return width of area in pixels."""
        return _gv.gv_view_area_get_width(self._o)
    
    def get_height(self):
        """Return height of area in pixels."""
        return _gv.gv_view_area_get_height(self._o)
    
    def add_layer(self, layer):
        """Add a new layer to the view window. 

        Arguments

          layer -- abc A GvLayer derived object to add to the view."""
        _gv.gv_view_area_add_layer(self._o, layer._o)

    def remove_layer(self, layer):
        """Remove a layer from view window.

        Arguments

          layer -- the layer to remove"""
        _gv.gv_view_area_remove_layer(self._o, layer._o)

    def get_named_layer(self, name):
        """Fetch the named layer from this view

        Returns None if no such layer exists on the view."""

        _o = _gv.gv_view_area_get_named_layer(self._o,name)
        if _o is not None: return _gtk._obj2inst(_o)
        return _o

    def active_layer(self):
        """Fetch the active layer for this view"""
        _o = _gv.gv_view_area_active_layer(self._o)
        if _o: return _gtk._obj2inst(_o)
        return _o

    def set_active_layer(self, layer):
        """Set the active layer for this view.

        It is an error to make a layer active if it has not already
        been added to the view.

        Arguments

          layer -- GvLayer to make active."""

        _gv.gv_view_area_set_active_layer(self._o, layer._o)

    def list_layers(self):
        """Fetch list of layers attached to this view."""
        l = _gv.gv_view_area_list_layers(self._o)
        return map(_gtk._obj2inst, l)

    def swap_layers(self, layer_a, layer_b):
        """Swap two layers in the display order stack.

        Arguments

          layer_a -- Integer index (within list_layers result) of first layer.
          
          layer_b -- Integer index (within list_layers result) of second layer.
          """
        _gv.gv_view_area_swap_layers(self._o, layer_a, layer_b)

    def create_thumbnail(self, layer, w, h):
        """Return area thumbnail as a GdkWindow.

        Arguments

          layer -- the GvLayer to render into the thumbnail.

          w -- Width in pixels of thumbnail.

          h -- Height in pixel of thumbnail."""
        return _gv.gv_view_area_create_thumbnail(self._o, layer._o, w, h)

    def zoom(self, zoom):
        """Zoom in or out.

        Note that the zoom value is log base 2 of the linear zoom factor.
        So to zoom in by a factor of 2, you would pass 1.  To zoom in by
        a factor of 8 you would pass 3.  To zoom out by a factor of eight
        you would pass -8.
        
        zoom -- the value to add to the current zoom factor."""
        _gv.gv_view_area_zoom(self._o,zoom)

    def get_zoom(self):
        """Get zoom value.

        Note that the zoom value is log base 2 of the linear zoom factor.
        So a zoom value of 1 means the view is zoomed in by a factor of 2.
        Similarly, a value of 3 means zoomed in by a factor of 8.  Negative
        values indicate zoomed out.
        """
        
        return _gv.gv_view_area_get_zoom(self._o)

    def rotate(self, angle):
        """Rotate view about center.

        angle -- the angle to rotate about the center by in degrees.  Positive
        is causes view contents to rotate counter-clockwise."""
        _gv.gv_view_area_rotate(self._o,angle)

    def translate(self, dx, dy):
        """Translate view by dx and dy.

        dx -- the amount to translate along the x axis in georeferenced units
        dy -- the amount to translate along the y axis in georeferenced units """
        _gv.gv_view_area_translate(self._o,dx,dy)

    def set_translation(self, x, y):
        """Set view center translation.

        The translation values are in georeferenced coordinates, and to
        put the value (1000,2000) at the view center a translation of
        (-1000,-2000) is needed.
        
        x -- the X (easting) value for view center translation.
        y -- the Y (northing) value for view center translation."""
        _gv.gv_view_area_set_translation(self._o,x,y)

    def get_translation(self):
        """Get view center translation.

        The translation values are in georeferenced coordinates, and to
        put the value (1000,2000) at the view center a translation of
        (-1000,-2000) would be returned.  The value is returned as an
        (x,y) tuple."""
        
        return _gv.gv_view_area_get_translation(self._o)

    def get_flip_x( self ):
        """Fetch X flip flag.

        Normally 1, but will be -1 if an X flip (mirroring) has been applied.
        """
        return _gv.gv_view_area_get_flip_x(self._o)

    def get_flip_y( self ):
        """Fetch Y flip flag.

        Normally 1, but will be -1 if a Y flip (mirroring) has been applied.
        """
        return _gv.gv_view_area_get_flip_y(self._o)

    def set_flip_xy( self, flip_x, flip_y ):
        """Set x/y flip flags.

        flip_x -- x mirroring flag, 1 or -1.
        flip_y -- x mirroring flag, 1 or -1.
        
        A value of 1 is unflipped, and -1 is flipped (mirrored).
        """
        _gv.gv_view_area_set_flip_xy( self._o, flip_x, flip_y )

    def copy_state(self, src_view):
        """Copy the view state of another view.

        This includes translation, rotation, and zoom factor.
        
        src_view -- the GvViewArea to copy the state from."""
        _gv.gv_view_area_copy_state(self._o,src_view)

    def map_location(self, xy):
        """ Translates a point from the current view projection (line/pixel or lat/long)
        to georeferenced coordinates.  Useful for a go to function that permits the
        user to enter a coordinate, then use set_translation() with the mapped location.

        returns a (x,y) tuple in georeferenced coordinates

        xy -- (x,y) tuple in current view coordinates"""

        return _gv.gv_view_area_map_location(self._o, xy)

    def get_pointer(self):
        """Fetch current pointer position.

        The pointer value is returned as an (X,Y) tuple in georeferenced
        coordinates."""
        return _gv.gv_view_area_get_pointer(self._o)

    def map_pointer(self, xy):
        """Translate position to georef coords.

        Translates a pixel/line position into map (georeferenced) coordinates
        within the view.  The pixel/line coordinates might come from a raw
        GdkEvent, for instance.

        Returns an (x,y) tuple in georeferenced coordinates.
        
        xy -- (x,y) tuple in GvViewArea pixel coordinates"""
        return _gv.gv_view_area_map_pointer(self._o, xy)

    def inverse_map_pointer(self, xy):
        """Translate position from georef coords.

        Translates a map (georeferenced) position into pixel/line coordinates
        within the GvViewArea on screen.

        Returns an (x,y) tuple in pixel/line coordinates.
        
        xy -- (x,y) tuple in georeferenced coordinates"""
        return _gv.gv_view_area_inverse_map_pointer(self._o, xy)

    def get_volume(self):
        """Fetch volume of layers in view.

        Returns the world volume of all layers attached to a view (not just
        what can be currently seen).  The volume is returned as an
        (xmin, xmax, ymin, ymax, zmin, zmax) tuple.  In case of failure a
        dummy cube of (0,1000,0,1000,0,1000) is returned.

        NOTE: At this time the zmin/zmax are not computed, and are always
        the default 0,1000 values.
        """
        
        return _gv.gv_view_area_get_volume(self._o)

    def get_extents(self):
        """Fetch extents of view window.

        The extents are returned as an (xmin,ymin,xmax,ymax) tuple
        in georeferenced coordinates."""
        return _gv.gv_view_area_get_extents(self._o)

    def fit_extents(self,llx, lly, width, height):
        """Fit view window to region.

        The position and size of the window are in georeferenced coordinates.
        The translation, zoom and rotation are updated to fit the entire
        desired box.  If the aspect ratio of the box is different than the
        window, then the window will display the region centered, with
        extra area viewed in one dimension.  The rotation is always set to
        zero by this call. 
        
        llx -- X (easting) position of the lower left corner.
        lly -- Y (northing) position of the lower left corner.
        width -- Width of view region.
        height -- Height of view region."""
        _gv.gv_view_area_fit_extents(self._o, llx, lly, width, height)

    def fit_all_layers(self):
        """Fit view window to extents of all layers

        This sets the 2D and 3D views to the default.  In 2D the default
        sets the view to the minimum extents that will display all layers.
        In 3D a default view is set which approximately shows all the data
        in a reasonable way.  Note that both the 2D and 3D views are set
        regardless of the current mode.
        """
        _gv.gv_view_area_fit_all_layers(self._o)

    def get_projection(self):
        """Return view coordinate system.

        The coordinate system is returned in OGC WKT format, and will
        likely be an empty string if there is no coordinate system."""
        return _gv.gv_view_area_get_projection( self._o )

    def set_projection(self, proj):
        """Set the coordinate system of the view.

        Currently the only time the coordinate system can be modified
        is when there are no layers attached.  When raster layers are added
        to the view, they will attempt to reproject themselves to match the
        view if possible.  Vector layers do not currently do this.
        
        proj -- new coordinate system in OGC WKT."""
        _gv.gv_view_area_set_projection( self._o, proj )

    def set_background_color(self, color):
        """Set the background color of the view.

        color -- an RGBA tuple with the color value (scaled 0.0 to 1.0).
        For reasonable operation alpha should always be 1.0.
        """
        _gv.gv_view_area_set_background_color( self._o, color )

    def get_background_color(self):
        """Get the background color of the view.

        Returns the background color as an RGBA tuple with the color
        values scaled 0.0 to 1.0.
        """
        return _gv.gv_view_area_get_background_color( self._o )

    def print_to_file(self, width, height, filename, format='GTiff',
                      is_rgb = 1):
        """Print view (at indicated resolution) to raster file.

        width -- the desired raster width at which to render the image.
        height -- the desired raster height at which to render the image.
        filename -- the name of the file to write to.
        format -- the GDAL format to use (defaults to 'GTiff').
        is_rgb -- non-zero for RGB output or zero for greyscale output.

        If the aspect ratio of width:height is not the same as the
        aspect ratio of the view, the extents will be extended in one
        direction to ensure the entire view data is visible.

        This method return 0 on success or non-zero on failure."""
        
        return _gv.gv_view_area_print_to_file(self._o, width, height,
                                              filename, format, is_rgb)

    def print_postscript_to_file(self, width, height,
                                 ulx, uly, lrx, lry,
                                 is_rgb, filename):
        """Print view (at indicated resolution) to PostScript file.

        width -- the desired raster width at which to render the image.
        height -- the desired raster height at which to render the image.
        ulx -- the upper left corner of the image print area in inches
        uly -- the upper left corner of the image print area in inches
        lrx -- the lower right corner of the image print area in inches
        lry -- the lower right corner of the image print area in inches
        is_rgb -- non-zero for RGB output or zero for greyscale output.
        filename -- the name of the file to write to.

        If the aspect ratio of width:height is not the same as the
        aspect ratio of the view, the extents will be extended in one
        direction to ensure the entire view data is visible.

        This method return 0 on success or non-zero on failure."""
        
        return _gv.gv_view_area_print_postscript_to_file(
            self._o, width, height, ulx, uly, lrx, lry,
            is_rgb, filename)

    def page_setup(self):
        _gv.gv_view_area_page_setup()

    def print_to_windriver(self, width, height, 
                           ulx, uly, lrx, lry,
                           is_rgb = 1):
        """Print view to Windows Print Driver

        width -- the desired raster width at which to render the image.
        height -- the desired raster height at which to render the image.
        ulx -- the upper left corner of the image print area in inches
        uly -- the upper left corner of the image print area in inches
        lrx -- the lower right corner of the image print area in inches
        lry -- the lower right corner of the image print area in inches
        is_rgb -- non-zero for RGB output or zero for greyscale output.

        If the aspect ratio of width:height is not the same as the
        aspect ratio of the view, the extents will be extended in one
        direction to ensure the entire view data is visible.

        This method return 0 on success or non-zero on failure."""
        
        return _gv.gv_view_area_print_to_windriver(self._o, width, height,
                                                   ulx, uly, lrx, lry, is_rgb)

    def get_mode(self):
        """Get 2D/3D Mode

        Returns either gview.MODE_2D or gview.MODE_3D depending on the
        current mode of the view."""
        
        return _gv.gv_view_area_get_mode(self._o)
    
    def set_mode(self, flag_3D=MODE_2D):
        """Set 2D/3D view mode.

        Set the view mode to either 2D orthonormal projection or
        3D perspective projection.

        flag_3D -- Either gview.MODE_2D or gview.MODE_3D"""

        _gv.gv_view_area_set_mode(self._o, flag_3D)

    def set_3d_view(self, eye_pos, eye_dir ):
        """Set 3D view.

        Set the 3D view position, and direction. 

        eye_pos -- (x,y,z) tuple indicating the eye position in georeferenced
        coordinates.

        eye_dir -- (x,y,z) tuple indicating the direction of view.  (0,0,-1)
        is straight down
        """

        _gv.gv_view_area_set_3d_view( self._o, eye_pos, eye_dir )

    def set_3d_view_look_at(self, eye_pos, eye_look_at ):
        """Set 3D view.

        Set the 3D view position, and direction. 

        eye_pos -- (x,y,z) tuple indicating the eye position in georeferenced
        coordinates.

        eye_look_at -- (x,y) tuple indicating the position in the z-plane to
        look at.
        """

        _gv.gv_view_area_set_3d_view_look_at( self._o, eye_pos, eye_look_at)

    def get_eye_pos(self):
        """Fetch 3D eye position

        The 3D eye position is returned as an (x,y,z) tuple."""

        return _gv.gv_view_area_get_eye_pos(self._o)
        
    def get_eye_dir(self):
        """Fetch 3D eye direction

        The 3D eye direction is returned as an (x,y,z) tuple."""

        return _gv.gv_view_area_get_eye_dir(self._o)

    def get_look_at_pos(self):
        """Fetch georeference location in z-plane that eye is looking

        Location is returned as an (x,y) tuple, or None if looking above z-plane"""
        return _gv.gv_view_area_get_look_at_pos(self._o)
        
    def height_scale(self, scale=1.0):
        """Set height scaling factor.

        Has no effect unless in 3D mode.  A scale value of 2.0 will exaggerate
        all elevations by a factor of 2 relative to horizontal (georeferenced)
        coordinates.

        scale -- scale factor (originally 1.0)
        """
        _gv.gv_view_area_height_scale(self._o, scale)

    def get_height_scale(self):
        return _gv.gv_view_area_get_height_scale(self._o)

    def queue_draw( self ):
        """Force queuing of a redraw.

        This method should not normally be needed, as a redraw should be
        triggered any time something changes that would require a redraw.
        """
        _gv.gv_view_area_queue_draw( self._o )

    def get_fontnames( self ):
        """Get list of available fontnames.

        Returns a Python list of font name strings suitable for using with
        LABEL() tools on this view area.  Generally the same for all views.
        """
        return _gv.gv_view_area_get_fontnames( self._o )

    def get_raw( self, ref_layer = None ):
        """Check if in Raw Mode

        This returns true if the view is in raw mode relative to the identified
        raster layer.  Raw mode is active if the coordinate system of the
        display is the raw pixel/line coordinates of the indicated raster.

        ref_layer -- a GvRasterLayer to check against.  If ref_layer is None,
                     always returns 0. 
        """

        if ref_layer is None:
            return 0
        else:
            return _gv.gv_view_area_get_raw( self._o, ref_layer._o )

    def set_raw( self, ref_layer, raw_enable ):
        """Set Raw Mode Enable

        Force the layer to be in raw mode (raw_enable=TRUE) or in georeferenced
        mode (raw_enable=FALSE) relative to the indicated raster layer.  If
        this requires a change, the coordinate system, and view extents of
        the view will be altered, and the mesh of the underlying raster will
        also be altered.
        
        ref_layer -- a GvRasterLayer to check against.
        raw_enable -- TRUE to set raw mode or FALSE for georeferenced mode.

        A value of zero is returned if this operation is successful, or a
        value of non-zero on failure.
        """
        if ref_layer is None:
            return 1
        
        return _gv.gv_view_area_set_raw( self._o, ref_layer._o, raw_enable )

    def get_property(self,name):
        """Get a GvViewArea property.

        name -- the key or name of the property being set.  Should be a
        well behaved token (no spaces, equal signs, or colons).

        NOTE: Returns None if property does not exist."""
        
        return _gv.gv_view_area_get_property(self._o,name)

    def set_property(self,name,value):
        """Set a GvViewArea property.

        name -- the key or name of the property being set.  Should be a
        well behaved token (no spaces, equal signs, or colons).
        
        value -- the value to be assigned.  Any text is acceptable."""
        
        return _gv.gv_view_area_set_property(self._o,name,value)
        
    def format_point_query( self, x, y ):
        """Format a point as text
         
           x - the x coordinate to format
           y - the y coordinate to format
           
           TODO: provide information on formatting using preferences
                 to control output.
        """
        
        return _gv.gv_format_point_query( self._o, x, y )

###############################################################################
def GvShapeFromXML( tree, parent, filename=None ):
    """
    construct a gvshape object from an xml tree
    """
    
    _obj = _gv.gv_shape_from_xml( tree )
    return GvShape( _obj = _obj )

class GvShape:
    """Vector feature class for GvShapes/GvShapesLayer

    The following properties have special interpretation for a GvShape.
    Note that modifying these properties does not automatically trigger a
    display-change signal ... please call display_change() manually.

    _gv_color -- RGBA value used for point, line, or area edge color.
    
    _gv_fill_color -- RGBA value used for area fill color.
    
    Note that similar (names differ) color properties can also be set on the
    GvShapesLayer.  Setting these properties on a particular shape overrides
    any layer drawing styles for that shape.

    """
    
    def __init__(self, _obj=None,type=GVSHAPE_POINT):
        if _obj is None:
            _obj = _gv.gv_shape_new(type)

        _gv.gv_shape_ref( _obj )
        self.__dict__['_o'] = _obj

    def __del__(self):
        if self.__dict__['_o'] is not None:
            _gv.gv_shape_unref( self.__dict__['_o'] )
            self.__dict__['_o'] = None

    def copy(self):
        """Make a copy of a shape"""

        copy = _gv.gv_shape_copy( self._o )
        if copy is None:
            return None

        return GvShape( _obj=copy )

    def __getattr__(self,attr):
        if self.__dict__.has_key(attr):
            return self.__dict__[attr]

        value = _gv.gv_shape_get_property( self._o, attr )
        if value is None:
            raise AttributeError, attr
        else:
            return value

    def __delattr__(self,attr):
        if self.__dict__.has_key(attr):
            del self.__dict__[attr]

        properties = self.get_properties()
        if not properties.has_key(attr):
            raise AttributeError, attr
        else:
            del properties[attr]
            self.set_properties(properties)

    def __setattr__(self,attr,value):
        if attr == '_o':
            self.__dict__['_o'] = value
        else:
            self.set_property(attr,value)

    def __str__(self):
        result = ''
        properties = self.get_properties()
        for key in properties.keys():
            result = result + key + '=' + properties[key] + '\n'
            
        result = result + self.geometry_to_wkt() + '\n'

        return result

    def serialize( self, base = None ):
        """serialize this object in a format suitable for XML representation.
        """
        if base is not None:
            raise ValueError, 'GvShape.serialize() doesnt allow base'

        return _gv.gv_shape_to_xml( self._o )

    def geometry_to_wkt(self):
        t = self.get_type()
        fmt = '%f %f %f'
        geom = ''
        if t == GVSHAPE_POINT:
            geom = ('POINT ('+fmt+')') % self.get_node()
        elif t == GVSHAPE_LINE:
            geom = 'LINESTRING ('
            for node in range(self.get_nodes()):
                if node > 0:
                    geom = geom + ','
                term = fmt % self.get_node(node)
                geom = geom + term
            geom = geom + ')'
        elif t == GVSHAPE_AREA:
            geom = 'POLYGON ('
            for ring in range(self.get_rings()):
                if ring > 0:
                    geom = geom + ','
                geom = geom + '('
                for node in range(self.get_nodes()):
                    if node > 0:
                        geom = geom + ','
                    term = fmt % self.get_node(node)
                    geom = geom + term
                geom = geom + ')'
            geom = geom + ')'
        return geom

    def destroy(self):
        """Destroy shape.

        The GvShape is not a GtkObject, and doesn't employ the same
        reference counting mechanisms to ensure destruction when no longer
        referenced.  It is the applications responsibility to destroy
        GvShape's with an explicit call to the GvShape.destroy() method
        when appropriate."""
        if self.__dict__['_o'] is not None:
            _gv.gv_shape_unref(self.__dict__['_o'])
            self.__dict__['_o'] = None

    def get_properties(self):
        """Get GvShape properties (attributes) as a dictionary.

        The properties are returned as a Python dictionary.  Note that
        changes to this dictionary are not applied back to the GvShape."""
        return _gv.gv_shape_get_properties(self.__dict__['_o'])

    def get_typed_properties(self, prop_list):
        return _gv.gv_shape_get_typed_properties(self.__dict__['_o'],prop_list)

    def get_property(self,property_name, default_value=None):
        """Get the value of a property.

        Fetches the value of a single property on the shape.  Roughly
        equivelent to shape_obj.get_properties()[property_name] or
        shape_obj.property_name but if the property does not exist
        get_property() returns a default value instead of throwing an
        exception.

        property_name -- the name of the property (attribute field) to fetch.
        default_value -- the value to return if the property does not exist,
                         defaults to None.

        Returns the property value (always a string) or the default value."""

        value = _gv.gv_shape_get_property( self._o, property_name )
        if value is None:
            return default_value
        else:
            return value

    def set_property(self,name,value):
        """Set a GvShape property.

        name -- the key or name of the property being set.  Should be a
        well behaved token (no spaces, equal signs, or colons).
        
        value -- the value to be assigned.  Any text is acceptable."""
        
        return _gv.gv_shape_set_property(self._o,name,value)

    def set_properties(self,properties):
        """Set a GvShape properties.

        Clear all existing properties, and assign the new set passed in.

        properties -- a python dictionary with the keys being property names,
        and the result is the property value"""
        
        return _gv.gv_shape_set_properties(self._o,properties)

    def get_node(self,node=0,ring=0):
        """Fetch a node (point) as a tuple.

        node -- the node within the selected ring to return.  Defaults to zero.
        ring -- the ring containing the desired node.  Defaults to zero.

        The node is returned as an (x,y,z) tuple.  None is returned if the
        requested node is out of range."""
        return _gv.gv_shape_get_node(self._o,node,ring)
    
    def set_node(self,x,y,z=0,node=0,ring=0):
        """Set a node.

        x -- the x value to assign.
        y -- the y value to assign.
        z -- the z value to assign.
        node -- the node to set.
        ring -- the ring containing the node to set.

        Note that the node and ring will be created if not already in
        existance."""
        return _gv.gv_shape_set_node(self._o,x,y,z,node,ring)
    
    def add_node(self,x,y,z=0,ring=0):
        """Add a node.

        x -- the x value to assign.
        y -- the y value to assign.
        z -- the z value to assign.
        ring -- the ring containing the node to set.

        Note that the ring will be created if not already in
        existance.  The index of the newly created node is returned. """
        return _gv.gv_shape_add_node(self._o,x,y,z,ring)

    def get_nodes(self,ring=0):
        """Get number of nodes.

        ring -- the ring to check.  Defaults to zero.

        Note that the returned number of nodes will be zero for non-existent
        rings."""
        return _gv.gv_shape_get_nodes(self._o,ring)
    
    def get_rings(self):
        """Get number of rings.
        """
        return _gv.gv_shape_get_rings(self._o)

    def get_type(self):
        """Get shape type.

        The returned integer will match one of gview.GVSHAPE_POINT,
        gview.GVSHAPE_LINE, gview.GVSHAPE_AREA or gview.GVSHAPE_COLLECTION."""
        return _gv.gv_shape_get_type(self._o)

    def delete_ring(self, ring):
        """Delete a ring

        ring -- the ring to delete."""
        return _gv.gv_shape_delete_ring(self._o,ring)
    
    def point_in_polygon(self, x, y ):
        """Check if point in this area.

        x -- the x component of the location to check.
        y -- the y component of the location to check.
        
        Returns a non-zero value if the point (x,y) is inside this
        shapes area.  Returns zero if not, or if the current shape is not
        an area."""
        return _gv.gv_shape_point_in_polygon( self._o, x, y )

    def distance_from_polygon(self, x, y ):
        """Compute shortest distance between point and outline of polygon

        x -- the x component of the location to check.
        y -- the y component of the location to check.
        
        Returns the distance as a double."""
        return _gv.gv_shape_distance_from_polygon( self._o, x, y )
    
    def clip_to_rect(self, x, y, width, height ):
        """Clip shape to a rectangle.

        x -- the minimum x of the clip rectangle.
        y -- the minimum y of the clip rectangle.
        width -- the width of the clip rectangle.
        height -- the height of the clip rectangle.

        Creates a new GvShape which is clipped to the indicated rectangle.
        If the shape does not intersect the rectangle None is returned.  If
        it is entirely contained within the rectangle a copy is returned.
        Otherwise a copy of the shape with clipped geometry is created and
        returned.  Clipping will generally not work well for complex polygons
        with holes due to an incomplete implementation of the clipping
        algorithm.  This will be fixed at some point in the future as needed.
        """

        result = _gv.gv_shape_clip_to_rect( self._o, x, y, width, height )
        if result is None:
            return None
        else:
            return GvShape( _obj=result )

    def add_shape( self, shape ):
        _gv.gv_shape_add_shape( self._o, shape._o )

    def get_shape( self, shape_index ):
        return _gv.gv_shape_get_shape( self._o, shape_index )

    def collection_get_count( self ):
        return _gv.gv_shape_collection_get_count( self._o )
            
def gv_shape_get_count():
    return _gv.gv_shape_get_count()

def gv_shape_line_from_nodes(xlist,ylist,zlist):
    """ Create a new line shape from three lists
        of nodes.
        Inputs: xlist- x coordinates
                ylist- y coordinates
                zlist- z coordinates
        xlist, ylist, and zlist must be the same
        length.
    """
    # cast so that tuples and numeric arrays are
    # accepted
    if type(xlist) != type([1]):
        xlist=list(xlist)
    if type(ylist) != type([1]):
        ylist=list(ylist)
    if type(zlist) != type([1]):
        zlist=list(zlist)
    obj=_gv.gv_shape_line_from_nodelists(xlist,ylist,zlist)
    if obj is None:
        return None
    else:
        return GvShape(_obj=obj,type=GVSHAPE_LINE)

def gv_shapes_lines_for_vecplot(xlist,ylist,zlist,oklist):
    """ Create a new line shape from three lists
        of nodes.
        Inputs: xlist- x coordinates
                ylist- y coordinates
                zlist- z coordinates
                oklist- whether or not the coordinate
                        should be included
        xlist, ylist, zlist, and oklist must be the same
        length.
    """
    if type(xlist) != type([1]):
        xlist=list(xlist)
    if type(ylist) != type([1]):
        ylist=list(ylist)
    if type(zlist) != type([1]):
        zlist=list(zlist)
    if type(oklist) != type([1]):
        oklist=list(oklist)
    obj=_gv.gv_shapes_lines_for_vecplot(xlist,ylist,zlist,oklist)
    if obj is None:
        return None
    else:
        return GvShapes(_obj=obj)

    
###############################################################################
class GvData(_gtk.GtkData):
    """Base class for various raster and vector data containers.

    All GvDatas have a name string, common undo semantics, and changing/changed
    event notication semantics.

    Signals:

    changing -- Indicates that the underlying data is going to be changed.
    This will trigger capture of an undo memento if undo is enabled for
    this object.

    changed -- Indicates that the underlying data has changed.

    Note that the change_info for changing and changed varies depending on
    the particular type of object.  In particular, GvRaster can carry the
    modified region, and shape containing objects can have a list of shapes.
    """

    get_type = _gv.gv_data_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return

    def serialize( self, base = None, filename=None ):
        """serialize this object in a format suitable for XML representation.
        """
        
        if base is None:
            base = [gdal.CXT_Element, 'GvData']

        base.append( [gdal.CXT_Attribute, 'read_only',
                      [gdal.CXT_Text, str(self.is_read_only())]] )
        base.append( [gdal.CXT_Attribute, 'name',
                      [gdal.CXT_Text, str(self.get_name())]] )
        projection = self.get_projection()
        if  projection is not None and len(projection) > 0:
            base.append( [gdal.CXT_Element, 'Projection',
                          [gdal.CXT_Text, self.get_projection()]] )

        props = self.get_properties()

        for key in props.keys():
            if key == '_gv_add_height_portable_path':
                continue
            v = props[key]
            if key == '_gv_add_height_filename' and os.path.exists( v ):
                base.append( [gdal.CXT_Element, 'Property',
                              [gdal.CXT_Attribute, 'name',
                               [gdal.CXT_Text,
                                '_gv_add_height_portable_path']],
                              [gdal.CXT_Text, pathutils.PortablePath( v, ref_path = filename ).serialize()]] )
            base.append( [gdal.CXT_Element, 'Property',
                          [gdal.CXT_Attribute, 'name', [gdal.CXT_Text, key]],
                          [gdal.CXT_Text, v]] )
        return base

    def sink( self ):
        _gtkmissing.gtk_object_sink( self._o )
        
    def initialize_from_xml( self, tree, filename=None ):
        """Initialize this instance's properties from the XML tree
        
        Restores name, read_only, projection and all Property instances
        """
        self.set_name( gvutils.XMLFindValue( tree, 'name', self.get_name() ) )
        self.set_read_only(int(gvutils.XMLFindValue(tree, 'read_only',
                                                    str(self.is_read_only()))))
        projection = gvutils.XMLFindValue( tree, 'projection',
                                                   self.get_projection() )
        if projection is not None:
            self.set_projection( projection )

        for subtree in tree[2:]:
            if subtree[1] == 'Property':
                name = gvutils.XMLFindValue( subtree, 'name' )
                if name is not None:
                    value = gvutils.XMLFindValue( subtree, '', '' )
                    self.set_property(name, value)

    def get_name(self):
        """Fetch the name of this GvData."""
        return _gv.gv_data_get_name(self._o)
    
    def set_name(self, name):
        """Set the name of this GvData."""
        _gv.gv_data_set_name(self._o, name)
        
    def is_read_only(self):
        """Fetch the read_only flag."""
        return _gv.gv_data_is_read_only(self._o)
    
    def set_read_only(self, read_only):
        """Set the read_only flag of this GvData."""
        _gv.gv_data_set_read_only(self._o, read_only)
        
    def changed(self):
        """Emit GvData changed signal.

        Send a notification that this data has changed, with a NULL 
        change_info value."""
        _gv.gv_data_changed(self._o)

    def get_parent(self):
        """Fetch parent GvData object.

        This is typically used to get the underlying GvData on which
        a GvLayer (which is also a GvData) depends."""

        _o_parent = _gv.gv_data_get_parent(self._o)
        if _o_parent is None:
            return None
        else:
            return _gtk._obj2inst(_o_parent)

    def get_projection(self):
        """Fetch projection, if any.

        The projection is normally expressed in OpenGIS Well Known Text
        format or an empty string if no value is available."""
        
        return _gv.gv_data_get_projection(self._o)

    def set_projection(self, projection):
        """Set the projection.

        This method won't actually modify the data geometry, only the
        interpretation of the geometry."""
        _gv.gv_data_set_projection(self._o, projection)

    def get_properties(self):
        """Get GvData properties (attributes) as a dictionary.

        The properties are returned as a Python dictionary.  Note that
        changes to this dictionary are not applied back to the GvData."""
        return _gv.gv_data_get_properties(self._o)
    
    def get_property(self,name):
        """Get a GvData property.

        name -- the key or name of the property being set.  Should be a
        well behaved token (no spaces, equal signs, or colons).

        NOTE: Returns None if property does not exist."""
        
        return _gv.gv_data_get_property(self._o,name)

    def set_properties( self, properties ):
        """Set GvData properties

        Clear all existing properties, and assign the new set passed in.

        properties -- a python dictionary with the keys being property names,
        and the result is the property value"""

        return _gv.gv_data_set_properties( self._o, properties )
    
    def set_property(self,name,value):
        """Set a GvData property.

        name -- the key or name of the property being set.  Should be a
        well behaved token (no spaces, equal signs, or colons).
        
        value -- the value to be assigned.  Any text is acceptable."""
        
        return _gv.gv_data_set_property(self._o,name,value)

    def freeze(self):
        """Freeze a GvData object so that changes are not propagated
           until thawed"""
        return _gv.gv_data_freeze(self._o)

    def thaw(self):
        """Thaw a frozen GvData object"""
        return _gv.gv_data_thaw(self._o)

def gv_data_registry_dump():
    _gv.gv_data_registry_dump()
    

###############################################################################
class GvRecord:

    def __init__(self, records, rec_index ):
        self.records = records
        self.rec_index = rec_index

    def get_properties( self ):
        return self.records.get_rec_properties( self.rec_index )

    def get_typed_properties( self ):
        return self.records.get_rec_typed_properties( self.rec_index )

    def get_property( self, property_name, default_value = None ):
        properties = self.records.get_rec_properties( self.rec_index )
        if properties.has_key( property_name ):
            return properties[property_name]
        else:
            return default_value

    def set_property(self,name,value):
        field_index = self.records.fieldname_to_index( name )
        self.records.set_rec_property( self.rec_index, field_index, value )
    
    def set_properties(self,properties):
        pass
        

###############################################################################
class GvRecords(GvData):
    get_type = _gv.gv_records_get_type
    def __init__(self, name=None, _obj=None, filename=None,
                 progress_cb = None, cb_data = None ):
        if _obj:
            self._o = _obj
            self.sink()
            return

        if filename is not None:
            if gvutils.is_shapefile(filename):
                self._o = _gv.gv_records_from_dbf( filename, progress_cb, cb_data )
            else:
                self._o = _gv.gv_records_from_rec( filename, progress_cb, cb_data )
                
            if self._o is None:
                raise ValueError, 'Reading %s failed.' % filename

            self.sink()
            if name is not None:
                self.set_name(name)
            else:
                self.set_name(filename)

            # default to all fields.
            self.set_used_properties(None)
            return
            
        self._o = _gv.gv_records_new()
        if name: self.set_name(name)

    def __len__(self):
        """Return number of shapes in container."""
        return _gv.gv_records_num_records(self._o)
    
    def __getitem__(self, rec_index):
        if rec_index < 0 or rec_index >= _gv.gv_records_num_records(self._o):
            raise IndexError
        else:
            return GvRecord( self, rec_index )
        
    def __setitem__(self, index, shape):
        pass
        
    def create_records( self, count = 1 ):
        return _gv.gv_records_create_records( self._o, count )

    def fieldname_to_index( self, field_name, schema = None ):
        if schema is None:
            schema = self.get_schema()
        for i in range(len(schema)):
            if schema[i][0] == field_name:
                return i

        field_name = string.lower(field_name)
        for i in range(len(schema)):
            if string.lower(schema[i][0]) == field_name:
                return i

        return -1
    
    def set_used_properties( self, property_list ):
        schema = self.get_schema()
        index_list = []
        if property_list is not None:
            for i in range(len(property_list)):
                item = property_list[i]
                i_fld = self.fieldname_to_index( item )
                if i_fld == -1:
                    raise ValueError, 'Unknown field name:' + item
                index_list.append( i_fld )
        else:
            index_list = range(len(schema))

        _gv.gv_records_set_used_properties( self._o, index_list )


    def get_rec_typed_properties( self, record_index ):
        return _gv.gv_records_get_typed_properties( self._o, record_index )

    def get_rec_properties( self, record_index ):
        return _gv.gv_records_get_properties( self._o, record_index )

    def get_rec_property( self, record_index, field_index ):
        return _gv.gv_records_get_raw_field_data( self._o, record_index,
                                                  field_index )

    def set_rec_property( self, record_index, field_index, value ):
        if value is not None:
            value = str(value)
            
        return _gv.gv_records_set_raw_field_data( self._o, record_index,
                                                  field_index, value )

    def get_schema( self, fieldname = None ):
        prop = self.get_properties()

        schema = []
        cur_field = 1
        key_name = '_field_name_' + str(cur_field)

        while prop.has_key(key_name):
            name = prop['_field_name_'+str(cur_field)]

            if fieldname is not None \
               and string.lower(name) != string.lower(fieldname):
                cur_field = cur_field + 1
                key_name = '_field_name_' + str(cur_field)
                continue

            type = prop['_field_type_'+str(cur_field)]
            width = int(prop['_field_width_'+str(cur_field)])
            try:
                precision = int(prop['_field_precision_'+str(cur_field)])
            except:
                precision = 0

            field_schema = (name, type, width, precision)

            if fieldname is not None:
                return field_schema

            schema.append( field_schema )
                        
            cur_field = cur_field + 1
            key_name = '_field_name_' + str(cur_field)

        if fieldname is not None:
            return None
        else:
            return schema

    def get_layout( self ):
        pass

    def add_field( self, name, type = 'string', width = 0, precision = 0 ):

        """Add field to schema.

        This function will define a new field in the schema for this
        container.  The schema is stored in the GvShapes properties, and it
        used by selected functions such as the save_to() method to define
        the schema of output GIS files.

        Note that adding a field to the schema does not cause it to be
        added to all the individual GvShape objects in the container.
        However, the save_to() method will assume a default value for
        shapes missing some of the fields from the schema, so this is generally
        not an issue. 

        name -- the name of the field.  The application is expected to ensure
                this is unique within the layer.

        type -- the type of the field.  Must be one of 'integer', 'float', or
                'string'.
                
        width -- the field width.  May be zero to indicated variable width.
        
        precision -- the number of decimal places to be preserved.  Should be
                     zero for non-float field types.

        The field number of the newly created field is returned."""

        if precision != 0 and type != 'float':
            raise ValueError, 'Non-zero precision on '+type+' field '+name+' in GvShapes.add_field()'

        rft = None
        
        # GV_RFT_FLOAT
        if type == 'float':
            rft = 2

        # GV_RFT_STRING
        if type == 'string':
            rft = 3

        # GV_RFT_INTEGER
        if type == 'integer':
            rft = 1

        if rft is None:
            raise ValueError, 'Illegal field type "'+type+'" in GvRecords.add_field(), should be float, integer or string.'

        return _gv.gv_records_add_field(self._o, name, rft, width, precision )
        
    def save_to_dbf(self, filename, selection = [],
                    progress_cb = None, cb_data = None ):
        """Save records attributes to a DBF file.
        
        filename -- name of the file to save to

        selection -- list of shape indexes to write, default for all.
        """
        
        return _gv.gv_records_to_dbf( self._o, filename, selection,
                                      progress_cb, cb_data )

    def MultiStratifiedCollect( self, selection, var1, var2, strat_vars = [],
                                progress_cb = None, progress_data = None ):
        return _gv.gv_records_MultiStratifiedCollect( self._o, selection,
                                                      var1, var2, strat_vars,
                                                      progress_cb,
                                                      progress_data )

    def recode( self, single_mapping, range_mapping, srcvar, dstvar = None,
                progress_cb = None, progress_data = None ):

        if dstvar is None:
            dstvar = srcvar

        return _gv.gv_records_recode( self._o, single_mapping, range_mapping,
                                      srcvar, dstvar,
                                      progress_cb, progress_data )

###############################################################################
def GvShapesFromXML( node, parent, filename=None ):
    """construct a gvshapes object from an xml tree.

    node is the current node to instantiate from
    parent is the parent object that wants to instantiate
    this GvShapes object.

    will return the new GvShapes instance or None if something went
    horribly wrong.
    """
    
    shapes = GvShapes()

    #restore properties
    shapes.initialize_from_xml( node, filename=filename )
    
    #restore shapes
    shape_tree = gvutils.XMLFind(node, 'Shapes')
    for subtree in shape_tree[2:]:
        shape = gvutils.XMLInstantiate( subtree, parent, filename=filename )
        if shape is None:
            print 'shape is None'
        elif shape._o is None:
            print 'shape._o is None'
        else:
            shapes.append(shape)

    return shapes

class GvShapes(GvData):
    """A GvData of points, lines and areas (GvShapes). 

    This layer can be treated as a list object, where each value is
    a GvShape.

    Notes on updating Shapes:

    In order to generate proper undo information, and to ensure proper
    generation of data changing and changed events, it is illegal for
    applications to change the geometry of attributes of GvShape objects
    that are members of a GvShapes container.  If you want to change some
    aspect of a shape, it is necessary to copy it, modify the copy, and then
    apply the copy back to the GvShapes.

    eg.
      shape = shapes[45].copy()
      shape.set_property( "abc", "def" )
      shapes[45] = shape
      
    """
    
    get_type = _gv.gv_shapes_get_type
    def __init__(self, name=None, _obj=None, shapefilename=None):
        """Create a GvShapes

        name -- name to assign to GvShapes, defaults to None.
        shapefilename -- name of ESRI shapefile to create from, or None
                         (default) to create an empty container.
        """
        if _obj:
            self._o = _obj
            self.sink()
            return
        
        if shapefilename:
            self._o = _gv.gv_shapes_from_shapefile(shapefilename)
            self.sink()
            return
        
        self._o = _gv.gv_shapes_new()
        if name: self.set_name(name)
        self.sink()
        
    def __len__(self):
        """Return number of shapes in container."""
        return _gv.gv_shapes_num_shapes(self._o)
    
    def __getitem__(self, index):
        """Return an individual shape by index"""
        shp_o = _gv.gv_shapes_get_shape(self._o, index)
        if shp_o is not None:
            return GvShape(_obj=shp_o)
        else:
            if index < 0 or index >= _gv.gv_shapes_num_shapes(self._o):
                raise IndexError
            else:
                return None;
        
    def __setitem__(self, index, shape):
        """Overwrite a shape by index

        Note that this actually deletes the old shape, and the new shape
        will hereafter be referenced in the layer.  Only freestanding GvShape
        objects (not assigned to any existing GvShapes) should be assigned in
        this manner, and they will thereafter be owned by the GvShapes."""

        _gv.gv_shapes_replace_shapes(self._o, [index,], [shape._o,])
        
    def __delitem__(self, index):
        """Delete an individual shape by index"""

        _gv.gv_shapes_delete_shapes(self._o, [index,])
        
    def serialize( self, base = None, filename = None ):
        """serialize this object in a format suitable for XML representation.
        """
        if base is None:
            base = [gdal.CXT_Element, 'GvShapes']

        GvData.serialize( self, base, filename=filename )
        
        shapes = [gdal.CXT_Element, 'Shapes' ]
        for i in range(len(self)):
            if self[i] is not None:
                shapes.append(self[i].serialize( ))
        base.append( shapes )
        
        return base

    def append(self, shape):
        """Add GvShape to GvShapes. If there is an empty space in GvShapes
        (i.e. a shape has been deleted), place the new shape in it. 

        shape -- GvShape to add.

        Returns the id of the newly added shape."""
        return _gv.gv_shapes_add_shape(self._o, shape._o)

    def append_last(self, shape):
        """Add GvShape to GvShapes always at the end of list. 

        shape -- GvShape to add.

        Returns the id of the newly added shape."""
        return _gv.gv_shapes_add_shape_last(self._o, shape._o)

    def get_extents(self):
        """Fetch bounds extents of shapes.

        The extents are returned as an (xmin,ymin,xsize,ysize) tuple."""
        return _gv.gv_shapes_get_extents(self._o)

    def delete_shapes(self, shapes):
        """Delete a list of shapes

        shapes -- a list of integer shape indexes to delete

        Note the underlying GvShape objects are destroyed in addition to
        them being removed from the container."""
        
        _gv.gv_shapes_delete_shapes(self._o, shapes)

    def save_to(self, filename, type = 0):
        """Save layer to ESRI Shapefile

        Shapefiles can only hold a single geometric type.  By default this
        method will select a type based on the geometry of the first feature
        (GvShape) written, but it can be overridden with the type argument.
        The possible values are listed as SHPT_ codes in shapefil.h.
        
        filename -- name of file to save to (extension will be automatically
                    supplied)
        type -- One of the shapefile type codes, or zero to try and auto
        detect the type of file to create.  Zero is the default."""
        
        return _gv.gv_shapes_to_shapefile( filename, self._o, type )
        
    def save_to_dbf(self, filename):
        """Save shape attributes to a DBF file.
        
        filename -- name of the file to save to
        """
        
        return _gv.gv_shapes_to_dbf( filename, self._o )

    def get_change_info(self, c_object):
        """Used to convert a PyCObject as returned from a changed/changing
        signal to a python tuple.
        
        Takes a PyCObject and returns the equivalent python object.

        (change_type, num_shapes, (shape_ids))
        where change_type is defined in gvconst.py
              num_shapes is an integer
              shape_ids is a list of shape IDs"""
        
        return _gv.gv_shapes_get_change_info(c_object)

    def add_height( self, raster, offset=0.0, default_height = 0.0 ):
        """Set vertex heights from raster DEM.

        Sets the Z component of each vertex to the value sampled from
        the raster, and then adds the offset.  Values off the DEM, or
        in _nodata_ areas of the DEM are set to 0.0.  Old z coordinates
        are always lost.

        The offset is normally used to boost the vectors up a bit over any
        raster layers so they remain visible.  Usually a value on the order
        of 1/3 the size of a pixel is sufficient.

        raster -- a GvRaster from which to sample elevations, should be in
        a compatible coordinate system to the shapes.
        offset -- optional offset to apply to the vertices. """

        # Actually add the height.
        _gv.gv_shapes_add_height( self._o, raster._o, offset, default_height )

    def get_schema( self, fieldname = None ):
        """Fetch attribute schema.

        When read from GIS data sources such as shapefiles or OGR supported
        GIS formats, there will be a schema associated with a GvShapes
        grouping.  The schema is the definition of the list of attributes
        shared by all shapes in the container.  This information is stored
        in the properties of the GvShapes.  This method extracts the schema
        information in a more easily used form for Python.

        The returned schema will contain a list of tuples, with one tuple
        per attribute in the schema.  The tuples wille each contain four
        elements.

         - name: the name of the field.
         - type: the type of the field.  One of 'integer', 'float' or 'string'.
         - width: the width normally used for displaying the field, and
                  limiting storage capacity in some formats (ie. shapefiles)
         - precision: the number of decimal places preserved.  For non
                      floating point values this is normally 0.

        Optionally, a single fieldname can be given as an argument and only
        schema tuple for that field will be returned (or None if it does not
        exist).
        
        """
        prop = self.get_properties()

        schema = []
        cur_field = 1
        key_name = '_field_name_' + str(cur_field)

        while prop.has_key(key_name):
            name = prop['_field_name_'+str(cur_field)]

            if fieldname is not None \
               and string.lower(name) != string.lower(fieldname):
                cur_field = cur_field + 1
                key_name = '_field_name_' + str(cur_field)
                continue

            type = prop['_field_type_'+str(cur_field)]
            width = int(prop['_field_width_'+str(cur_field)])
            try:
                precision = int(prop['_field_precision_'+str(cur_field)])
            except:
                precision = 0

            field_schema = (name, type, width, precision)

            if fieldname is not None:
                return field_schema

            schema.append( field_schema )
                        
            cur_field = cur_field + 1
            key_name = '_field_name_' + str(cur_field)

        if fieldname is not None:
            return None
        else:
            return schema

    def get_layout( self ):
        """Get tabular layout information.

        This returns a list of field names, and their suggested width.  The
        list of field names is based on the results of get_schema(), so
        any fields not listed in the schema will be missed.  The width
        returned for each field is the maximum of the field title, and all
        the field values occuring in all shapes.

        The return result is a list of (field_name, width) tuples in the
        same order as in the schema.
        """

        schema = self.get_schema()
        name_list = []
        width_list = []
        for item in schema:
            name_list.append( item[0] )
            width_list.append( len(item[0]) )

        field_count = len(name_list)

        for rec in self:

            props = rec.get_properties()

            for i_field in range(field_count):
                try:
                    l = len(props[name_list[i_field]])
                    if l > width_list[i_field]:
                        width_list[i_field] = l
                except:
                    pass

        result = []
        for i_field in range(field_count):
            result.append( (name_list[i_field], width_list[i_field]) )

        return result

    def add_field( self, name, type = 'string', width = 0, precision = 0 ):

        """Add field to schema.

        This function will define a new field in the schema for this
        container.  The schema is stored in the GvShapes properties, and it
        used by selected functions such as the save_to() method to define
        the schema of output GIS files.

        Note that adding a field to the schema does not cause it to be
        added to all the individual GvShape objects in the container.
        However, the save_to() method will assume a default value for
        shapes missing some of the fields from the schema, so this is generally
        not an issue. 

        name -- the name of the field.  The application is expected to ensure
                this is unique within the layer.

        type -- the type of the field.  Must be one of 'integer', 'float', or
                'string'.
                
        width -- the field width.  May be zero to indicated variable width.
        
        precision -- the number of decimal places to be preserved.  Should be
                     zero for non-float field types.

        The field number of the newly created field is returned."""

        if type != 'float' and type != 'integer' and type != 'string':
            raise ValueError, 'Illegal field type "'+type+'" in GvShapes.add_field(), should be float, integer or string.'

        if precision != 0 and type != 'float':
            raise ValueError, 'Non-zero precision on '+type+' field '+name+' in GvShapes.add_field()'

        cur_schema = self.get_schema()
        new_entry = len(cur_schema) + 1
        
        self.set_property( '_field_name_'+str(new_entry), name )
        self.set_property( '_field_type_'+str(new_entry), type )
        self.set_property( '_field_width_'+str(new_entry), str(width) )
        self.set_property( '_field_precision_'+str(new_entry), str(precision))

        return new_entry

       

###############################################################################
class GvPoints(GvData):
    get_type = _gv.gv_points_get_type
    def __init__(self, name=None, _obj=None):
        if _obj: self._o = _obj; return        
        self._o = _gv.gv_points_new()
        if name: self.set_name(name)
    def __len__(self):
        return _gv.gv_points_num_points(self._o)
    def __getitem__(self, index):
        return _gv.gv_points_get_point(self._o, index)
    def append(self, point):
        return _gv.gv_points_new_point(self._o, point)

###############################################################################
class GvPolylines(GvData):
    get_type = _gv.gv_polylines_get_type
    def __init__(self, name=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_polylines_new()
        if name: self.set_name(name)
    def __len__(self):
        return _gv.gv_polylines_num_lines(self._o)
    def __getitem__(self, index):
        return _gv.gv_polylines_get_line(self._o, index)
    def append(self, line):
        return _gv.gv_polylines_new_line(self._o, line)

###############################################################################
class GvAreas(GvData):
    get_type = _gv.gv_areas_get_type
    def __init__(self, name=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_areas_new()
        if name: self.set_name(name)
    def __len__(self):
        return _gv.gv_areas_num_areas(self._o)
    def __getitem__(self, index):
        return _gv.gv_areas_get_area(self._o, index)
    def append(self, area):
        return _gv.gv_areas_new_area(self._o, area)

###############################################################################

def GvRasterFromXML( node, parent, filename=None ):
    band = int(gvutils.XMLFindValue(node,"band","1"))
    portable_path = gvutils.XMLFindValue( node, 'portable_path' )
    if portable_path is not None:
        f = pathutils.PortablePathFromXML( portable_path ).local_path( ref_path = filename )
    else:
        for child in node[2:]:
            if child[0] == gdal.CXT_Text:
                f = child[1]

    ds = manager.get_dataset( f )
    raster = manager.get_dataset_raster( ds, band )
    return raster

class GvRaster(GvData):
    """Raster data object

    Signals:
        
    geotransform-changed -- generated when the geotransform (whether
    affine or the polynomials based on gcps) changes.  Primarily used
    by the GvRasterLayer to ensure updates to mesh and display.
    """
    
    get_type = _gv.gv_raster_get_type
    def __init__(self, filename=None, dataset=None, _obj=None,
                 sample=SMSample, real=1 ):
        """Create new raster.

        All the arguments of this method are optional, and can be passed
        as keywords.
        
        filename -- name of the file to open.  It must be suitable for use
        with gdal.Open().

        dataset -- a gdal.Dataset object as returned by gdal.Open().  May
        be used as an alternative to filename.

        sample -- Method to use to compute reduced levels of detail.  Either
        gview.SMAverage (2x2 average) or gview.SMSample (decimation).

        real -- The band from the raster file to use as the band.

        """
        if _obj: self._o = _obj; return
        if (filename is None) and (dataset is None):
            raise ValueError, "expecting filename or dataset handle"

        if not (dataset is None):
            dataset_raw = dataset._o
        else:
            dataset_raw = None

        self._o = _gv.gv_raster_new(filename = filename, sample = sample,
                                    real = real, dataset = dataset_raw)
        self.sink()

    def flush_cache(self,x_off=0,y_off=0,width=0,height=0):
        """Flush data cache.

        This will cause the data caches of GDAL, and this GvRaster to be
        cleared out.  If this is being done to trigger reload, and redisplay
        of modified data on disk, then a changed signal should be emitted on
        the GvRaster instead.  This will trigger a flush automatically, and
        also invalidate displays, forcing them to be rerendered.

        x_off -- x origin of area to be flushed.
        y_off -- y origin of area to be flushed.
        width -- width of area to be flushed (zero for whole image).
        height -- height of area to be flushed (zero for whole image).
        """
        _gv.gv_raster_flush_cache(self._o,x_off,y_off,width,height)

    def get_sample(self, x, y):
        """Fetch sample value from raster.

        This function will fetch the real, or complex data value at the
        given location (in raster pixel/line coordinates).  If the result
        is real a single number is returned.  It it is complex a (real
        imaginary) tuple is returned.  If the requested point is outside
        the raster, or if the call fails for some other reason a None is
        returned.

        x -- x offset from top left corner of pixel to fetch.
        y -- y offset from top left corner of pixel to fetch."""
        
        return _gv.gv_raster_get_sample(self._o, x, y)

    def georef_to_pixel(self, x, y ):
        """Translate georeferenced coordinates to pixel/line.

        x -- X (easting or longitude) in raster layer georeferencing system.
        y -- Y (northing or latitude) in raster layer georeferencing system.

        Returns a (pixel,line) coordinate tuple on the raster."""
        
        return _gv.gv_raster_georef_to_pixel(self._o, x, y)

    def cursor_link_georef_to_pixel(self, x, y ):
        """Translate cursor/link georeferenced coordinates to pixel/line.

        x -- X (easting or longitude) in raster layer georeferencing system.
        y -- Y (northing or latitude) in raster layer georeferencing system.

        Returns a (pixel,line) coordinate tuple on the raster."""
        
        return _gv.gv_raster_georef_to_pixelCL(self._o, x, y)

    def pixel_to_georef(self, x, y ):
        """Translate pixel/line to georeferenced coordinate.

        x -- pixel on raster layer (0.0 is left side of leftmost pixel)
        y -- line on raster layer (0.0 is top side of topmost pixel)

        Returns an (x,y) coordinate tuple in the raster georeferencing
        system."""
        
        return _gv.gv_raster_pixel_to_georef(self._o, x, y)

    def cursor_link_pixel_to_georef(self, x, y ):
        """Translate pixel/line to cursor/link georeferenced coordinate.

        x -- pixel on raster layer (0.0 is left side of leftmost pixel)
        y -- line on raster layer (0.0 is top side of topmost pixel)

        Returns an (x,y) coordinate tuple in the raster georeferencing
        system defined for the cursor and link mechanism (defaults
        to the standard pixel_to_georef if no separate gcps have
        been defined for the cursor/link)."""
        
        return _gv.gv_raster_pixel_to_georefCL(self._o, x, y)

    def data_changing(self, x_off, y_off, width, height):
        """Send GvData changing signal with a raster rectangle.

        This signal indicates that a region of the raster is about to change,
        and will trigger capture of an undo memento of the region if
        undo is enabled.

        x_off -- pixel offset to top left corner of change region.
        y_off -- line offset to top left corner of change region.
        width -- width of window that is changing. 
        height -- width of window that is changing."""
        _gv.gv_raster_data_changing(self._o, x_off, y_off, width, height )
        
    def data_changed(self, x_off, y_off, width, height):
        """Send GvData changed signal with a raster rectangle.

        This signal indicates that a region of the raster has just changed,
        and will trigger invalidation of any buffered data from the
        source file, and rereading for display.
        
        x_off -- pixel offset to top left corner of change region.
        y_off -- line offset to top left corner of change region.
        width -- width of window that is changed. 
        height -- width of window that is changed."""
        _gv.gv_raster_data_changed(self._o, x_off, y_off, width, height )

    def get_change_info(self, c_object):
        """Used to convert a PyCObject as returned from a changed/changing
        signal to a python tuple.

        Returns an equivalent python tuple object to a GvRasterChangeInfo
        structure as returned by a display_changed signal.

        Returns (change_type, x_off, y_off, width, height)
           where change_type is defined in gvconst.py and the rest are integers.
        """
        return _gv.gv_raster_get_change_info(c_object)

    def get_band_number(self):
        band = self.get_band()
        dataset = self.get_dataset()
        for iband in range(dataset.RasterCount):
            test_band = dataset.GetRasterBand(iband+1)
            if test_band._o == band._o:
                return iband+1
        return -1
    
    def get_band(self):
        """Get GDAL raster band

        Fetch the band associated with the GvRaster as a
        gdal.RasterBand object.
        """
        
        band_swigptr = _gv.gv_raster_get_gdal_band(self._o)
        if band_swigptr is None:
            return None
        
        return gdal.Band(_obj=band_swigptr);
        
    def get_dataset(self):
        """Get GDAL raster dataset

        Fetch the dataset associated with the GvRaster as a
        gdal.Dataset object.
        """
        
        band_swigptr = _gv.gv_raster_get_gdal_dataset(self._o)
        if band_swigptr is None:
            return None
        
        return gdal.Dataset(_obj=band_swigptr);

    def autoscale(self, alg = ASAAutomatic, alg_param = -1.0, assign = 0):
        """Force autoscaling to be recomputed.

        alg -- Algorithm to use (see below)
        alg_param -- the parameter to the algorithm, or -1.0 to get
                     default parameter value (possibly from preferences).
        assign -- 1 to assign min/max to GvRaster or 0 to just return it.

        This method will force recomputation of scaling min/max values
        based on a sample of the data.  The algorithms collect roughly 10000
        sample points approximately at random.  Any recognised no data values
        are removed from the sample set.

        The first algorithm option is ASAPercentTailTrim, in which case
        the parameter is the percentage of the tail to exclude (0.02 for
        2%).

        The second algorithm option is ASAStdDeviation in which case
        the min/max values are based on the selected number of standard
        deviations below and above the mean of the sample.  The parameter
        value might be 1.25 to use 1.25 standard deviations on each side of
        the mean as the min/max values.

        The algorithm value ASAAutomatic can also be passed (the default)
        to determine the preferred algorithm from application preferences.

        If the autoscale() fails (for instance due to an IO error, or if all
        the sample data is the nodata value) the method will throw an
        exception otherwise a (min,max) tuple is returned.
        
        """
        return _gv.gv_raster_autoscale(self._o, alg, alg_param, assign)
    
    def get_min(self):
        """Get the minimum for default scaling

        See the autoscale() method for information on this is established."""
        return _gv.gv_raster_get_min(self._o)
        
    def get_max(self):
        """Get the maximum for default scaling
        
        See the autoscale() method for information on this is established."""
        return _gv.gv_raster_get_max(self._o)

    def force_load(self):
        """Force loading all full res data.

        All full res data for this GvRaster is forceably loaded, though
        normal cache expiration rules apply so earlier tiles may already
        be discarded as later tiles are fetched.  This is a blocking
        operation and should be use with care.  It's main purpose is to
        provide speculative "preloading" of smallish files to provide smooth
        animation effects."""

        _gv.gv_raster_force_load( self._o )
        
    def get_gcps(self):
        gcp_tuple_list = _gv.gv_raster_get_gcps(self._o)

        gcp_list = []
        for gcp_tuple in gcp_tuple_list:
            gcp = gdal.GCP()
            gcp.Id = gcp_tuple[0]
            gcp.Info = gcp_tuple[1]
            gcp.GCPPixel = gcp_tuple[2]
            gcp.GCPLine = gcp_tuple[3]
            gcp.GCPX = gcp_tuple[4]
            gcp.GCPY = gcp_tuple[5]
            gcp.GCPZ = gcp_tuple[6]
            gcp_list.append(gcp)

        return gcp_list

    def get_cursor_link_gcps(self):
        gcp_tuple_list = _gv.gv_raster_get_gcpsCL(self._o)

        gcp_list = []
        for gcp_tuple in gcp_tuple_list:
            gcp = gdal.GCP()
            gcp.Id = gcp_tuple[0]
            gcp.Info = gcp_tuple[1]
            gcp.GCPPixel = gcp_tuple[2]
            gcp.GCPLine = gcp_tuple[3]
            gcp.GCPX = gcp_tuple[4]
            gcp.GCPY = gcp_tuple[5]
            gcp.GCPZ = gcp_tuple[6]
            gcp_list.append(gcp)

        return gcp_list

    def set_gcps(self, gcp_list ):
        tuple_list = []
        for gcp in gcp_list:
            tuple_list.append( (gcp.Id, gcp.Info, gcp.GCPPixel, gcp.GCPLine,
                                gcp.GCPX, gcp.GCPY, gcp.GCPZ) )

        return _gv.gv_raster_set_gcps( self._o, tuple_list )

    def set_cursor_link_gcps(self, gcp_list, poly_order=1 ):
        tuple_list = []
        for gcp in gcp_list:
            tuple_list.append( (gcp.Id, gcp.Info, gcp.GCPPixel, gcp.GCPLine,
                                gcp.GCPX, gcp.GCPY, gcp.GCPZ) )

        return _gv.gv_raster_set_gcpsCL( self._o, tuple_list, poly_order )

    def set_poly_order_preference(self, poly_order):
        # Set preferred polynomial order for this raster (for use in
        # display).  This is only used if it is appropriate for
        # the current number of gcp's (ground control points).
        # If order is <1 or >3 it will be reset to fall within this
        # range.
        _gv.gv_raster_set_poly_order_preference(self._o, poly_order)

#def GvLayerFromXML( node, parent, filename=None ):
#    band = int(gvutils.XMLFindValue(node,"band","1"))
#    for child in node[2:]:
#        if child[0] == gdal.CXT_Text:
#            filename = child[1]

#    ds = manager.get_dataset( filename )
#    raster = manager.get_dataset_raster( ds, band )
#    return raster

###############################################################################
class GvLayer(GvData):
    """Base class for display layers.

    Signals:

    setup -- called when the layer is being setup.  Internal use. 

    teardown -- called when the layer is being destroyed.  Internal use.

    draw -- called after normal drawing is complete on the layer.  Gives tools
    an opportunity to draw layer specific overlays.

    get-extents -- called to fetch extents of layer.  Takes a GvRect as an
    argument (not clear to me why this is a signal).

    display-change -- called to indicate a display property (colour,
    interpolation method, etc) of this layer has changed.  Triggers redraw.
    """
    
    get_type = _gv.gv_layer_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return

    def serialize( self, base = None, filename=None ):
        if base is None:
            base = [gdal.CXT_Element, 'GvLayer']

        base.append( [gdal.CXT_Attribute, 'visible',
                      [gdal.CXT_Text, str(self.is_visible())]] )

        GvData.serialize( self, base, filename=filename )

        return base

    def initialize_from_xml( self, tree, filename=None ):
        """restore object properties from XML tree
        """
        GvData.initialize_from_xml( self, tree, filename=filename )
        self.set_visible( int(gvutils.XMLFindValue( tree, 'visible',
                                                    str(self.is_visible()))))
        
    def is_visible(self):
        """Check if layer is visible.

        Returns a non-zero value if the layer is currently visible.
        """
        return _gv.gv_layer_is_visible(self._o)
    
    def set_visible(self, visible):
        """Set layer visibility.

        visible -- 0 for invisible, and non-zero for visible.
        """
        _gv.gv_layer_set_visible(self._o, visible)
        
    def extents(self):
        """Return extents of layer.

        The extents are returned as a tuple (xmin,ymin,width,height)."""
        return _gv.gv_layer_extents(self._o)

    def reproject(self, projection):
        """Attempt to change view projection.

        projection -- the projection string in OpenGIS Well Known Text format.
        
        Currently this only works for rasters, but eventually it will
        modify the display projection of any kind of GvLayer.

        Returns 0 on failure, or non-zero on success."""
        return _gv.gv_layer_reproject(self._o, projection)

    def launch_properties(self):
        """Launch a properties panel for this layer.

        Returns the dialog object, or None if none can be created."""
        return None

    def display_change(self):
        """Send a display property notification."""
        _gv.gv_layer_display_change(self._o)

    def get_view(self):
        """Fetch the GvViewArea this layer is on."""

        _o_view = _gv.gv_layer_get_view( self._o )
        if _o_view is None:
            return None
        else:
            return _gtk._obj2inst(_o_view)

    def classify(self):
        from gvclassification import GvClassification
        from gvclassifydlg import GvClassificationDlg

        classification = GvClassification(self)
        classifyier = GvClassificationDlg(classification)
        classifyier.show()
        
    def show_legend(self):
        from gvclassification import GvClassification
        import gvlegenddlg
        
        cls = GvClassification(self)
        if cls.count > 0:
            gvlegenddlg.show_legend( self )

    def refresh( self ):
        """Refresh from view of layer as required by layer type."""
        pass

###############################################################################
class GvShapeLayer(GvLayer):
    """Display layer of vector shape objects.

    Signals:

    selection-changed -- This signal is emitted when the selection for the
    layer has changed (including clearing the selection).  Use get_selected()
    to get the current selection list.

    subselection-changed -- This signal is emitted when the subselection
    (the focus shape within the current selection) changes.  Note that a
    subselection-changed signal is usually generated on selection changes,
    as well as subselection changes.
    
    This class has many other signals, but they are mostly for internal
    implementation of selection, editing and so forth.

    """
    get_type = _gv.gv_shape_layer_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return

    def serialize(self, base, filename=None ):
        """serialize this object in a format suitable for XML representation.

        Adds properties for the current selection
        """

        if base is None:
            base = [gdal.CXT_Element, 'GvShapeLayer']

        GvLayer.serialize( self, base, filename=filename )
                
    def initialize_from_xml( self, tree, filename=None ):
        """initialize this object from the XML tree
        """

        GvLayer.initialize_from_xml( self, tree, filename=filename )
        
    def set_color(self, color):
        """Set the drawing color.

        This method is deprecated.
        """
        _gv.gv_shape_layer_set_color(self._o, color)

    def pick_shape( self, view, x, y ):
        """
        """
        return _gv.gv_shape_layer_pick_shape( self._o, view._o, x, y )

    def get_selected(self):
        """Get list of currently selected objects.

        The list of shape id's is returned as a list. 
        """
        return _gv.gv_shape_layer_get_selected(self._o)

    def get_subselected(self):
        """Get current subselection.

        Returns the shape id of the current subselection.  The subselection
        is the one shape out the current set of selected shapes that has
        special focus of attention from the user.  The return value will be
        -1 if there is no subselection ... generally because there is no
        selection."""
        
        return _gv.gv_shape_layer_get_subselection(self._o)

    def subselect_shape(self, shape_id):
        """Change the subselection.

        shape_id -- the new subselection. This may be -1, otherwise it must
        be in the current selected shape set.
        """
        _gv.gv_shape_layer_subselect_shape( self._o, shape_id )

    def clear_selection(self):
        """Clear selection

        Clear the current shape selection for this layer, sending a
        selection-changed signal if there was anything selected."""

        _gv.gv_shape_layer_clear_selection(self._o)

    def select_all(self):
        """Select all shapes in layer

        All shapes in the layer are marked as selected, and if this is a
        change, a selection-changed signal is sent."""

        _gv.gv_shape_layer_select_all(self._o)

    def select_shape(self,shape_id):
        """Add a shape to selection

        Adds the indicated shape to the current selection, triggering a
        selection-changed signal if that shape wasn't previously selected.
        The existing selection should be cleared explicitly with
        clear_selection() if you only want the new shape select.

        Nothing will happen if the shape is already selected.

        shape_id -- the id (index) of the shape to be selected."""

        _gv.gv_shape_layer_select_shape(self._o,shape_id)

    def deselect_shape(self,shape_id):
        """Remove shape from selection

        Removes the indicated shape from the current selection, triggering a
        selection-changed signal if that shape was previously selected.

        shape_id -- the id (index) of the shape to be deselected."""

        _gv.gv_shape_layer_deselect_shape(self._o, shape_id)

    def set_selection_mode(self,mode=0,clear=1):
        """Set selection mode

        mode=0:  multiple selection (default)
        mode=1:  single selection

        clear=0: do not clear existing selections before changing mode
        clear=1: clear existing selections before changing mode (default)
        
        """
        if clear == 1:
            self.clear_selection()
            self.display_change()

        if mode == 1:
            self.set_property("selection_mode","single")
        else:
            self.set_property("selection_mode","multiple")


###############################################################################
def GvShapesLayerFromXML( base, parent, filename=None ):
    """Create a GvShapesLayer from an XML tree

    Look for a GvShapes tree and use it to build the GvShapes object if
    possible.  Otherwise, look for the _filename propery and use it.  If
    neither is found, the layer will not have any shapes.
    
    Returns a new GvShapesLayer or None if it failed
    """
    shape_tree = gvutils.XMLFind( base, 'GvShapes' )
    if shape_tree is not None:
        shapes = gvutils.XMLInstantiate( shape_tree, None, filename=filename )
    else:
        portable_path = gvutils.XMLFindValue( base, 'portable_path' )
        if portable_path is not None:
            shapefilename = pathutils.PortablePathFromXML( portable_path ).local_path( ref_path = filename )
        else:
            shapefilename = gvutils.XMLFindValue( base, "_filename" )
            if shapefilename is None:
                shapes = None
        if shapefilename is not None:
            shapes = GvShapes( shapefilename = shapefilename )

    layer = GvShapesLayer( shapes = shapes )

    if layer is not None:
        layer.initialize_from_xml( base, filename=filename )

    return layer

class GvShapesLayer(GvShapeLayer):
    """Vector Display Layer

    The following properties have special interpretation for a GvShapesLayer.
    Note that modifying these properties does not automatically trigger a
    display-change signal ... please call display_change() manually.

    _point_color -- RGBA value used for point color.
    
    _point_size -- Size of point cross hairs in screen pixels.
    
    _line_color -- RGBA value used for line color.
    
    _area_edge_color -- RGBA value used for area edge drawing.  Set alpha to
    zero to skip drawing edges.
    
    _area_fill_color -- RGBA value used for area filling.  Set alpha to zero
    to skip drawing fill.

    Note that the above property values can also be set on individual
    shapes to override drawing style on a per-shape basis.
    """
    get_type = _gv.gv_shapes_layer_get_type

    def __init__(self, shapes=None, _obj=None):
        if _obj: self._o = _obj; return
        if shapes != None: shapes = shapes._o
        self._o = _gv.gv_shapes_layer_new(shapes)
        self.sink()

    def serialize( self, base = None, filename=None ):
        """Create a representation of this object suitable for XMLing.
        """
        if base is None:
            base = [gdal.CXT_Element, "GvShapesLayer"]

        layer_props = self.get_properties()
        shapes = self.get_parent()
        if shapes is not None:
            shape_props = shapes.get_properties()
            if (layer_props.has_key('_serialize_shapes') and \
                layer_props['_serialize_shapes'] == '1') \
                or not shape_props.has_key('_filename'):
                base.append( shapes.serialize( filename=filename ) )
            elif shape_props.has_key('_filename'):
                v = shape_props['_filename']
                if os.path.exists( v ):
                    base.append( [gdal.CXT_Attribute, 'portable_path',
                                  [gdal.CXT_Text, pathutils.PortablePath( v, ref_path = filename ).serialize()]] )
                base.append( [gdal.CXT_Attribute, '_filename',
                              [gdal.CXT_Text, v]] )

        # Do we have a symbol manager?

        sm = self.get_symbol_manager(0)
        if sm is not None:
            base.append( sm.serialize() )
            
        #serialize the base class properties (all the way to GvData)
        GvShapeLayer.serialize( self, base, filename=filename )

        return base
        
    def launch_properties(self):
        import gvvectorpropdlg
        return gvvectorpropdlg.LaunchVectorPropDialog( self )

    def get_symbol_manager( self, ok_to_create = 0 ):
        _sm = _gv.gv_shapes_layer_get_symbol_manager( self._o, ok_to_create )
        if _sm is None:
            return None
        else:
            return GvSymbolManager( _obj = _sm )

    def initialize_from_xml( self, tree, filename=None ):
        """initialize this object from the XML tree
        """

        # Initialize GvSymbolManager.
        
        sm_xml = gvutils.XMLFind( tree, 'GvSymbolManager' )
        if sm_xml is not None:
            sm = self.get_symbol_manager( 1 )
            sm.initialize_from_xml( sm_xml, filename=filename )

        GvShapeLayer.initialize_from_xml( self, tree, filename=filename )
        
###############################################################################
class GvPointLayer(GvShapeLayer):
    get_type = _gv.gv_point_layer_get_type
    def __init__(self, points=None, _obj=None):
        if _obj: self._o = _obj; return
        if points != None: points = points._o
        self._o = _gv.gv_point_layer_new(points)

###############################################################################
class GvLineLayer(GvShapeLayer):
    get_type = _gv.gv_line_layer_get_type
    def __init__(self, plines=None, _obj=None):
        if _obj: self._o = _obj; return
        if plines != None: plines = plines._o
        self._o = _gv.gv_line_layer_new(plines)

###############################################################################
class GvAreaLayer(GvShapeLayer):
    get_type = _gv.gv_area_layer_get_type
    def __init__(self, areas=None, _obj=None):
        if _obj: self._o = _obj; return
        if areas != None: areas = areas._o
        self._o = _gv.gv_area_layer_new(areas)

###############################################################################
def GvPqueryLayerFromXML( base, parent, filename=None ):
    shape_tree = gvutils.XMLFind( base, 'GvShapes' )
    if shape_tree is not None:
        shapes = gvutils.XMLInstantiate( shape_tree, None, filename=filename )
    else:
        portable_path = gvutils.XMLFindValue( base, 'portable_path' )
        if portable_path is not None:
            shapefilename = pathutils.PortablePathFromXML( portable_path ).local_path( ref_path = filename )
        else:
            shapefilename = gvutils.XMLFindValue( base, "_filename" )
            if shapefilename is None:
                shapes = None
        if shapefilename is not None:
            shapes = GvShapes( shapefilename = shapefilename )

    layer = GvPqueryLayer( shapes = shapes )

    if layer is not None:
        layer.initialize_from_xml( base, filename=filename )

    return layer

class GvPqueryLayer(GvShapesLayer):
    """Point Query Layer

    This layer is intended to only hold points, but this isn't strictly
    enforced.  For each point in this layer, coordinate and/or raster
    values are displayed beside the point. 

    The following properties have special interpretation for a GvPqueryLayer.
    Note that modifying these properties does not automatically trigger a
    display-change signal ... please call display_change() manually.

    _point_color -- RGBA value used for point and text color.
    
    _point_size -- Size of point cross hairs in screen pixels

    _pixel_mode -- One of "off" or "on" indicating if pixel raster values
    should be displayed for each query point.
    
    _coordinate_mode -- One of "off", "raster", "georef", or "latlong"
    indicating what coordinate system the coordinates should be displayed in
    (or skipped for off). 
    
    Note that the above property values can also be set on individual
    shapes to override drawing style on a per-shape basis.
    """
    get_type = _gv.gv_pquery_layer_get_type
    def __init__(self, shapes=None, _obj=None):
        if _obj: self._o = _obj; return
        if shapes != None: shapes = shapes._o
        self._o = _gv.gv_pquery_layer_new( shapes )
        self.sink()

    def launch_properties(self):
        import gvpquerypropdlg
        return gvpquerypropdlg.LaunchPQueryPropDialog( self )

    def serialize( self, base = None, filename=None ):
        """Create a representation of this object suitable for XMLing.
        """
        if base is None:
            base = [gdal.CXT_Element, "GvPqueryLayer"]

        #serialize the base class properties
        GvShapesLayer.serialize( self, base, filename=filename )

        return base
        
###############################################################################
class IpGcpLayer(GvShapesLayer):
    get_type = _gv.ip_gcp_layer_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.ip_gcp_layer_new()
        self.sink()

###############################################################################
class AppCurLayer(GvShapesLayer):
    get_type = _gv.app_cur_layer_get_type
    def __init__(self, _obj=None, shapes=None):
        if _obj: self._o = _obj; return
        if shapes is not None:
            shapes = shapes._o
        self._o = _gv.app_cur_layer_new(shapes)
        self.sink()

###############################################################################
def GvRasterLayerFromXML( node, parent, filename=None ):
    prototype_node = gvutils.XMLFind( node, 'Prototype' )
    if prototype_node is not None:
        prototype_data = GvRasterFromXML( prototype_node, None,
                                          filename=filename )
    else:
        prototype_data = None

    rl_mode = int(gvutils.XMLFindValue( node, 'mode', str(RLM_AUTO) ))
    mesh_lod = gvutils.XMLFindValue( node, 'mesh_lod', '0' )

    layer = GvRasterLayer( raster = prototype_data, rl_mode = rl_mode,
                           creation_properties = [('mesh_lod',mesh_lod)] )
    layer.initialize_from_xml( node, filename=filename )

    sources_min_max = []
    for child in node[2:]:
        if child[0] == gdal.CXT_Element and child[1] == 'Source':
            raster = GvRasterFromXML( child, None, filename=filename )
            isource = int(gvutils.XMLFindValue(child,"index","0"))
            min = float(gvutils.XMLFindValue(child,"min","0"))
            max = float(gvutils.XMLFindValue(child,"max","0"))
            sources_min_max.append([min, max])
            const_value = int(gvutils.XMLFindValue(child,"const_value","0"))
            nodata = gvutils.XMLFindValue( child, "nodata", None )
            nodata = eval(gvutils.XMLFindValue(child, "nodata", "None"))

            layer.set_source( isource, raster, min = min, max = max,
                              const_value = const_value, nodata = nodata )
        else:
            raster = None

    stretch = layer.get_property( 'last_stretch' )
    if stretch is not None:
	exec 'func = layer.' + stretch + '()'

    # Warning !!! stretch functions generally reset min/max with autoscale for
    # each source, so we have to reset them to the good values...
    for i in range(layer.sources):
        layer.min_set( i, sources_min_max[i][0] )
        layer.max_set( i, sources_min_max[i][1] )

    # Set classification? 
    
    from gvclassification import GvClassification
    cls = GvClassification( layer )
    if cls.count > 0:
        cls.update_all_layers()

    # Set elevations?
    f = layer.get_property( '_gv_add_height_portable_path' )
    if f is None:
        f = layer.get_property( '_gv_add_height_filename' )
    else:
        f = pathutils.PortablePathFromXML( f ).local_path( ref_path = filename )
    if f is not None:
        ds = manager.get_dataset( f )
        dem_raster = manager.get_dataset_raster(
            ds, int(layer.get_property( '_gv_add_height_band' )) )
        layer.add_height( dem_raster,
                          float(layer.get_property( '_gv_add_height_default')))

    return layer

class GvRasterLayer(GvLayer):
    get_type = _gv.gv_raster_layer_get_type
    def __init__(self, raster=None, creation_properties=None, _obj=None,
                 rl_mode = RLM_AUTO ):
        """Create a raster layer.

        raster -- the primary GvRaster to which this layer is tied.  It
        will be the GvData parent of this layer, and will be used to establish
        georeferencing, and other information.   Internally this is known
        as the ``prototype-data''.

        creation-properties -- A list of (name, value) tuples with special
        creation options.  Currently the only supported one is ('raw','yes')
        to avoid using affine or gcp based georeferencing information from
        the GvRaster.

        rl_mode -- One of the RLM modes (documented in get_mode()), or
        gview.RLM_AUTO meaning the layer type should be deduced from the
        passed GvRaster (the default).
        """
        if _obj:
            self._o = _obj
        else:
            if raster is None:
                raise ValueError, "expecting GvRaster instance"
            if creation_properties is None:
                self._o = _gv.gv_raster_layer_new(raster._o, rl_mode)
            else:
                self._o = _gv.gv_raster_layer_new(raster._o, rl_mode,
                                                  creation_properties)

        self.sink()
        
        # Note: we don't want to include alpha in self.sources as it should
        # not be enhanced.
        if self.get_mode() == RLM_SINGLE:
            self.sources = 1
        elif self.get_mode() == RLM_COMPLEX:
            self.sources = 1
        else:
            self.sources = 3

    def serialize(self, layer = None, filename=None ):
        if layer is None:
            layer = [gdal.CXT_Element, 'GvRasterLayer']
            
        layer.append( [CXT_Attribute, 'mode',
                       [CXT_Text, str(self.get_mode())]] )

        layer.append( [CXT_Attribute, 'mesh_lod',
                       [CXT_Text, str(self.get_mesh_lod())]] )

        GvLayer.serialize( self, layer, filename=filename )

        source_count = self.sources
        prototype_raster = None
        for isource in range(source_count):
            if prototype_raster is None:
                raster = self.get_data(isource)
                if raster is not None:
                    prototype_raster = raster

        if prototype_raster is not None:
            v = raster.get_dataset().GetDescription()
            proto = [gdal.CXT_Element, 'Prototype',
                     [gdal.CXT_Attribute, 'band', 
                      [gdal.CXT_Text, str(raster.get_band_number())]]]
            if os.path.exists( v ):
                proto.append( [gdal.CXT_Attribute, 'portable_path', 
                               [gdal.CXT_Text, pathutils.PortablePath( v, ref_path=filename ).serialize()]] )
            proto.append( [gdal.CXT_Text, v] )
            layer.append( proto )

        # Note that self.sources isn't necessary all the sources.  
        for isource in range(source_count):
            src = [gdal.CXT_Element, 'Source',
                   [gdal.CXT_Attribute, 'index',
                    [gdal.CXT_Text, str(isource)]],
                   [gdal.CXT_Attribute, 'min',
                    [gdal.CXT_Text, str(self.min_get(isource))]],
                   [gdal.CXT_Attribute, 'max',
                    [gdal.CXT_Text, str(self.max_get(isource))]]
                   ]

            if self.nodata_get(isource) != -100000000.0:
                src.append( [gdal.CXT_Attribute, 'nodata',
                             [gdal.CXT_Text, str(self.nodata_get(isource))]] )
                
            raster = self.get_data(isource)
            if raster is None:
                src.append( [gdal.CXT_Attribute, 'constant',
                             [gdal.CXT_Text, str(self.get_const_value(isource))]] )
            else:
                src.append( [gdal.CXT_Attribute, 'band',
                             [gdal.CXT_Text, str(raster.get_band_number())]] )
                v = raster.get_dataset().GetDescription()
                if os.path.exists( v ):
                    src.append( [gdal.CXT_Attribute, 'portable_path', 
                                 [gdal.CXT_Text, pathutils.PortablePath( v, ref_path=filename ).serialize()]] )
                src.append( [gdal.CXT_Text, v] )

            layer.append( src )

        return layer

    def view_to_pixel(self, x, y ):
        """Translate view coordinates to pixel/line.

        x -- X (easting or longitude) in view georeferencing system.
        y -- Y (northing or latitude) in view georeferencing system.

        Returns a (pixel,line) coordinate tuple on the raster."""
        
        return _gv.gv_raster_layer_view_to_pixel(self._o, x, y)

    def pixel_to_view(self, x, y ):
        """Translate pixel/line to view coordinate.

        x -- pixel on raster layer (0.0 is left side of leftmost pixel)
        y -- line on raster layer (0.0 is top side of topmost pixel)

        Returns an (x,y) coordinate tuple in the view georeferencing
        system."""
        
        return _gv.gv_raster_layer_pixel_to_view(self._o, x, y)

    def get_mode(self):
        """Fetch the GvRasterLayer display mode.

        It will be one of gview.RLM_SINGLE (greyscale or pseudocolored
        raster band), gview.RLM_RGBA (RGBA composite from individual GvRaster
        bands), or gview.RLM_COMPLEX (complex GvRaster pseudocolored with 2D
        lookup table)."""
        return _gv.gv_raster_layer_get_mode(self._o);

    def get_mesh_lod(self):
        return _gv.gv_raster_layer_get_mesh_lod(self._o)
        
    def get_data(self, isource=0):
        """Fetch the GvRaster for a source.

        Note that gview.RLM_SINGLE mode has one source (isource=0),
        gview.RLM_COMPLEX has one source, and gview.RLM_RGBA has four (red,
        green, blue and alpha).  Any source may be None indicating that
        that source will use the constant value (see get_const_value()).

        isource -- the source index (from 0 to 3).  

        """

        data = _gv.gv_raster_layer_get_data(self._o, isource)
        if data is not None:
            return _gtk._obj2inst(data)
        else:
            return None
        
    def source_get_lut(self, isource=0):
        """Fetch the lut for a source

        This fetches the pre-compositing lut applied to a source.  It
        will be None (if there isn't any in effect), or a String of 256
        values between 0 and 255.  Source lut's can only be set with
        GvRasterLayer.set_source().
        
        isource -- the source to fetch from."""
        return _gv.gv_raster_layer_source_get_lut(self._o, isource);

    def get_nodata(self, isource):
	"""Fetch NODATA value. DEPRECATED: use nodata_get()."""
        return _gv.gv_raster_layer_get_nodata( self._o, isource )
        
    def set_source(self, isource, data, min=None, max=None, const_value=0,
                   lut=None, nodata=None):
        """Set a data source

        Sets all the configuration information for one of the data sources
        of a layer.  This method will trigger a display-change signal if
        any values are altered.

        isource -- the source index (from 0 to 3)

        data -- a GvRaster, or None if the source should be constant valued.

        min -- the minimum value to use for scaling this raster to the
        range 0-255.  If min and max are defaulted they will be extracted
        from the raster. 

        max -- the maximum value to use for scaling this raster to the
        range 0-255.  If min and max are defaulted they will be extracted
        from the raster.

        const_value -- Constant value to use in place of data if data is None.

        lut -- Pre-compositing lookup table or None.  If passed it must be
        a string of exactly 256 characters mapping input values to output
        values in the range 0-255. 
        """

        if data is None:
            data_o = None
        else:
            data_o = data._o
	
	if (min is None) and (data is not None):
	    min = data.get_min()
	
	if (max is None) and (data is not None):
	    max = data.get_max()

        if( self.get_property("_scale_lock") is not None and 
            self.get_property("_scale_lock") == "locked" ) :
            
            if( self.get_property("_scale_limits") is not None ) : 
                min, max = map \
                ( string.atof, 
                  string.split(self.get_property("_scale_limits"))
                )

        return _gv.gv_raster_layer_set_source(self._o, isource, data_o,
                                              min, max, const_value, lut,
                                              nodata )
        
    def alpha_set(self, alpha_mode, alpha_check_val):
        return _gv.gv_raster_layer_alpha_set(self._o, alpha_mode, alpha_check_val)

    def alpha_get(self):
        return _gv.gv_raster_layer_alpha_get( self._o )

    def min_set(self,isource,min):
        """Set the scaling minimum.

        This will trigger a redraw via the display-change signal if it
        changes the scaling value.

        isource -- the source index (from 0 to 3).
        min -- new minimum value for scaling.
        """
        return _gv.gv_raster_layer_min_set(self._o, isource, min )

    def min_get(self,isource):
        """Fetch the scaling minimum."""
        return _gv.gv_raster_layer_min_get(self._o,isource)

    def max_set(self,isource,max):
        """Set the scaling maximum.

        This will trigger a redraw via the display-change signal if it
        changes the scaling value.

        isource -- the source index (from 0 to 3).
        max -- new maximum value for scaling.
        """
        return _gv.gv_raster_layer_max_set(self._o, isource, max)

    def max_get(self,isource):
        """Fetch the scaling maximum."""
        return _gv.gv_raster_layer_max_get(self._o,isource)

    def nodata_set(self,isource,real,imaginary):
        """Set the NODATA value.

        This will trigger a redraw via the display-change signal if it
        changes the NODATA value.

        isource -- the source index (from 0 to 3).
        nodata -- new nodata value.
        """
        return _gv.gv_raster_layer_nodata_set(self._o,isource,real,imaginary)

    def nodata_get(self,isource):
        """Fetch the NODATA value."""
	return _gv.gv_raster_layer_nodata_get(self._o,isource)

    def type_get(self,isource):
        """Fetch GDAL type of the raster object."""
	return _gv.gv_raster_layer_type_get(self._o,isource)

    def get_const_value(self,isource):
        """Fetch source constant value"""
        return _gv.gv_raster_layer_get_const_value(self._o,isource)

    def zoom_set(self,mag_mode,min_mode):
        """Set interpolation method

        I believe mag_mode sets the interpolation mode when zooming in past
        1:1 on a texture, and min_mode is the interpolation mode used for
        downsampling from the texture, but I am not sure.  Both default to
        bilinear, and are normally changed together.
        
        mag_mode -- One of gview.RL_FILTER_BILINEAR or gview.RL_FILTER_NEAREST.
        min_mode -- One of gview.RL_FILTER_BILINEAR or gview.RL_FILTER_NEAREST.
        """
        return _gv.gv_raster_layer_zoom_set( self._o, mag_mode, min_mode )

    def zoom_get(self):
        """Fetch zoom mode

        Returns the mag_mode, and min_mode interploation modes as a tuple.
        See also: zoom_set()"""
        
        return _gv.gv_raster_layer_zoom_get(self._o)

    def texture_clamp_set(self,s_mode,t_mode):
        return _gv.gv_raster_layer_texture_clamp_set(self._o, mag_mode, min_mode )

    def texture_mode_set(self,texture_mode,color):
        """Set the texture mode.

        The default mode is replace in which case the fragment color is
        ignored.  In modulate mode the raster is modulated with the
        provided fragment color.
        
        texture_mode -- gview.RL_TEXTURE_REPLACE or gview.GL_TEXTURE_MODULATE
        color -- fragment color as an RGBA tuple."""
        return _gv.gv_raster_layer_texture_mode_set(self._o, texture_mode,
                                                    color )

    def texture_mode_get(self):
        return _gv.gv_raster_layer_texture_mode_get(self._o)

    def blend_mode_set(self,mode,sfactor=0,dfactor=0):
        """Set blend mode

        mode -- 0=off, non-0=on
        sfactor -- ...
        dfactor -- ..."""
        
        return _gv.gv_raster_layer_blend_mode_set(self._o, mode, sfactor, dfactor )

    def blend_mode_get(self):
        return _gv.gv_raster_layer_blend_mode_get(self._o)

    def lut_put(self,lut=None):
        """Set the lut.

        This method will reset the compositing lut on a rasterlayer.  The lut
        should be a string of 1024 bytes for a 1D LUT and 262144 bytes (as a
        String) for a 2D LUT.  The array should be stored in "RGBARGBA..."
        format.

        2D LUTs should only be applied to layers in RLM_COMPLEX mode, and
        1D LUTs should only be applied to layers in RLM_SINGLE mode.  It is
        an error to apply luts in any other case. 

        lut -- the lut to set, stored as a string.  None may be used to
               clear the lut.
        """
        return _gv.gv_raster_layer_lut_put(self._o, lut)

    def lut_get(self, rgba_complex=0):
        """Fetch the lut.

        The returned lut will be a string of 1024 bytes if 1D, or 262144 bytes
        if the lut is 2D.  The data is stored in "RGBARGBA..." format.

        The rgba_complex variable is used to determine whether the
        real or complex lut should be returned in the rgba case (this
        mode supports both real and complex data).  Use 0 for real
        (default for backwards compatibility), 1 for complex.  This
        variable was added in case complex and real data are mixed within
        a given RGBA layer, to allow access to either lut.  If mixed
        real/complex data are never going to be permitted, or if real
        data within an RGBA layer never has an associated lut, rgba_complex
        should probably be removed again and the type of lut returned should
        be based on whether the first source of the layer contains real or
        complex data.
        """
        return _gv.gv_raster_layer_lut_get(self._o, rgba_complex)

    def lut_type_get(self):
        """Fetch the LUT type.

        Returns one of RL_LUT_NONE, RL_LUT_1D, or RL_LUT_2D (defined in
        gvconst.py)."""
        return _gv.gv_raster_layer_lut_type_get( self._o )

    def lut_color_wheel_new(self,h_mode,h_param,s_mode,s_param,v_mode,v_param):
        """Generate 2D LUT

        Returns a lut suitable for applying to a RLM_COMPLEX layer with the
        lut_put() method.  See gvrasterpropdlg.py for an example of use of
        this method. 

        h_mode -- one of the RL_LUT_* values indicating the source of the hue
        component of the HLS color.

        h_param -- if h_mode is RL_LUT_SCALAR this should be the constant hue
        value between 0.0 and 1.0. 
        
        s_mode -- one of the RL_LUT_* values indicating the source of the 
        saturation component of the HLS color.

        s_param -- if s_mode is RL_LUT_SCALAR this should be the constant 
        saturation value between 0.0 and 1.0. 
        
        v_mode -- one of the RL_LUT_* values indicating the source of the value
        component of the HLS color.

        v_param -- if v_mode is RL_LUT_SCALAR this should be the constant value
        value between 0.0 and 1.0.
        """
        return _gv.gv_raster_layer_lut_color_wheel_new(self._o,h_mode,h_param,
                                                       s_mode,s_param,
                                                       v_mode,v_param)

    def lut_color_wheel_new_ev(self,set_phase=1, set_magnitude=1):
        """Generate 2D LUT

        Applies a lut suitable for an RLM_COMPLEX layer with the
        lut_put() method.  See gvrasterpropdlg.py for an example of use of
        this method.   This method is similar to lut_color_wheel_new()
        but is simplified and computes the 2D LUT based on looking up
        within a standard phase color table (from EV) and using magnitude
        to modulate the color.

        set_phase -- One if varying phase is to be used to lookup the color
        in a color table, or zero to use a fixed color of white.

        set_magnitude -- One if magnitude is to be used to modify the
        intensity of the selected color, or zero to use a constant magnitude
        factor of 1.0.
        
        """
        return _gv.gv_raster_layer_lut_color_wheel_new_ev(self._o,
                                                          set_phase,
                                                          set_magnitude)

    def lut_color_wheel_1d_new( self, s=1.0, v=1.0, offset=0.0 ):
        return _gv.gv_raster_layer_lut_color_wheel_1d_new( self._o,s,v,offset)

    def autoscale_view(self, alg = ASAAutomatic, alg_param = -1.0, isource=0 ):
        """Force autoscaling to be recomputed.

        alg -- Algorithm to use (see below)
        alg_param -- the parameter to the algorithm, or -1.0 to get
                     default parameter value (possibly from preferences).
        isource -- the GvRaster to get scaling for

        This method will compute of scaling min/max values based on a sample
        of the data in the current view for the selected source raster.  The
        algorithm information is the same as GvRaster.autoscale().
        
        If the autoscale_view() method fails (for instance due to an IO error,
        or if all the sample data is the nodata value) the method will throw an
        exception otherwise a (min,max) tuple is returned.
        
        """
        return _gv.gv_raster_layer_autoscale_view(self._o, alg, alg_param,
                                                  isource)

    def autoscale( self, alg = ASAAutomatic, alg_param = -1.0, isource=0,
                   viewonly = 0):
        if viewonly == 0:
            raster = self.get_data(isource)
            if raster is None:
                return (self.min_get(isource), self.max_get(isource))
            else:
                return raster.autoscale(alg, alg_param)

        else:
            try:
                return self.autoscale_view(alg, alg_param, isource)
            except:
                return (self.min_get(isource), self.max_get(isource))
        
    def histogram_view(self, isource = 0, scale_min = 0.0, scale_max = 255.0,
                       hist_size = 256 ):
        """Compute histogram of viewed pixels.

        isource -- the GvRaster to collect histogram from.
        scale_min -- the min value to use when scaling to histogram buckets.
        scale_max -- the max value to use when scaling to histogram buckets.
        hist_size -- the number of histogram buckets to divide the range into.

        This method will attempt to collect all the pixels in the current
        view into a histogram.  Note that all pixels values are read only from
        the GvRaster cache (for speed), so missing tiles or tiles only
        available at reduced levels of detail will be underrepresented.

        In 2D the sampling identification of raster pixels should be exact
        for unrotated and unwarped images, otherwise it will be based on the
        bounding rectangle and so will include some extra pixels outside the
        view.  In 3D all tiles which appear to intersect the view will be
        sampled, so potentially many pixels outside the view will be included
        in the histogram.

        The function returns a list object with histogram entry counts of
        size hist_size, or an exception in the case of failure.
        
        """
        return _gv.gv_raster_layer_histogram_view(self._o, isource,
                                                  scale_min, scale_max,
                                                  hist_size )
    
    def launch_properties(self):
        import gvrasterpropdlg
        return gvrasterpropdlg.LaunchRasterPropDialog( self )

    def add_height(self, height_raster, default_height = 0.0):
        """ Adds height to raster layer for 3D effect.

        Georeferrencing information will be used to place height_raster
        with respect to layer.

        height_raster -- a GvRaster containing elevation information in a
        compatible georeferencing system with this raster layer."""

        # Actually add the height.
        
        _gv.gv_raster_layer_add_height(self._o, height_raster._o,
                                       default_height)

        # In order to be able to reconstitute with elevation data,
        # we need to store information about where the elevation came from.

        self.set_property( '_gv_add_height_filename',
                           height_raster.get_dataset().GetDescription() )
        self.set_property( '_gv_add_height_band',
                           str(height_raster.get_band_number()) )
        self.set_property( '_gv_add_height_default',
                           str(default_height) )

    def clamp_height(self, bclamp_min=0, bclamp_max=0, 
                     min_height=-30000.0,max_height=30000.0):
        """ Sets lower mesh height bound to min_height if bclamp_min is 1.
        Sets upper mesh height bound to max_height if bclamp_max is 1. """

        _gv.gv_raster_layer_clamp_height(self._o, bclamp_min, bclamp_max,
                                         min_height, max_height)
            
    def complex_lut(self, method='magnitude'):

        # This property is set at c-level now.
        #self.set_property( 'last_complex_lut', method )
        
        # Magnitude
        if method == 'magnitude':
            self.lut_color_wheel_new_ev( 0, 1 )
            
        # Phase
        elif method == 'phase':
            self.lut_color_wheel_new_ev( 1, 0 )

        # Magnitude and Phase
        elif method == 'magphase':
            self.lut_color_wheel_new_ev( 1, 1 )

        # Real
        elif method == 'real':
            self.lut_color_wheel_new( RL_LUT_SCALAR, -1,
                                      RL_LUT_SCALAR, 0.75,
                                      RL_LUT_REAL, 1 )

        # Imaginary
        elif method == 'imaginary':
            self.lut_color_wheel_new( RL_LUT_SCALAR, -1,
                                      RL_LUT_SCALAR, 0.75,
                                      RL_LUT_IMAGINARY, 1 )
        
    def equalize(self, viewonly = 0):
        """Compute a histogram equalized source LUT, and apply.

        This method is not meaningful for RLM_COMPLEX layers, and will
        be ignored."""

        for isrc in range(self.sources):
            raster = self.get_data(isrc)
            if raster is None:
                continue
            
            (smin, smax) = self.autoscale(viewonly=viewonly,isource=isrc)
            
            if viewonly == 0:
                gdal_band = raster.get_band()
                histogram = gdal_band.GetHistogram(smin, smax, approx_ok = 1)
            else:
                try:
                    histogram = self.histogram_view(isrc, smin, smax, 256 )
                except:
                    # normally this means we are "off" the raster.
                    continue

            cum_hist = []
            total = 0
            for bucket in histogram:
                cum_hist.append(total + bucket/2)
                total = total + bucket

            if total == 0:
                total = 1
                gdal.Debug( 'OpenEV',
                       'Histogram total is zero in GvRasterLayer.equalize()' )
                
            lut = ''
            for i in range(256):
                value = (cum_hist[i] * 256L) / total
                if value < 0 :
                    value = 0
                elif value >= 255:
                    value = 255
                lut = lut + chr(value)
                
            self.set_source(isrc, raster, smin, smax, 
                            self.get_const_value(isrc), lut,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'equalize' )

    def linear( self, viewonly = 0 ):

        for isrc in range(self.sources):
            (smin, smax) = self.autoscale( isource=isrc, viewonly = viewonly )
            
            self.set_source(isrc, self.get_data(isrc), smin, smax,
                            self.get_const_value(isrc), None,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'linear' )

    def none_lut( self, viewonly = 0 ):

        for isrc in range(self.sources):
            raster = self.get_data(isrc)
            if raster is None:
                continue
            
            if raster.get_band().DataType == gdal.GDT_Byte:
                (smin, smax) = (0.0, 255.0)
            else:
                (smin, smax) = self.autoscale( isource = isrc,
                                               viewonly = viewonly )

            self.set_source(isrc, self.get_data(isrc), smin, smax,
                            self.get_const_value(isrc), None,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'none_lut' )

    def log( self, viewonly = 0 ):

        import math
        
        lut = ''
        for i in range(256):
            value = int((255 * (math.log(1.0+i) / math.log(256.0)))+0.5)
            if value < 0 :
                value = 0
            elif value >= 255:
                value = 255
            lut = lut + chr(value)
                
        for isrc in range(self.sources):
            (smin, smax) = self.autoscale( isource=isrc, viewonly = viewonly )
            self.set_source(isrc, self.get_data(isrc), smin, smax,
                            self.get_const_value(isrc), lut,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'log' )

    def root( self, viewonly = 0 ):

        import math
        
        lut = ''
        for i in range(256):
            value = 255 * math.sqrt(i/255.0)
            if value < 0 :
                value = 0
            elif value >= 255:
                value = 255
            lut = lut + chr(value)
                
        for isrc in range(self.sources):
            (smin, smax) = self.autoscale( isource=isrc, viewonly = viewonly )

            self.set_source(isrc, self.get_data(isrc), smin, smax,
                            self.get_const_value(isrc), lut,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'root' )

    def square( self, viewonly = 0 ):

        import math
        
        lut = ''
        for i in range(256):
            value = 255 * math.pow(i/255.0,2.0)
            if value < 0 :
                value = 0
            elif value >= 255:
                value = 255
            lut = lut + chr(value)
                
        for isrc in range(self.sources):
            (smin, smax) = self.autoscale( isource=isrc, viewonly = viewonly )

            self.set_source(isrc, self.get_data(isrc), smin, smax,
                            self.get_const_value(isrc), lut,
                            self.nodata_get(isrc))

        self.set_property( 'last_stretch', 'square' )

    def window_restretch(self):

        # Re-apply the last stretch operation.
        if self.get_property( 'last_stretch' ) != None:
            func_name = 'self.'+ self.get_property('last_stretch')
        else:
            func_name = 'self.'+ 'linear'

        exec 'func = ' + func_name  in locals()

        func( viewonly = 1 )
    
    def get_height( self, x, y ):
        """Fetch 3D mesh height at location

        Returns the elevation as extracted from the mesh used for 3D
        display at the indicated georeferenced location on this raster
        layer.  If the request fails for some reason (such as being off
        the raster) an exception is generated.

        x -- Georeferenced X location to sample at. 
        y -- Georeferenced Y location to sample at.
        """
        return _gv.gv_raster_layer_get_height( self._o, x, y )

    def build_skirt( self, base_height = 0.0 ):
        """Build a skirt around the edges of layer.

        The skirt is basically edges dropping down from the edge of the
        raster to some base height.  The skirt generation knows about nodata
        regions, and will also build skirts on their edges.  The skirt is
        coloured according to the location on the raster it is dropped from.

        base_height -- elevation to which the skirt drops, defaults to 0.0.

        The returned skirt is a GvLayer (currently a GvShapesLayer). 
        """
        layer_o = _gv.gv_build_skirt( self._o, base_height )
        if layer_o is not None:
            return GvLayer( layer_o )
        else:
            return None

    def refresh( self ):
        """Refresh raster data from disk."""
        for isource in range(4):
            raster = self.get_data(isource)
            if raster is not None:
                raster.changed()

###############################################################################
class GvTool(_gtk.GtkObject):
    get_type = _gv.gv_tool_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        
    def activate(self, view):
        _gv.gv_tool_activate(self._o, view._o)
        
    def deactivate(self, view):
        _gv.gv_tool_deactivate(self._o, view._o)
        
    def get_view(self):
        v_o = _gv.gv_tool_get_view(self._o)
        if v_o is None:
            return None
        else:
            return GvViewArea(_obj=v_o)
        
    def set_boundary(self, boundary):
        """Set constraint rectangle.

        boundary -- boundary is a tuple in the form (column,row,width,height)
        """
        return _gv.gv_tool_set_boundary(self._o, boundary)

    def set_cursor(self, cursor_type):
        """ Set the tool's associated cursor.

        cursor_type -- an integer (one of the standard GDK cursor types)
        """
        return _gv.gv_tool_set_cursor(self._o, cursor_type)


###############################################################################
class GvSelectionTool(GvTool):
    get_type = _gv.gv_selection_tool_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_selection_tool_new()
    def set_layer(self, layer):
        _gv.gv_selection_tool_set_layer(self._o, layer._o)

###############################################################################
class GvZoompanTool(GvTool):
    get_type = _gv.gv_zoompan_tool_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_zoompan_tool_new()

###############################################################################
class GvPointTool(GvTool):
    get_type = _gv.gv_point_tool_get_type
    def __init__(self, layer=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_point_tool_new()
        if layer: self.set_named_layer(layer)
    def set_layer(self, layer):
        _gv.gv_point_tool_set_layer(self._o, layer._o)    
    def set_named_layer(self, name):
        _gv.gv_point_tool_set_named_layer(self._o, name)

###############################################################################
class GvLineTool(GvTool):
    get_type = _gv.gv_line_tool_get_type
    def __init__(self, layer=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_line_tool_new()
        if layer: self.set_named_layer(layer)
    def set_layer(self, layer):
        _gv.gv_line_tool_set_layer(self._o, layer._o)
    def set_named_layer(self, name):
        _gv.gv_line_tool_set_named_layer(self._o, name)

###############################################################################
class GvRectTool(GvTool):
    get_type = _gv.gv_rect_tool_get_type
    def __init__(self, layer=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_rect_tool_new()
        if layer: self.set_named_layer(layer)
    def set_layer(self, layer):
        _gv.gv_rect_tool_set_layer(self._o, layer._o)
    def set_named_layer(self, name):
        _gv.gv_rect_tool_set_named_layer(self._o, name)

###############################################################################
class GvRotateTool(GvTool):
    get_type = _gv.gv_rotate_tool_get_type
    def __init__(self, layer=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_rotate_tool_new()
        if layer: self.set_named_layer(layer)
    def set_layer(self, layer):
        _gv.gv_rotate_tool_set_layer(self._o, layer._o)
    def set_named_layer(self, name):
        _gv.gv_rotate_tool_set_named_layer(self._o, name)

###############################################################################
class GvAreaTool(GvTool):
    get_type = _gv.gv_area_tool_get_type
    def __init__(self, layer=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_area_tool_new()
        if layer: self.set_named_layer(layer)
    def set_layer(self, layer):
        _gv.gv_area_tool_set_layer(self._o, layer._o)
    def set_named_layer(self, name):
        _gv.gv_area_tool_set_named_layer(self._o, name)

###############################################################################
class GvNodeTool(GvTool):
    get_type = _gv.gv_node_tool_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_node_tool_new()
    def set_layer(self, layer):
        _gv.gv_node_tool_set_layer(self._o, layer._o)

###############################################################################
class GvRoiTool(GvTool):
    """Region of Interest Selection Tool

    Signals:

    roi-changing -- generated when the ROI is being rubber-banded and
                    coordinates are changing
        
    roi-changed -- generated when the ROI has been changed and not currently
    being modified.
    """
    
    get_type = _gv.gv_roi_tool_get_type
    def __init__(self, boundary=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_roi_tool_new()
        if boundary: self.set_boundary(boundary)
    def get_rect(self):
        """ Returns the current ROI """
        return _gv.gv_roi_tool_get_rect(self._o)
    def append(self, rect):
        """ Creates an ROI.

        rect -- a tuple (column, row, width, height)
        """
        return _gv.gv_roi_tool_new_rect(self._o, rect)
    
###############################################################################
class GvPoiTool(GvTool):
    """Point of Interest Selection Tool

    Signals:

    poi-changed -- generated when the POI has been changed.
    """
    
    get_type = _gv.gv_poi_tool_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_poi_tool_new()

    def get_point(self):
        """ Returns the current POI """
        return _gv.gv_poi_tool_get_point(self._o)

    def set_point(self, point):
        """ Sets the current POI.

        point -- a tuple (column, row)
        """
        return _gv.gv_poi_tool_new_point(self._o, point)
    
###############################################################################
class GvTrackTool(GvTool):
    get_type = _gv.gv_track_tool_get_type
    def __init__(self, label=None, _obj=None):
        if _obj: self._o = _obj; return
        if label is None:
            raise ValueError, "expecting GtkLabel instance"
        self._o = _gv.gv_track_tool_new(label._o)

###############################################################################
class GvToolbox(GvTool):
    get_type = _gv.gv_toolbox_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_toolbox_new()
    def add_tool(self, name, tool):
        _gv.gv_toolbox_add_tool(self._o, name, tool._o)
    def activate_tool(self, name):
        _gv.gv_toolbox_activate_tool(self._o, name)


###############################################################################
class GvAutopanTool(GvTool):
    """Autopan Tool

    Signals:

    """
    
    get_type = _gv.gv_autopan_tool_get_type
    def __init__(self, boundary=None, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_autopan_tool_new()
        if boundary: self.set_boundary(boundary)

    def set_extents(self, rect):
        """ Sets the panning extents.

        rect -- a tuple (column, row, width, height)
        """
        return _gv.gv_autopan_tool_new_rect(self._o, rect)
    
    def get_extents(self):
        """ Gets the panning extents.
            Returns a tuple (column, row, width, height)
        """
        return _gv.gv_autopan_tool_get_rect(self._o)
    
    def play(self):
        """ Start panning. """
        return _gv.gv_autopan_tool_play(self._o)
    
    def pause(self):
        """ Pause panning. Regions remain drawn in secondary views."""
        return _gv.gv_autopan_tool_pause(self._o)
    
    def stop(self):
        """ Stop panning. Regions do not remain drawn in secondary views."""
        return _gv.gv_autopan_tool_stop(self._o)

    def set_speed(self, speed):
        """ Set the relative speed (a value between -1 and 1: -1
            for maximum speed backwards; 1 for maximum speed
            forwards).
        """
        return _gv.gv_autopan_tool_set_speed(self._o, speed)

    def get_speed(self):
        """ Returns the current speed setting. """
        
        return _gv.gv_autopan_tool_get_speed(self._o)

    def set_overlap(self, overlap):
        """ Set block overlap perpendicular to panning direction
            (a value between 0 and 1).
        """
        return _gv.gv_autopan_tool_set_overlap(self._o, overlap)

    def get_overlap(self):
        """ Returns the current overlap setting. """
        return _gv.gv_autopan_tool_get_overlap(self._o)

    def set_block_x_size(self, xsize, mode):
        """ Set size of high-resolution block.
            Inputs:
                xsize- width of block, as a fraction of the
                       full panning region width if mode == 0
                       (in this case 0 < xsize < 1), or in
                       view coordinates if mode == 1.
                mode- block size setting mode.
        """
        return _gv.gv_autopan_tool_set_block_x_size(self._o, xsize, mode)

    def set_x_resolution(self, resolution):
        """ Set the resolution of the zoomed extents:
            Inputs:
                resolution- view resolution
        """
        return _gv.gv_autopan_tool_set_x_resolution(self._o, resolution)

    def set_standard_path(self, path_type):
        """ Set the standard path to follow in panning:
            Inputs:
                path_type- an integer (0-4, currently)

                0- start top left, go right, down, left, down,...
                1- start bottom left, go right, up, left, up,...
                2- start top right, go left, down, right, down,...
                3- start bottom right, go left, up, left, up,...
                4- start top left, go right, jump down and back
                   to the left edge, go right,...
        """
        return _gv.gv_autopan_tool_set_standard_path(self._o, path_type)

    def set_lines_path(self, lines):
        """ Sets the path to follow based on a GvShapes object
            that contains line shapes.
        """
        return _gv.gv_autopan_tool_set_lines_path(self._o, lines._o)

    def set_location(self, x, y):
        """ Set the current location within the panning
            extents (snaps to nearest computed location).
        """
        # z is in case we ever do anything with 3d panning, but
        # for now only 2d has been considered.
        return _gv.gv_autopan_tool_set_location(self._o,x,y,0)

    def get_location(self):
        """ Get the current location within the panning extents.
            Raises an error if there is no current location.
        """
        return _gv.gv_autopan_tool_get_location(self._o)

    def get_state(self):
        """ Gets the current settings of the following autopan
            tool parameters (returned as a tuple):
            
                play_flag: 0- stopped, 1- playing, 2- paused
                
                path_type: 0- starts top left, goes right, down, left...
                           1- starts bottom left, goes right, up, left...
                           2- starts top right, goes left, down, right...
                           3- starts bottom right, goes left, up, right...
                           
                
                block_size_mode, block_x_size, resolution:
                  block_size_mode = 0:
                      - user sets block_x_size to a float between 0 and 1,
                        corresponding to the block size as a fraction of the
                        total x extents (block_y_size will be determined by
                        block_x_size and the window's aspect ratio).
                        resolution is ignored in this mode.

                  block_size_mode = 1:
                      - same as mode 0, except that block_x_size is in view
                        coordinates rather than a fraction of total x extents
                        to be panned.

                  block_size_mode = 2:
                      - block size is set so that the size of pixels in the 
                        view will be constant at resolution.

                num_views: number of secondary views associated with
                           the tool.
        """
        return _gv.gv_autopan_tool_get_state(self._o)

    def clear_trail(self):
        """ Clear the stored trail and refresh secondary views. """
        return _gv.gv_autopan_tool_clear_trail(self._o)

    def set_trail_color(self, view, red, green, blue, alpha):
        """ Set the trail color for a secondary view.

            Inputs:
                view- view to reset the trail color of.
                red, green, blue, alpha- floating point values in
                                         the range 0-1.
        """
        return _gv.gv_autopan_tool_set_trail_color(self._o, view._o, red,
                                                   green, blue, alpha)

    def set_trail_mode(self, view, trail_mode):
        """ Set whether or not to display a trail in a secondary
            view.

            Inputs:
                view- view to reset the trail mode on.
                trail_mode- integer 0 or 1.
        """
        return _gv.gv_autopan_tool_set_trail_mode(self._o, view._o, trail_mode)

    def set_trail_parameters(self, overview_extents, overview_width_pixels):
        """ Set the rough predicted extents that the trail will cover, and
            the width that this should correspond to in screen pixels. """
        return _gv.gv_autopan_tool_set_trail_parameters(self._o,
                                                 overview_extents,
                                                 overview_width_pixels)

    def get_trail_parameters(self):
        """ Get the trail parameters and number of trail tiles.
        
            Returns a tuple (extents,width,num tiles):
                extents, width- parameters used to decide trail tile
                                coverage and resolution (see
                                set_trail_parameters)
                num tiles- number of trail tiles created so far.
        """
        tup = _gv.gv_autopan_tool_get_trail_parameters(self._o)
        return ((tup[0],tup[1],tup[2],tup[3]),tup[4],tup[5])
                

    def save_trail_tiles(self, basename):
        """ Saves trail tiles to files named basename+'0',
            basename+'1', etc.  Returns the number of tiles saved
            (-1 if an error occured).  Tiles are always saved
            to Geotiff format (requires metadata capability).
        """
        return _gv.gv_autopan_tool_save_trail_tiles(self._o,
                                                    basename)
    
    def load_trail_tiles(self, basename, num_trail_tiles):
        """ Loads trail tiles from files named basename+'0',
            basename+'1', etc., up to basename+str(num_trail_tiles-1)
            Returns the number of tiles loaded
            (-1 if an error occured).
        """
        return _gv.gv_autopan_tool_load_trail_tiles(self._o,
                                                    basename,
                                                    num_trail_tiles)

    def register_view(self, view, can_resize=0, can_reposition=0,
                      trail_mode=0):
        """ Register a secondary view.  Current panning extents will
            be drawn as a blue-green rectangle in this view.
            Inputs:
                view- view to register
                can_resize- integer 0 or 1: 1 if user can resize the
                            current panning block size by banding
                            the rectangle in the secondary view, 0
                            if they can't. NOT IMPLEMENTED YET: set
                            to 0.
                can_reposition- integer 0 or 1: 1 if user can reposition the
                            current panning block size by dragging
                            the rectangle in the secondary view, 0
                            if they can't.
                trail_mode- integer 0 or 1: 0 if view should not show
                            trail already traveled; 1 if it should.
        """
        return _gv.gv_autopan_tool_register_view(self._o, view._o,
                                                 can_resize, can_reposition,
                                                 trail_mode)

    def remove_view(self, view):
        """ De-register a secondary view. """
        return _gv.gv_autopan_tool_remove_view(self._o, view)


###############################################################################
class GvViewLink(_gtk.GtkObject):
    get_type = _gv.gv_view_link_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_view_link_new()
    def register_view(self, view):
        _gv.gv_view_link_register_view(self._o, view._o)
    def remove_view(self, view):
        _gv.gv_view_link_remove_view(self._o, view._o)
    def enable(self):
        _gv.gv_view_link_enable(self._o)
    def disable(self):
        _gv.gv_view_link_disable(self._o)
    def set_cursor_mode(self,mode=0):
        try:
            _gv.gv_view_link_set_cursor_mode(self._o,mode)
        except:
            pass

###############################################################################
class GvSymbolManager(_gtk.GtkObject):
    get_type = _gv.gv_symbol_manager_get_type
    
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_get_symbol_manager()

    def get_symbol( self, name ):
        result = _gv.gv_symbol_manager_get_symbol( self._o, name )
        if result is not None and result[0] == 1:
            result = (result[0], GvShape( _obj = result[1] ) )

        return result

    def has_symbol( self, name ):
        return _gv.gv_symbol_manager_has_symbol( self._o, name )

    def get_names( self ):
        return _gv.gv_symbol_manager_get_names( self._o )

    def inject_raster_symbol( self, name, width, height, rgba_buffer  ):
        _gv.gv_symbol_manager_inject_raster_symbol( self._o, name,
                                                    width, height, rgba_buffer)

    def inject_vector_symbol( self, name, shape ):
        _gv.gv_symbol_manager_inject_vector_symbol( self._o, name, shape._o )

    def eject_symbol( self, name ):
        return _gv.gv_symbol_manager_eject_symbol( self._o, name )

    def save_vector_symbol( self, name, newname ):
        _gv.gv_symbol_manager_save_vector_symbol( self._o, name, newname )

    def serialize( self ):
        tree = [gdal.CXT_Element, 'GvSymbolManager']

        names = self.get_names()
        
        for name in names:
            sym = self.get_symbol( name )
            if sym[0] == 0:
                print 'rasters symbol serialization not yet supported.'

            elif sym[0] == 1:
                vs = [CXT_Element, 'GvVectorSymbol',
                      [CXT_Attribute, 'name',
                       [CXT_Text, name]]]
                vs.append( sym[1].serialize() )
                tree.append( vs )
            else:
                print 'unsupported symbol type, not serialized'

        return tree
        
    def initialize_from_xml( self, tree, filename=None ):
        for item in tree[2:]:
            if item[0] == CXT_Element and item[1] == 'GvVectorSymbol':
                name = gvutils.XMLFindValue(item, 'name', None )
                shape = GvShapeFromXML( gvutils.XMLFind( item, 'GvShape' ), None )
                self.inject_vector_symbol( name, shape )

###############################################################################
class GvManager(_gtk.GtkObject):
    get_type = _gv.gv_manager_get_type
    def __init__(self, _obj=None):
        if _obj: self._o = _obj; return
        self._o = _gv.gv_get_manager()

    def add_dataset(self, dataset):
        """Adds gdal.Dataset instance to the list of managed datasets.

        This method adds given gdal.Dataset instance to the list of available
	datasets. Does nothing if this dataset already listed.
	
	Returns a gdal.Dataset object (the same as given in parameters)."""

        swig_ds = _gv.gv_manager_add_dataset(self._o, dataset._o)
        if swig_ds is None:
            return None

        return gdal.Dataset( _obj=swig_ds )

    def get_dataset(self, filename):
        """Fetch gdal.Dataset for a filename.

        This method fetches a gdal.Dataset for a given filename, while
        ensuring that the dataset is only opened once, even if requested
        more than once.
	
	Returns an opened  gdal.Dataset object."""

        swig_ds = _gv.gv_manager_get_dataset(self._o, filename)
        if swig_ds is None:
            return None

        return gdal.Dataset( _obj=swig_ds )
        
    def get_dataset_raster(self,dataset,band):
        """Fetch GvRaster for a dataset band.

        This method fetches a GvRaster for a given dataset band, while
        ensuring that only one GvRaster is instantiated for the band
        across the whole application. """
        
        raster_o = _gv.gv_manager_get_dataset_raster(self._o, dataset._o,band)
        if raster_o is None:
            return None

        return GvRaster(_obj=raster_o)

    def set_busy( self, busy_flag ):
        _gv.gv_manager_set_busy( self._o, busy_flag )

    def get_busy( self ):
        return _gv.gv_manager_get_busy( self._o )

    def queue_task( self, task_name, priority, cb, cb_data = None ):
        """Queue an idle task.

        The GvManager has a concept of a unified, prioritized set of idle
        tasks.  These are only executed when there is no further pending
        user input, or windows events to process, and are typically used to
        perform low priority work like loading additional tiles in GvRasters
        for display purposes.

        This mechanism can also be used by the application level, for
        instance, to update the gui, or perform chunks of processing.

        Note that there is no mechanism available to remove a task from
        the queue untill it is actually executed.  Items in the list can be
        dumped to stderr with the GvManager.dump() call for debugging purposes.

        The OpenEV core currently has three idle tasks which may be queued:

         - zoompan-handler (priority 2): used to implement continuous zooming.
         - 3d-motion-handler (priority 2): similar to zoompan-handler for 3d.
         - raster-layer-update (priority 10): used to load, and process
         additional raster tiles.

        Note that the return value of the user callback is examined to
        determine if the task should be requeued automatically.  A value
        of zero indicates that the task should not be requeued, while any
        other numeric value results in automatic requeuing. 

        task_name -- name for task, useful in debugging.
        priority -- numeric priority.  Higher values have lower priority.
        cb -- python callback to invoke
        cb_data -- single argument to pass to callback (optional).
        """
        
        _gv.gv_manager_queue_task( self._o, task_name, priority, cb, cb_data )

    def dump( self ):
        """Dump GvManager info to stderr.

        The list of preferences, openev datasets, and idle tasks is written
        to stderr in human readable format.  Useful as a debugging aid.
        """
        _gv.gv_manager_dump( self._o )
        

###############################################################################
def undo_register(data):
    """Register GvData for undo.

    data -- GvData to be registered.

    This call registers the passed GvData with the undo system.  As long
    as it exists, and the undo system is enabled any changes to it will
    be recorded for undo.  There is no way to unregister an individual GvData
    once registered."""
    _gv.gv_undo_register_data(data._o)

    
###############################################################################
def can_undo():
    """Returns TRUE if undo system is enabled."""
    return _gv.gv_undo_can_undo()


###############################################################################
def undo_pop():
    """Undo the most recent undo group."""
    _gv.gv_undo_pop();

###############################################################################
def undo_clear():
    """Destroy all saved undo steps."""
    _gv.gv_undo_clear();

###############################################################################
def undo_close():
    """Temporarily disable capture of undo steps."""
    _gv.gv_undo_close();

###############################################################################
def undo_open():
    """Enable capture of undo steps."""
    _gv.gv_undo_open();

###############################################################################
def undo_start_group():
    """Establish a multi operation undo group.

    All undo operations saved to the undo stack after this call, and
    before the next undo_end_group() call will be considered to be a single
    group.  A single call to undo_pop() will cause the entire group of
    undo steps to be applied.

    This is normally used to group multiple underlying operations that
    should appear to be a single operation to the user. 

    Returns the undo group integer identifier.  This should be kept and
    passed to the undo_end_group() method to terminate the grouping."""
    return _gv.gv_undo_start_group()

###############################################################################
def undo_end_group( group ):
    """Close off a multi operation undo group.

    group -- the group id to be terminated.  This should be the value
    returned by the corresponding undo_start_group()."""
    return _gv.gv_undo_end_group( group )



###############################################################################
# Manage Application Properties:

app_preferences = None
app_preffile = None

def set_default_preferences( defaults ):
    """
    add a set of default preferences to the gview preference manager if they are not already
    loaded.

    defaults - a dictionary of pref_name = default_value pairs.

    this checks to make sure that the preferences are already loaded.
    """
    global app_preferences
   
    if app_preferences is None:
        load_preferences()
    for key in defaults.keys():
        if get_preference(str(key)) is None:
            set_preference( str(key), str(defaults[key]))


def get_preference(name, default = None):
    """Fetch preference value

    This method will return a String value, or None if the preference is
    unknown.
    
    name -- the name of the preference to fetch.
    """
    global app_preferences
    
    if app_preferences is None:
        load_preferences()
        
    res = _gv.gv_manager_get_preference(manager._o,name)
    if res is None:
        return default
    else:
        return res

def set_preference(name,value):
    """Set preference value

    This method will set the preference value in a global application list,
    which will be saved on application shutdown in the $HOME/.openev file,
    and restore on subsequent startups.

    name -- preference name (String)
    value -- preference value (String)
    """
    global app_preferences
    
    if app_preferences is None:
        load_preferences()

    return _gv.gv_manager_set_preference(manager._o,name,value)

def load_preferences():
    global app_preferences
    
    app_preferences = {}
    
    if not os.path.exists(get_preffile()):
        return
    
    file = open(get_preffile(),'r')
    contents = file.readlines()
    file.close()
    
    for line in contents:
        tokens = string.split(line, '=', 1)
        if len(tokens) == 2:
            name,value = tokens
            set_preference( string.strip(name), string.strip(value) )
    
def save_preferences():
    global app_preferences

    if app_preferences is None:
        return

    prefs = _gv.gv_manager_get_preferences(manager._o)
    
    if not os.path.exists(os.path.dirname(get_preffile())):
        return
    
    file = open(get_preffile(), 'w')
    for item in prefs.items():
        name, value = item
        file.write(name + '=' + value + '\n')
    file.close()

def get_preffile():
    global app_preffile

    if app_preffile is None:
        app_preffile = os.path.expanduser('~/.openev')
        if app_preffile == '\\/.openev' or app_preffile == '~/.openev':
            app_preffile = 'C:\\.openev'

    return app_preffile
    

###############################################################################
def find_gview():
    try:
        gv_path = os.environ['OPENEV_HOME']
        if os.path.isdir(os.path.join(gv_path,'pics')):
            return gv_path
    except:
        pass
    
    try:
        gv_path = os.environ['OPENEVHOME']
        if os.path.isdir(os.path.join(gv_path,'pics')):
            return gv_path
    except:
        pass
    
    for dir in sys.path:
        gv_path = os.path.normpath(os.path.join(dir,'..'))
        if os.path.isdir(os.path.join(gv_path,'pics')):
            return gv_path
        
    gv_path = os.path.expanduser('~/devel/gview')
    if os.path.isdir(os.path.join(gv_path,'pics')):
        return gv_path
    
    gv_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    if os.path.isdir(os.path.join(gv_path,'pics')):
        return gv_path

    print 'Unable to find OpenEV tree ... some problems may be encountered.'
    return ''

###############################################################################
def raster_cache_get_max():
    return _gv.gv_raster_cache_get_max()

def raster_cache_set_max(new_max):
    _gv.gv_raster_cache_set_max(new_max)

def raster_cache_get_used():
    return _gv.gv_raster_cache_get_used()

def texture_cache_get_max():
    return _gv.gv_texture_cache_get_max()

def texture_cache_set_max(new_max):
    _gv.gv_texture_cache_set_max(new_max)

def texture_cache_get_used():
    return _gv.gv_texture_cache_get_used()

def texture_cache_dump():
    return _gv.gv_texture_cache_dump()

###############################################################################

def rgba_to_rgb(rgba):
    #Convert RGBA data to RGB.
    #
    #This function is used to accelerate conversion of RGBA LUTs into RGB
    #so that they can be displayed in a GtkPreview.  Currently only used by
    #gvrasterpropdlg.py.
    return _gv.gv_rgba_to_rgb(rgba)

###############################################################################

def gtk_object_deref_and_destroy(object):
    _gtkmissing.gtk_object_deref_and_destroy(object._o)

def gtk_object_get_ref_count(object):
    return _gtkmissing.gtk_object_get_ref_count(object._o)

def gtk_object_sink(object):
    return _gtkmissing.gtk_object_sink(object._o)

def gtk_object_ref(object):
    return _gtkmissing.gtk_object_ref(object._o)

def gtk_object_unref(object):
    return _gtkmissing.gtk_object_ref(object._o)

def py_object_get_ref_count(object):
    return _gtkmissing.py_object_get_ref_count(object)

pgu.gtk_register('IpGcpLayer', IpGcpLayer)
pgu.gtk_register('AppCurLayer', AppCurLayer)
for m in map(lambda x: eval(x), filter(lambda x: x[:2] == 'Gv', dir())):
    if m != 'GvShape':
        pgu.gtk_register(m.__name__,m)
        
del m

manager = GvManager(_obj = _gv.gv_get_manager())
get_preference('test')

"""Home directory of OpenEV tree for purposes of finding icons, online help,
etc"""
home_dir = find_gview()

if get_preference('gdal_cache') != None:
    import gdal
    gdal.SetCacheMax( int(get_preference('gdal_cache')) )
else:
    gdal.SetCacheMax( 12582912 )

if get_preference('gvraster_cache') != None:
    raster_cache_set_max( int(get_preference('gvraster_cache')) )
else:
    raster_cache_set_max( 39845888 )
    
if get_preference('texture_cache') != None:
    texture_cache_set_max( int(get_preference('texture_cache')) )
else:
    texture_cache_set_max( 33554432 )
