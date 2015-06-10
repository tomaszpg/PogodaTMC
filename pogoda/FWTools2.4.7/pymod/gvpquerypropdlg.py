###############################################################################
# $Id: gvpquerypropdlg.py,v 1.11 2000/08/23 14:32:10 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  GvPqueryLayer Properties Dialog
# Author:   Frank Warmerdam, warmerda@home.com
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
#  $Log: gvpquerypropdlg.py,v $
#  Revision 1.11  2000/08/23 14:32:10  warmerda
#  fixed logic of pixel_mode callback
#
#  Revision 1.10  2000/08/22 16:13:33  warmerda
#  fixed layer: prefixing of layer name
#
#  Revision 1.9  2000/08/10 15:59:29  warmerda
#  added help topic
#
#  Revision 1.8  2000/07/21 01:34:56  warmerda
#  added read_only flag for GvData, and utilize for vector layers
#
#  Revision 1.7  2000/07/20 02:45:04  warmerda
#  avoid doing gui updates in response to signals if dialog destroyed
#
#  Revision 1.6  2000/06/14 15:13:21  warmerda
#  updated pgu stuff
#
#  Revision 1.5  2000/06/09 01:04:14  warmerda
#  added standard headers
#

from gtk import *
from string import *

from gvconst import *
import gview
import gvvectorpropdlg
import gvutils
import pgucolorsel
import gvhtml

pq_prop_dialog_list = []

def LaunchPQueryPropDialog(layer):
    # Check list to see if dialog exists - make it visible
    for test_dialog in pq_prop_dialog_list:
        if test_dialog.layer._o == layer._o:
            test_dialog.update_gui()
            test_dialog.show()
            test_dialog.get_window()._raise()
            return test_dialog

    # Create new dialog if one doesn't exist already
    new_dialog = GvPQueryPropDialog(layer)
    pq_prop_dialog_list.append( new_dialog )
    return new_dialog

class GvPQueryPropDialog(gvvectorpropdlg.GvVectorPropDialog):

    def __init__(self, layer):
        GtkWindow.__init__(self)
        self.set_title('GView')
        self.layer = layer
        self.updating = FALSE

        gvhtml.set_help_topic( self, "gvpquerypropdlg.html" )
        
        # create the general layer properties dialog
        self.create_notebook()
        self.create_pane1()
        
        if self.layer is not None:
            self.layer.connect('display-change', self.refresh_cb)
        
        # Setup Object Drawing Properties Tab
        self.pane2 = GtkVBox(spacing=10)
        self.pane2.set_border_width(10)
        self.notebook.append_page( self.pane2, GtkLabel('Draw Styles'))

        vbox = GtkVBox(spacing=10)
        self.pane2.add(vbox)

        # Create Color control.
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Color:'),expand=FALSE)
        self.point_color = \
                 pgucolorsel.ColorControl('Point Color',
                                          self.color_cb,'_point_color')
        box.pack_start(self.point_color)

        # Point size
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Point Size:'),expand=FALSE)
        self.point_size = GtkCombo()
        self.point_size.set_popdown_strings(
            ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '15', '20') )
        self.point_size.entry.connect('changed', self.point_size_cb)
        box.pack_start(self.point_size,expand=FALSE)

        # Coordinate
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Coordinate:'),expand=FALSE)

        self.coord_om = gvutils.GvOptionMenu(
            ('Off','Raster Pixel/Line','Georeferenced','Geodetic (lat/long)'),
            self.set_coordinate_mode)
        box.pack_start(self.coord_om,expand=FALSE)

        # Raster Value
        box = GtkHBox(spacing=3)
        vbox.pack_start(box, expand=FALSE)
        box.pack_start(GtkLabel('Pixel Value:'),expand=FALSE)

        self.pixel_mode_om = \
            gvutils.GvOptionMenu(('On','Off'), self.set_pixel_mode)
        box.pack_start(self.pixel_mode_om,expand=FALSE)

        self.update_gui()
        
        self.show_all()

    # Initialize GUI state from underlying object state.
    def update_gui(self):
        if self.flags( DESTROYED ) > 0:
            return
        
        if self.layer is None or self.updating == TRUE:
            return

        self.updating = TRUE
        
        # Layer name.
        self.layer_name.set_text( self.layer.get_name() )
        
        # Visibility radio buttons
        self.vis_yes.set_active( self.layer.is_visible() )
        self.vis_no.set_active( not self.layer.is_visible() )

        # Editability radio buttons
        self.edit_yes.set_active( not self.layer.is_read_only() )
        self.edit_no.set_active( self.layer.is_read_only() )

        self.set_color_or_default('_point_color', self.point_color)
        # point size
        self.point_size.entry.delete_text(0,-1)
        if self.layer.get_property('_point_size') is None:
            self.point_size.entry.insert_text('6')
        else:
            self.point_size.entry.insert_text(
                self.layer.get_property('_point_size'))

        # coordinate mode
        mode = self.layer.get_property( '_coordinate_mode' )
        if mode is None:
            self.coord_om.set_history(2)
        elif mode == 'off':
            self.coord_om.set_history(0)
        elif mode == 'raster':
            self.coord_om.set_history(1)
        elif mode == 'latlong':
            self.coord_om.set_history(3)
        else:
            self.coord_om.set_history(2)

        # pixel mode
        mode = self.layer.get_property( '_pixel_mode' )
        if mode is None or mode != 'off':
            self.pixel_mode_om.set_history(0)
        else:
            self.pixel_mode_om.set_history(1)

        self.updating = FALSE

    # Dialog closed, remove references to python object
    def close( self, widget, args ):
        pq_prop_dialog_list.remove(self)

    def set_coordinate_mode(self, om):
        if self.coord_om.get_history() == 0:
            self.layer.set_property( '_coordinate_mode', 'off')
        elif  self.coord_om.get_history() == 1:
            self.layer.set_property( '_coordinate_mode', 'raster')
        elif  self.coord_om.get_history() == 2:
            self.layer.set_property( '_coordinate_mode', 'georef')
        elif  self.coord_om.get_history() == 3:
            self.layer.set_property( '_coordinate_mode', 'latlong')
        self.layer.display_change()

    def set_pixel_mode(self, om):
        if om.get_history() == 0:
            self.layer.set_property( '_pixel_mode', 'on')
        else:
            self.layer.set_property( '_pixel_mode', 'off')
        self.layer.display_change()

