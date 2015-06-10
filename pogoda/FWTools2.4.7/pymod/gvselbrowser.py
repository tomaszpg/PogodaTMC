###############################################################################
# $Id: gvselbrowser.py,v 1.4 2001/11/09 15:41:49 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  GUI component to show the current list of selected objects, and
#           to control a single sub-selection out of that set. 
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2001, Frank Warmerdam <warmerdam@pobox.com>
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
#  $Log: gvselbrowser.py,v $
#  Revision 1.4  2001/11/09 15:41:49  warmerda
#  avoid using negative oids
#
#  Revision 1.3  2001/04/23 15:22:47  warmerda
#  added callback on oid text field
#
#  Revision 1.2  2001/04/19 22:07:53  warmerda
#  avoid use of +=
#
#  Revision 1.1  2001/04/09 18:26:46  warmerda
#  New
#
#

from gtk import *
from string import *
from gvsignaler import *
import os.path
import pgu
import gview
import gvutils

class GvSelBrowser(GtkVBox):

    def __init__(self, spacing=10):
        GtkVBox.__init__(self, spacing=spacing)

        self.updating = 0
        
        self.sel_manager = gview.app.sel_manager

        self.sel_manager.subscribe('active-layer-changed', self.update_gui)
        self.sel_manager.subscribe('selection-changed', self.update_gui)
        self.sel_manager.subscribe('subselection-changed', self.update_gui)

        self.tooltips = GtkTooltips()

        hbox = GtkHBox(spacing=3)
        self.pack_start(hbox,expand=FALSE)
        self.hbox = hbox

        hbox.pack_start(GtkLabel('Shape:'),expand=FALSE)

        self.oid_tb = GtkEntry(maxlen=7)
        self.oid_tb.connect('activate', self.oid_cb)
        self.oid_tb.connect('focus-out-event', self.oid_cb)
        hbox.pack_start(self.oid_tb)

        left_button = GtkButton()
        left_button.add(GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                                    'pan_left.xpm')))
        self.tooltips.set_tip(left_button,'Cycle Selection Down')
        left_button.connect('clicked', self.cycle_down)
        hbox.pack_start(left_button,expand=FALSE)

        self.n_of_n_label = GtkLabel('XXXX of XXXX')
        hbox.pack_start(self.n_of_n_label)
        
        right_button = GtkButton()
        right_button.add(GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                                    'pan_rght.xpm')))
        self.tooltips.set_tip(left_button,'Cycle Selection Up')
        right_button.connect('clicked', self.cycle_up)
        hbox.pack_start(right_button, expand=FALSE)

        hbox = GtkHBox(spacing=3)
        self.pack_start(hbox)
        self.layer_label = GtkLabel('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
        self.layer_label.set_justify( JUSTIFY_LEFT )
        hbox.pack_start(self.layer_label, expand=FALSE)

        self.connect('unrealize', self.close)
        
        self.update_gui()
        self.show_all()

    def close(self, *args):
        self.sel_manager.unsubscribe('active-layer-changed', self.update_gui)
        self.sel_manager.unsubscribe('selection-changed', self.update_gui)
        self.sel_manager.unsubscribe('subselection-changed', self.update_gui)
        
    def update_gui(self, *args):
        self.updating = 1
        layer = self.sel_manager.get_active_layer()
        if layer is None:
            self.layer_label.set_text('Layer: <none selected>')
        else:
            self.layer_label.set_text('Layer: '+layer.get_name())
            
        try:
            layer = self.sel_manager.get_active_layer()
            selected = layer.get_selected()
            subsel = layer.get_subselected()
        except:
            self.n_of_n_label.set_text('0 of 0')
            self.oid_tb.set_text('')
            self.updating = 0
            return
        
        self.oid_tb.set_text(str(subsel))

        index_of = self.get_sel_index(subsel,selected)
        
        label = '%d of %d' % (index_of+1, len(selected))
        self.n_of_n_label.set_text(label)
        
        self.updating = 0

    def oid_cb(self, *args):
        if self.updating:
            return
        
        try:
            new_oid = int(self.oid_tb.get_text())
            layer = self.sel_manager.get_active_layer()
            selected = layer.get_selected()
            if new_oid in selected:
                layer.subselect_shape( new_oid )
            else:
                layer.clear_selection()
                if new_oid >= 0:
                    layer.select_shape( new_oid )

            layer.display_change()
        except:
            pass

    def cycle_down(self, *args):
        try:
            layer = self.sel_manager.get_active_layer()
            selected = layer.get_selected()
        except:
            return
        
        index_of = self.get_sel_index( layer.get_subselected(), selected )
        if index_of > 0:
            layer.subselect_shape( selected[index_of-1] )

    def cycle_up(self, *args):
        try:
            layer = self.sel_manager.get_active_layer()
            selected = layer.get_selected()
        except:
            return
            
        index_of = self.get_sel_index( layer.get_subselected(), selected )
        if index_of < len(selected)-1:
            layer.subselect_shape( selected[index_of+1] )

    def get_sel_index(self, subsel, selected):
        index_of = 0
        while index_of < len(selected) \
              and selected[index_of] != subsel:
            index_of = index_of + 1

        if index_of >= len(selected):
            return -1
        else:
            return index_of

class GvSelectionManager(Signaler):

    """
    Convenient manager for view, layer, and shape selection tracking.

    The GvSelectionManager provides a single object which can be easily
    used to track changes in current view, layer, shape selection and shape
    sub-selection.  This is mainly useful because adding and removing
    callbacks to individual layers and views is a hassle.

    This class is normally accessed as "gview.app.sel_manager", and the
    object instance is normally created by the openev.py startup.  The
    object publishes the following "gvsignaler.py" style signals.  Use
    the "subscribe" method to add a callback.

    active-view-changed -- The current application view has changed (as
                           understood by openev.ViewManager).

    active-layer-changed -- The current layer of the active view (as returned
                            by GvViewArea.active_layer()) has changed, possibly
                            as a result of the current view changing.

    selection-changed -- The shape selection on the current layer (as
                         GvShapeLayer.get_selected()) has changed, possibly
                         as a result of a change of active layer or view.
                         Clearing selection, and selecting non-GvShapeLayers
                         can result in a selection-changed.

    subselection-changed -- The item within the current selection has
                            changed, possible as the result of a change in
                            selection, active layer or active view.

    """

    def __init__(self, view_manager):

        self.view_manager = view_manager
        self.view_manager.subscribe('active-view-changed',self.view_change)

        self.view = self.view_manager.get_active_view()
        if self.view is not None:
            self.view_cb_id \
                = self.view.connect('active-changed', self.layer_change)
        else:
            self.view_cb_id = None

        self.layer = None
        self.layer_selcb_id = None
        self.layer_sselcb_id = None

        self.sel_len = 0
        self.ssel = -1
        self.ssel_layer = None
        
        self.publish('active-view-changed')
        self.publish('active-layer-changed')
        self.publish('selection-changed')
        self.publish('subselection-changed')

        self.layer_change()
        
    def view_change(self, *args):
        if self.view == self.view_manager.get_active_view():
            return

        if self.view_cb_id is not None:
            self.view.disconnect(self.view_cb_id)
            self.view_cb_id = None
            
        self.view = self.view_manager.get_active_view()
        
        if self.view is not None:
            self.view_cb_id \
                = self.view.connect('active-changed', self.layer_change)
        
        self.notify('active-view-changed')
        self.layer_change()

    def get_active_view_window(self):
        """Fetch active GvViewWindow."""
        return self.view_manager.get_active_view_window()

    def get_active_view(self):
        """Fetch active GvViewArea."""
        return self.view_manager.get_active_view()

    def layer_change(self, *args):
        if self.view is None:
            new_layer = None
        else:
            new_layer = self.view.active_layer()

        if new_layer == self.layer:
            return
        
        if self.layer_selcb_id is not None:
            self.layer.disconnect(self.layer_selcb_id)
            self.layer.disconnect(self.layer_sselcb_id)
            self.layer_selcb_id = None

        self.layer = new_layer

        if self.layer is not None \
           and gvutils.is_of_class(self.layer.__class__, 'GvShapeLayer'):
            self.layer_selcb_id = \
                 self.layer.connect('selection-changed',self.sel_change)
            self.layer_sselcb_id = \
                 self.layer.connect('subselection-changed',self.ssel_change)

        self.notify('active-layer-changed')
        self.sel_change()
        self.ssel_change()

    def get_active_layer(self):
        return self.layer

    def sel_change(self,*args):
        try:
            new_len = len(self.layer.get_selected())
        except:
            new_len = 0

        if new_len == 0 and self.sel_len == 0:
            return

        self.sel_len = new_len
        self.notify('selection-changed')

    def ssel_change(self,*args):

        try:
            new_ssel = self.layer.get_subselected()
        except:
            new_ssel = -1

        if new_ssel == -1 and self.ssel == -1:
            return

        if self.ssel_layer == self.layer and new_ssel == self.ssel:
            return

        self.ssel_layer = self.layer
        self.ssel = new_ssel

        self.notify('subselection-changed')
    

pgu.gtk_register('GvSelBrowser',GvSelBrowser)
