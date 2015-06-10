##############################################################################
# $Id: layerdlg.py,v 1.33 2003/09/09 15:18:46 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  Layer Management Dialog
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
#  $Log: layerdlg.py,v $
#  Revision 1.33  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.32  2003/07/28 19:42:34  gmwalter
#  Checked in Diana's xml changes (modified to include tools), added
#  python shell xml configuration.
#
#  Revision 1.31  2003/02/20 19:27:22  gmwalter
#  Updated link tool to include Diana's ghost cursor code, and added functions
#  to allow the cursor and link mechanism to use different gcps
#  than the display for georeferencing.  Updated raster properties
#  dialog for multi-band case.  Added some signals to layerdlg.py and
#  oeattedit.py to make it easier for tools to interact with them.
#  A few random bug fixes.
#
#  Revision 1.30  2001/06/22 13:33:29  warmerda
#  fix crash when last view removed from layerdlg
#
#  Revision 1.29  2000/09/26 15:11:57  srawlin
#  changed get_selected_layer() to return the active view names as well as layer
#
#  Revision 1.28  2000/09/25 14:08:28  srawlin
#  added get_selected_layer()
#
#  Revision 1.27  2000/08/23 15:18:27  srawlin
#  changed window policy to allow resizing
#
#  Revision 1.26  2000/08/15 21:24:37  srawlin
#  fixed list_layers to work if selected_view is None
#
#  Revision 1.25  2000/08/10 15:59:29  warmerda
#  added help topic
#
#  Revision 1.24  2000/08/08 20:59:36  warmerda
#  use SELECTION_SINGLE, don't force auto-selection of active layer
#
#  Revision 1.23  2000/08/08 20:11:55  warmerda
#  don't reset active layer while updating display
#
#  Revision 1.22  2000/07/17 17:12:57  warmerda
#  register new layers for undo
#
#  Revision 1.21  2000/06/28 17:04:19  srawlin
#  dialog not visible when launched
#
#  Revision 1.20  2000/06/20 15:29:58  warmerda
#  removed debugging statement
#
#  Revision 1.19  2000/06/20 12:28:01  warmerda
#  fixed delete layer, made thumbnails optional
#
#  Revision 1.18  2000/06/19 19:20:42  warmerda
#  implemented layer creation, attempted destruction
#
#  Revision 1.17  2000/06/14 21:43:46  warmerda
#  slightly improve updating logic
#
#  Revision 1.16  2000/06/12 19:23:10  warmerda
#  signal on view changes, allow outside setting of view
#
#  Revision 1.15  2000/06/09 01:04:14  warmerda
#  added standard headers
#

from gtk import *
import gview
import os.path
import gvsignaler
import gvhtml

THUMB_W = 24
THUMB_H = 32
EYE_W = 24

# FIXME: Need a global tooltips object?
tooltips = GtkTooltips()

static_layer_dialog = None

def Launch():
    global static_layer_dialog
    
    if static_layer_dialog is None:
        static_layer_dialog = LayerDlg()

    return static_layer_dialog

class LayerDlg(GtkWindow,gvsignaler.Signaler):
    def __init__(self):
        GtkWindow.__init__(self)
        self.set_title('Layers')
        self.set_usize(250, 500)
        self.set_border_width(3)
        self.set_policy(TRUE,TRUE,FALSE)
        self.connect('delete-event',self.close)
        shell = GtkVBox(spacing=3)
        self.add(shell)
        gvhtml.set_help_topic(self, "layerdlg.html" );

        # View chooser menu
        hbox = GtkHBox(spacing=3)
        shell.pack_start(hbox, expand=FALSE)
        hbox.pack_start(GtkLabel('View:'), expand=FALSE, padding=3)
        viewopt = GtkOptionMenu()
        hbox.pack_start(viewopt)
        viewmenu = GtkMenu()
        viewopt.set_menu(viewmenu)

        # Do we want to include a thumbnail?  This is buggy on some platforms.
        if gview.get_preference('layer_thumbnail') is None \
           or gview.get_preference('layer_thumbnail') == 'off':
            self.thumbnail = FALSE
        else:
            self.thumbnail = TRUE

        self.updating = FALSE

        # Layer list
        layerbox = GtkScrolledWindow()
        shell.pack_start(layerbox)
        if self.thumbnail:
            layerlist = GtkCList(cols=3)
        else:
            layerlist = GtkCList(cols=2)
            
        layerbox.add_with_viewport(layerlist)
        layerlist.set_shadow_type(SHADOW_NONE)
        layerlist.set_selection_mode(SELECTION_SINGLE)
        layerlist.set_row_height(THUMB_H + 4)
        layerlist.set_column_width(0, EYE_W)
        if self.thumbnail:
            layerlist.set_column_width(1, THUMB_W + 4)
        layerlist.connect('select-row', self.layer_selected)
        layerlist.connect('button-press-event', self.list_clicked)

        # Option buttons
        opts = (('new.xpm', 'New layer', self.new_layer),
                ('raise.xpm', 'Raise layer', self.raise_layer),
                ('lower.xpm', 'Lower layer', self.lower_layer),
                ('delete.xpm','Delete layer', self.delete_layer))
        butbox = GtkHBox(spacing=1)
        shell.pack_start(butbox, expand=FALSE)
        for opt in opts:
            but = GtkButton()
            butbox.pack_start(but)        
            but.add(GtkPixmap(self,os.path.join(gview.home_dir,'pics',opt[0])))
            tooltips.set_tip(but, opt[1])
            but.connect('clicked', opt[2])

        self.connect('realize', self.realize)

        shell.show_all()
        self.viewopt = viewopt
        self.viewmenu = viewmenu
        self.layerlist = layerlist
        self.views = {}
        self.menuitems = {}
        self.selected_view = None

        self.eye_pixmap = \
            GtkPixmap(self,os.path.join(gview.home_dir,'pics','eye.xpm'))

        # Publish signals
        self.publish('active-view-changed')
        self.publish('deleted-layer')
        
        
    def close(self,*args):
        self.hide()
        return TRUE

    def list_layers(self):
        lst = []
        if self.selected_view is not None:
            lst = self.views[self.selected_view].list_layers()
            # Reverse the list since we want the last draw layer listed first.
            lst.reverse()
        return lst

    def add_view(self, name, view):
        # FIXME: connect to view 'destroy' event ?
        self.views[name] = view
        menuitem = GtkMenuItem(name)
        self.viewmenu.append(menuitem)
        menuitem.connect('activate', self.view_selected, name)
        menuitem.show()
        self.menuitems[name] = menuitem
        if self.viewmenu.get_active() == menuitem:
            self.viewopt.set_history(0)
            menuitem.activate()

    def remove_view(self, name):
        try:
            view = self.views[name]
            menuitem = self.menuitems[name]
        except KeyError:
            return
        self.viewmenu.remove(menuitem)
        self.viewopt.set_history(0)
        del self.views[name]
        del self.menuitems[name]
        if len(self.menuitems) > 0:
            newitem = self.viewmenu.get_active()
            newitem.activate()
            
        if len(self.views) == 0:
            # FIXME: things get kind of screwed up here...
            # there doesn't seem to be a way to tell GtkMenu/GtkOptionMenu
            # that there is nothing active.  This at least is stable...
            # Possible solution: rebuild viewmenu on each view add/remove.
            view.disconnect(self.active_change_id)
            self.selected_view = None
            self.layerlist.clear()

    def view_selected(self, item, name):
        # don't use item - view_selected() is called from gvapp with item=None
        if name == self.selected_view: return
        if self.selected_view:
            self.views[self.selected_view].disconnect(self.active_change_id)
        self.selected_view = name
        i = 0
        for x in self.viewmenu.children():
            if x == self.menuitems[name]:
                self.viewopt.set_history(i)
                break
            i = i + 1
        self.notify('active-view-changed')

        view = self.views[name]
        self.active_change_id = view.connect('active-changed',
                                             self.active_layer_changed)

        self.update_layers()
        self.active_layer_changed(view)
        
        self.notify( 'active-view-changed')

    def get_active_view(self):
        if self.selected_view:
            return self.views[self.selected_view]
        else:
            return None

    def update_layers(self,*args):
        if not self.flags() & REALIZED: return

        self.updating = TRUE
        
        lst = self.layerlist
        view = self.views[self.selected_view]
        layers = self.list_layers()

        # get active layer so we can restore after
        active = view.active_layer()
        if active is not None and active in layers:
            active_row = layers.index(active)
        else:
            active_row = None

        if self.thumbnail:
            thumbnail_mask = create_bitmap_from_data(
                self.get_window(), '\xff' * (THUMB_W/8 * THUMB_H),
                THUMB_W, THUMB_H)
            
        lst.freeze()
        lst.clear()
        
        for i in range(len(layers)):
            if self.thumbnail:
                lst.append(('', '', layers[i].get_name()))
            else:
                lst.append(('', layers[i].get_name()))
                
            if layers[i].is_visible():
                lst.set_pixmap(i, 0, self.eye_pixmap)

            if self.thumbnail:
                try:
                    thumbnail = view.create_thumbnail(layers[i],
                                                      THUMB_W, THUMB_H)
                    lst.set_pixmap(i, 1, thumbnail, thumbnail_mask)
                except:
                    pass

        # restore active layer selection
        if active_row is not None:
            lst.select_row(active_row, -1)

        lst.thaw()        
        self.updating = FALSE

    def realize(self, widget):
        if self.selected_view:
            self.update_layers()

    def active_layer_changed(self, view):
        self.update_layers()
        layers = self.list_layers()
        active = view.active_layer()
        if active is not None and active in layers:
            self.layerlist.select_row(layers.index(active), -1)
        
    def layer_selected(self, lst, row, col, event):
        if self.updating:
            return
        
        view = self.views[self.selected_view]
        layers = self.list_layers()
        view.signal_handler_block(self.active_change_id)
        view.set_active_layer(layers[row])
        view.signal_handler_unblock(self.active_change_id)

    def toggle_visibility(self, row):
        layers = self.list_layers()
        lst = self.layerlist
        if lst.get_cell_type(row, 0) == CELL_PIXMAP:
            layers[row].set_visible(FALSE)
        else:
            layers[row].set_visible(TRUE)

        self.update_layers()

    def launch_properties(self, row):
        layers = self.list_layers()
        layer = layers[row]
        layer.launch_properties()
            
    def list_clicked(self, lst, event):
        try:
            row, col = lst.get_selection_info(int(event.x), int(event.y))
        except:
            return
        
        if event.button == 1:
            if col == 0:
                lst.emit_stop_by_name('button-press-event')
                self.toggle_visibility(row)

        elif event.button == 3:
            lst.emit_stop_by_name('button-press-event')
            self.launch_properties(row)

    def new_layer(self, *args):
        if not self.selected_view:
            return
        view = self.views[self.selected_view]
        layer_list = view.list_layers()
        layer_map = {}
        for layer in layer_list:
            layer_map[layer.get_name()] = layer

        counter = 1
        name = 'UserShapes_'+str(counter)
        while layer_map.has_key(name):
            counter = counter + 1
            name = 'UserShapes_'+str(counter)
        
        shapes = gview.GvShapes(name=name)
        gview.undo_register(shapes)
        layer = gview.GvShapesLayer(shapes)
        view.add_layer(layer)
        view.set_active_layer(layer)
        

    def raise_layer(self, *args):
        if not self.selected_view: return
        view = self.views[self.selected_view]        
        layers = self.list_layers()
        row = layers.index(view.active_layer())
        index = len(layers) - row - 1
        if row == 0: return
        self.layerlist.swap_rows(row-1, row)
        view.swap_layers(index, index+1)

    def lower_layer(self, *args):
        if not self.selected_view: return
        view = self.views[self.selected_view]        
        layers = self.list_layers()
        row = layers.index(view.active_layer())
        index = len(layers) - row - 1
        if index == 0: return
        self.layerlist.swap_rows(row, row+1)
        view.swap_layers(index-1, index)

    def delete_layer(self, *args):
        if not self.selected_view: return
        view = self.views[self.selected_view]
        layer = view.active_layer()
        layername = layer.get_name()
        if layer is not None:
            view.remove_layer(layer)
            
        self.notify('deleted-layer',view,layername)
        

    def get_selected_layer(self, *args):
        """ Returns a tuple with the name of the active view and the object with the currently selected layer
            in that view.  From the layer you can get the layer name another other useful properties of the
            layer. """
        if not self.selected_view: return
        view = self.views[self.selected_view]
        return (self.selected_view, view.active_layer())
