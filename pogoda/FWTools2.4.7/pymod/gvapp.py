#!/usr/bin/env python
###############################################################################
# $Id: gvapp.py,v 1.32 2000/06/15 14:55:13 srawlin Exp $
#
# Project:  OpenEV
# Purpose:  OpenEV Application Mainline
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
#  $Log: gvapp.py,v $
#  Revision 1.32  2000/06/15 14:55:13  srawlin
#  added colour support for 3D drapes
#
#  Revision 1.31  2000/06/15 14:41:48  warmerda
#  Changed fit message.
#
#  Revision 1.30  2000/06/15 13:55:29  warmerda
#  added zoomin, zoomout, seeall and 1:1 functions
#
#  Revision 1.29  2000/06/14 21:43:10  warmerda
#  added iconbar
#
#  Revision 1.28  2000/06/14 15:42:11  srawlin
#  added 3D mesh LOD setting and initial height scaling
#
#  Revision 1.27  2000/06/14 13:57:51  warmerda
#  atlfilesel is now pgufilesel
#
#  Revision 1.26  2000/06/13 22:39:14  srawlin
#  added GUI for openning 3D View.  Added Logo
#
#  Revision 1.25  2000/06/13 20:04:32  warmerda
#  updated warp_gcp label
#
#  Revision 1.24  2000/06/13 19:19:47  warmerda
#  Fixed bug with pref panel.
#
#  Revision 1.23  2000/06/13 17:20:04  warmerda
#  added cache control preferences
#
#  Revision 1.22  2000/06/13 15:32:47  warmerda
#  added file selection dialog for vectors, use atlfilesel
#
#  Revision 1.21  2000/06/12 20:16:21  warmerda
#  added shapefile write support
#
#  Revision 1.20  2000/06/12 19:22:45  warmerda
#  added ViewManager class to manage view list, and sync layerdlg/toolbox
#
#  Revision 1.19  2000/06/12 15:06:58  warmerda
#  added raster preferences
#
#  Revision 1.18  2000/06/09 01:04:14  warmerda
#  added standard headers
#

from gvsignaler import Signaler
import gtk
from gtk import FALSE, TRUE
import gtkmissing
import sys
import GtkExtra
import gview
import gvconst
import layerdlg
import gdal
import gvutils
import os
import pgufilesel
import math

class GViewApp(gtk.GtkWindow, Signaler):
    def __init__(self):
        gtk.GtkWindow.__init__(self)
        self.set_title('OpenEV')
        self.set_border_width(3)
        self.file_sel = None
        self.drape_file_sel = None
        self.DEM_file_sel = None
        shell = gtk.GtkVBox(spacing=3)
        self.add(shell)
        self.files = []
        self.pref_dialog = None
        self.view_manager = ViewManager()

        # Menu bar
        menuf = GtkExtra.MenuFactory()
        menuf.add_entries([
            ('File/Open', '<control>O', self.file_open_cb ),
            ('File/Open 3D', None, self.open_3D_request),
            ('File/Save Vector Layer', None, self.save_vector_layer_request),
            ('File/New View', None, self.new_view),
            ('File/Print', None, self.print_cb),
            ('File/Quit', None, self.quit),
            ('Edit/Undo', '<control>Z', self.undo),
            ('Edit/Layers...', None, self.show_layerdlg),
            ('Edit/Edit Toolbar...', None, self.show_toolbardlg),
            ('Edit/Preferences...', None, self.launch_preferences),
            ('Help/EVApp...', None, self.helpcb, 'evapp.html')
            ])
        self.add_accel_group(menuf.accelerator)
        shell.pack_start(menuf, expand=FALSE)

        self.create_iconbar()
        shell.pack_start(self.iconbar)

        logo = gtk.GtkPixmap(self, os.path.join(gview.home_dir,'pics','openev.xpm'))
        shell.pack_start(logo, expand=FALSE)
        
        # End of widgets
        shell.show_all()

        # Toolbar
        self.toolbar = Toolbar()
        self.view_manager.set_toolbar( self.toolbar )

        # Other dialogs, etc.
        self.layerdlg = layerdlg.Launch()
        self.view_manager.set_layerdlg(self.layerdlg)
        self.views = []

        # Trap window close event
        self.connect('delete-event', self.close)

        # Publish signals
        self.publish('quit')

    def print_cb(self, *args):
        import gvprint
        view = self.view_manager.get_active_view()
        pd = gvprint.GvPrintDialog( view )
        pd.show_all()
        
    def helpcb(self, item, topic='evapp.html'):
        import gvhtml
        gvhtml.LaunchHTML( topic )
        
    def close(self, *args):
        self.quit()
        return TRUE
        
    def quit(self, *args):
        # Save preferences
        gview.save_preferences()
        
        # Notify listeners of quit event
        self.notify('quit')

    def undo(self, *args):
        gview.undo_pop()

    def show_layerdlg(self, *args):
        self.layerdlg.show()
        self.layerdlg.get_window()._raise()

    def show_toolbardlg(self, *args):
        self.toolbar.show()
        self.toolbar.get_window()._raise()

    def new_view(self, *args):
        view = ViewWindow()
        view.connect('delete-event', self.close_view)

        self.view_manager.add_view(view)
        self.views.append(view)
        view.show()

    def close_view(self, view, *args):
        # Promote view to ViewWindow instance
        for v in self.views:
            if view == v:   # Compares gtk objects, not python instances.
                view = v
                break

        self.layerdlg.remove_view(view.title)
        self.views.remove(view)

    def save_vector_layer_request( self, *args ):
        view = self.view_manager.get_active_view()
        if view is None:
            return

        layer = view.active_layer()
        if layer is None:
            return

        if gvutils.is_of_class( layer.__class__, 'GvShapesLayer' ) == 0:
            return

        pgufilesel.SimpleFileSelect( self.save_vector_layer_with_file,
                                     cb_data = layer.get_parent(), 
                                     title = 'Shapefile To Save to',
                                     default_filename = layer.get_name() )

    def save_vector_layer_with_file( self, filename, shapes_data ):
        shapes_data.save_to( filename )

    def launch_preferences(self, *args):
        if self.pref_dialog is None:
            self.pref_dialog = PrefDialog()
            self.pref_dialog.connect('destroy', self.destroy_preferences)
        self.pref_dialog.show()
        self.pref_dialog.get_window()._raise()

    def destroy_preferences(self,*args):
        self.pref_dialog = None
        
    def file_open_shape_by_name(self, filename):
        shape_data = gview.GvShapes(shapefilename=filename)
        if shape_data is None:
            return
        
        gview.undo_register(shape_data)
        
        for view in self.views:
            layer = gview.GvShapesLayer( shape_data )
            view.viewarea.add_layer(layer)

    def file_open_cb(self, *args):
        pgufilesel.SimpleFileSelect( self.file_open_by_name, None,
                                     'File Open' )
        
    def file_open_by_name(self, filename, *args):
        if filename[len(filename)-4:] == '.shp':
            self.file_open_shape_by_name(filename)
            return
        
        if filename[len(filename)-4:] == '.SHP':
            self.file_open_shape_by_name(filename)
            return
        
        dataset = gdal.Open(filename)
        if dataset is None:
            GtkExtra.message_box('Error',
                      'Unable to open '+filename,
                      ('OK',) )
            return

        self.files.append(dataset)

        for band_index in range(1,1+min(3,dataset.RasterCount)):
            band = dataset.GetRasterBand(band_index)
            
            interp = band.GetRasterColorInterpretation()
            if interp == gdal.GCI_PaletteIndex:
                raster = gview.GvRaster(dataset=dataset,sample=gview.SMSample,
                                        real=band_index)
            else:
                raster = gview.GvRaster(dataset=dataset,real=band_index)
            
            raster.set_name(filename)
            gview.undo_register(raster)
            
            view = self.view_manager.get_active_view()
            if view is None:
                return
            
            options = []
            if gview.get_preference('gcp_warp_mode') is not None \
               and gview.get_preference('gcp_warp_mode') == 'no':
                options.append(('raw','yes'))
                
            raster_layer = gview.GvRasterLayer(raster, options)
                
            if interp == gdal.GCI_RedBand:
                raster_layer.texture_mode_set(1,(1.0,0.0,0.0,1.0))
                raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)
            elif interp == gdal.GCI_GreenBand:
                raster_layer.texture_mode_set(1,(0.0,1.0,0.0,1.0))
                raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)
            elif interp == gdal.GCI_BlueBand:
                raster_layer.texture_mode_set(1,(0.0,0.0,1.0,1.0))
                raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)
                
            view.add_layer(raster_layer)

    def create_iconbar(self):
        self.iconbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL,
                                      gtk.TOOLBAR_ICONS)

        self.add_icon_to_bar( 'openfile.xpm', None,
                              'Open and Display Raster/Vector File',
                              self.file_open_cb )

        self.add_icon_to_bar( 'print.xpm', None,
                              'Print Current View',
                              self.print_cb )

        self.add_icon_to_bar( 'nonelut.xpm', None,
                              'Revert to no Enhancement',
                              self.nonelut_cb )

        self.add_icon_to_bar( 'equalize.xpm', None,
                              'Apply Equalization Enhancement to Raster',
                              self.equalize_cb )

        self.add_icon_to_bar( 'seeall.xpm', None,
                              'Fit All Layers',
                              self.seeall_cb )

        self.add_icon_to_bar( 'onetoone.xpm', None,
                              'Zoom to 1:1 on Raster',
                              self.onetoone_cb )

        self.add_icon_to_bar( 'zoomin.xpm', None,
                              'Zoom in x2',
                              self.zoomin_cb )

        self.add_icon_to_bar( 'zoomout.xpm', None,
                              'Zoom out x2',
                              self.zoomout_cb )

        self.add_icon_to_bar( 'help.xpm', None,
                              'Launch Online Help',
                              self.helpcb )

    def add_icon_to_bar(self, filename, text, hint_text, cb ):
        full_filename = os.path.join(gview.home_dir,'pics',filename)
        pix, mask = gtk.create_pixmap_from_xpm(self,None,full_filename)
        self.iconbar.append_item(text,hint_text, hint_text,
                                 gtk.GtkPixmap(pix,mask), cb )

    def equalize_cb(self, *args):
        try:
            self.view_manager.get_active_view().active_layer().equalize()
        except:
            pass
        
    def nonelut_cb(self, *args):
        try:
            self.view_manager.get_active_view().active_layer().lut_put(None)
        except:
            pass

    def seeall_cb(self,*args):
        try:
            self.view_manager.get_active_view().fit_all_layers()
        except:
            pass
        
    def onetoone_cb(self,*args):
        try:
            view = self.view_manager.get_active_view()
            raster = view.active_layer().get_parent()
            point1 = view.inverse_map_pointer(raster.pixel_to_georef( 0, 0 ))
            point2 = view.inverse_map_pointer(raster.pixel_to_georef( 1, 1 ))
            dist = math.sqrt(math.pow((point1[0]-point2[0]),2)
                             + math.pow((point1[1]-point2[1]),2))
            factor = dist / math.sqrt(2)
            view.zoom(-1 * (math.log(factor) / math.log(2)) )
        except:
            pass
        
    def zoomin_cb(self,*args):
        try:
            self.view_manager.get_active_view().zoom(1)
        except:
            pass
        
    def zoomout_cb(self,*args):
        try:
            self.view_manager.get_active_view().zoom(-1)
        except:
            pass
        
        
    # -------- 3D File Open and Setup --------

    def open_3D_request(self, *args):
        self.drape_dataset = None
        self.DEM_dataset = None

        # Create Dialog Window
        dialog = gtk.GtkWindow()
        dialog.set_title('Open 3D')
        dialog.set_border_width(10)
        dialog.set_usize(500, 700)
        dialog.set_policy(FALSE, FALSE, TRUE)
        box = gtk.GtkVBox(homogeneous=FALSE, spacing=10)
        dialog.add(box)
        self.file_dialog_3D = dialog
        
        # Drape File Selector
        drape_label = gtk.GtkLabel('Select Drape')
        box.pack_start(drape_label)

        self.drape_fileSelectWin = gtk.GtkFileSelection()
        zsChildren = self.drape_fileSelectWin.children()[0].children() 
        for zsChild in zsChildren : zsChild.reparent(box)

        # DEM File Selector
        ruler1 = gtk.GtkHSeparator()
        box.pack_start(ruler1)
        DEM_label = gtk.GtkLabel('Select DEM')
        box.pack_start(DEM_label)

        self.DEM_fileSelectWin = gtk.GtkFileSelection()
        zsChildren = self.DEM_fileSelectWin.children()[0].children() 
        for zsChild in zsChildren : zsChild.reparent(box)

        # Mesh LOD and Height Scale
        mesh_opts = gtk.GtkHBox(homogeneous=FALSE, spacing=10)
        lod_label =  gtk.GtkLabel('Mesh Level of Detail')
        spin_adjust = gtk.GtkAdjustment(value=4, lower=0, upper=7, step_incr=1)
        self.lod_spin_button = gtk.GtkSpinButton(spin_adjust, climb_rate=1, digits=0)

        hscale_label = gtk.GtkLabel('Height Scaling Factor:')
        self.scale_value = gtk.GtkEntry(maxlen=7)
        self.scale_value.set_text('1.0')
        
        mesh_opts.pack_start(lod_label)
        mesh_opts.pack_start(self.lod_spin_button)
        mesh_opts.pack_start(hscale_label)
        mesh_opts.pack_start(self.scale_value)
        box.pack_start(mesh_opts)

        # Okay/Cancel Buttons
        buttons = gtk.GtkHBox(homogeneous=FALSE, spacing=10)
        okay = gtk.GtkButton('OK')
        okay.set_usize(64, 32)
        okay.connect('clicked', self.perform_3D_request)
        
        cancel = gtk.GtkButton('Cancel')
        cancel.set_usize(64, 32)
        cancel.connect('clicked', dialog.destroy)

        buttons.pack_end(cancel, expand=FALSE)
        buttons.pack_end(okay, expand=FALSE)
        box.pack_start(buttons, expand=FALSE)

        # Show everything but unused fileselection buttons
        dialog.show_all()
        box.children()[1].hide()  # Remove Drape Create/Delete/Rename 
        box.children()[6].hide()  # Remove Drape Ok/Cancel
        box.children()[9].hide()  # Remove DEM Create/Delete
        box.children()[14].hide() # Remove DEM Ok/Cancel
        

    def perform_3D_request(self, *args):
        """Tries to open selected files, then creates 3D Layer and switches to 3D mode"""

        # Get Data
        self.drape_dataset = self.raster_open_by_name(self.drape_fileSelectWin.get_filename())
        self.DEM_dataset = self.raster_open_by_name(self.DEM_fileSelectWin.get_filename())
        mesh_lod = self.lod_spin_button.get_value_as_int()
        hscale = float(self.scale_value.get_text())

        if (self.drape_dataset is not None) and (self.DEM_dataset is not None):
            # Get Current View & Prefs
            view = self.view_manager.get_active_view()
            if view is None:
                return

            options = []
            if gview.get_preference('_gcp_warp_mode') is not None \
               and gview.get_preference('_gcp_warp_mode') == 'no':
                options.append(('raw','yes'))

            # Set Current View to 3D Mode
            view.set_mode(gvconst.MODE_3D)
            view.height_scale(hscale)
            options.append(('mesh_lod',str(mesh_lod)))


            # For each band create layer and mesh
            for band_index in range(1,1+min(3,self.drape_dataset.RasterCount)):
                band = self.drape_dataset.GetRasterBand(band_index)
            
                interp = band.GetRasterColorInterpretation()
                
                # Create Drape Raster
                drape_raster = gview.GvRaster(dataset=self.drape_dataset, real=band_index)
                drape_raster.set_name(str(self.drape_fileSelectWin.get_filename()))
                gview.undo_register(drape_raster)

                # Create Drape Raster Layer
                drape_raster_layer = gview.GvRasterLayer(drape_raster, options)

                if interp == gdal.GCI_RedBand:
                    drape_raster_layer.texture_mode_set(1,(1.0,0.0,0.0,1.0))
                    drape_raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)
                elif interp == gdal.GCI_GreenBand:
                    drape_raster_layer.texture_mode_set(1,(0.0,1.0,0.0,1.0))
                    drape_raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)
                elif interp == gdal.GCI_BlueBand:
                    drape_raster_layer.texture_mode_set(1,(0.0,0.0,1.0,1.0))
                    drape_raster_layer.blend_mode_set(gview.RL_BLEND_ADD,1,1)

                # Add to view
                view.add_layer(drape_raster_layer)

                # Create DEM Raster and Add as Height
                DEM_raster = gview.GvRaster(dataset=self.DEM_dataset)
                DEM_raster.set_name(str(self.DEM_fileSelectWin.get_filename()))
                drape_raster_layer.add_height(DEM_raster)

            # Clean up File Dialog Window
            self.file_dialog_3D.destroy()

        
    def raster_open_by_name(self,filename):
        dataset = gdal.Open(filename)
        if dataset is None:
            GtkExtra.message_box('Error',
                                 'Unable to open '+filename,
                                 ('OK',) )
            return None
        return dataset


class Toolbar(gtk.GtkWindow):
    def __init__(self):
        gtk.GtkWindow.__init__(self)

        toolbox = gview.GvToolbox()        
        toolbox.add_tool("select", gview.GvSelectionTool())
        toolbox.add_tool("zoompan", gview.GvZoompanTool())
        toolbox.add_tool("line", gview.GvLineTool())
        toolbox.add_tool("area", gview.GvAreaTool())
        toolbox.add_tool("node", gview.GvNodeTool())
        toolbox.add_tool("point", gview.GvPointTool())
        toolbox.add_tool("pquery", gview.GvPointTool())
        toolbox.add_tool("roi", gview.GvRoiTool())
        
        toolbar = gtk.GtkToolbar(gtk.ORIENTATION_VERTICAL, gtk.TOOLBAR_TEXT)
        self.add(toolbar)
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, None,
                                     'Select', 'Selection tool',
                                     None, None, self.toggle, "select")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Zoom', 'Zoom/Pan mode',
                                     None, None, self.toggle, "zoompan")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Point Edit', 'Point editing tool',
                                     None, None, self.toggle, "point")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Point Query', 'Point query tool',
                                     None, None, self.toggle, "pquery")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Draw Line', 'Line drawing tool',
                                     None, None, self.toggle, "line")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Draw Area', 'Area drawing tool',
                                     None, None, self.toggle, "area")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,
                                     'Edit Node', 'Node edit tool',
                                     None, None, self.toggle, "node")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_RADIOBUTTON, but,                                     'Draw ROI', 'ROI drawing tool',
                                     None, None, self.toggle, "roi")
        but = toolbar.append_element(gtk.TOOLBAR_CHILD_TOGGLEBUTTON, None,
                                     'Link Views', 'Link views together',
                                     None, None, self.link)

        toolbar.show()
        self.toolbox = toolbox
        self.toolbar = toolbar
        self.link = gview.GvViewLink()
        
    def toggle(self, but, data):
        # For Point Query Tool:
        # Make the special point query layer the current layer and if there
        # isn't one, create it. 
        if data == "pquery":
            view = self.toolbox.get_view()
            if view is not None:
                layer_list = view.list_layers()
                result_layer = None
                for layer in layer_list:
                    if layer.get_property('pquery') is not None:
                        result_layer = layer

                if result_layer is None:
                    result_layer = gview.GvPqueryLayer()
                    result_layer.set_property('pquery','true')
                    view.add_layer(result_layer)

                view.set_active_layer( result_layer )
            
        self.toolbox.activate_tool(data)
        
    def link(self, but):
        but = gtk.GtkToggleButton(_obj=but)
        if (but.active):
            self.link.enable()
        else:
            self.link.disable()
            
    def add_view(self, view):
        self.toolbox.activate(view)
        self.link.register_view(view)
        
class ViewWindow(gtk.GtkWindow):
    next_viewnum = 1
    def __init__(self):
        gtk.GtkWindow.__init__(self)
        title = 'View %d' % ViewWindow.next_viewnum
        ViewWindow.next_viewnum = ViewWindow.next_viewnum + 1
        self.set_title(title)
        self.set_policy(TRUE, TRUE, FALSE)
        self.connect('destroy', self.destroy)
        shell = gtk.GtkVBox()
        self.add(shell)
        
        viewarea = gview.GvViewArea()
        viewarea.size(512, 512)
        shell.pack_start(viewarea, expand=TRUE)

        statusbar = gtk.GtkHBox()
        shell.pack_start(statusbar, expand=FALSE)
        label = gtk.GtkLabel()
        statusbar.pack_start(label, expand=FALSE, padding=3)
        tracker = gview.GvTrackTool(label)
        tracker.activate(viewarea)

        shell.show_all()
        viewarea.grab_focus()
        gtk.quit_add_destroy(1, self)

        self.viewarea = viewarea
        self.tracker = tracker
        self.title = title
        
    def destroy(self, *args):
        self.tracker.deactivate(self.viewarea)

class ViewManager(Signaler):

    def __init__(self):
        self.layerdlg = None
        self.toolbar = None
        self.active_view = None
        self.view_list = []
        self.publish( 'active-view-changed' )
        self.updating = FALSE

    def set_layerdlg(self,layerdlg):
        self.layerdlg = layerdlg
        self.layerdlg.subscribe('active-view-changed',self.layerdlg_cb)

    def layerdlg_cb(self,*args):
        self.set_active_view( self.layerdlg.get_active_view() )
        
    def set_toolbar(self,toolbar):
        self.toolbar = toolbar
        self.toolbar.toolbox.connect('activate',self.toolbar_cb)

    def toolbar_cb(self,*args):
        self.set_active_view( self.toolbar.toolbox.get_view() )

    def add_view(self, new_view ):
        self.updating = TRUE
        self.view_list.append( new_view )
        if self.toolbar is not None:
            self.toolbar.add_view(new_view.viewarea)

        if self.layerdlg is not None:
            self.layerdlg.add_view(new_view.title, new_view.viewarea)

        self.updating = FALSE
        self.set_active_view( new_view )

    def get_views(self):
        return self.view_list

    def get_active_view(self):
        if self.active_view == None:
            return None
        else:
            return self.active_view.viewarea
    
    def get_active_view_window(self):
        return self.active_view
    
    def set_active_view(self, new_view):
        if self.updating:
            return
        if new_view == self.active_view:
            return
        if self.active_view is not None \
           and new_view == self.active_view.viewarea:
            return

        for v in self.view_list:
            if v.viewarea == new_view:
                new_view = v

        self.active_view = new_view
        if new_view.get_window() is not None:
            new_view.get_window()._raise()
        self.notify('active-view-changed')

        if self.layerdlg is not None:
            self.layerdlg.view_selected( None, new_view.title )

        if self.toolbar is not None:
            self.toolbar.toolbox.activate(new_view.viewarea)
            
class PrefDialog(gtk.GtkWindow):
    def __init__(self):
        gtk.GtkWindow.__init__(self)
        self.set_title('Preferences')

        self.set_border_width(3)
        self.notebook = gtk.GtkNotebook()
        self.add( self.notebook )

        self.create_raster_prefs()
        self.create_tracking_tool_prefs()
        self.create_cache_prefs()
        
        self.show_all()

    def create_raster_prefs(self):
        
        self.ttp = gtk.GtkVBox(spacing=10)
        self.ttp.set_border_width(10)
        self.notebook.append_page( self.ttp, gtk.GtkLabel('Raster'))

        # Warp with GCPs
        box = gtk.GtkHBox(spacing=3)
        self.ttp.pack_start(box, expand=FALSE)
        box.pack_start(gtk.GtkLabel('Display Georeferenced:'),expand=FALSE)
        
        self.gcp_warp_om = \
               gvutils.GvOptionMenu(('Yes','No'), self.set_gcp_warp_mode)
        box.pack_start(self.gcp_warp_om,expand=FALSE)

        if gview.get_preference('gcp_warp_mode') is not None \
           and gview.get_preference('gcp_warp_mode') == 'no':
            self.gcp_warp_om.set_history(1)
            

    def create_cache_prefs(self):
        
        self.ttp = gtk.GtkVBox(spacing=10)
        self.ttp.set_border_width(10)
        self.notebook.append_page( self.ttp, gtk.GtkLabel('Caching'))

        # GDAL Cache
        box = gtk.GtkHBox(spacing=3)
        self.ttp.pack_start(box, expand=FALSE)
        box.pack_start(gtk.GtkLabel('GDAL Cache (bytes):'),expand=FALSE)
        
        self.gdal_cache = gtk.GtkEntry(maxlen=9)
        self.gdal_cache.connect('activate',self.gdal_cb)
        self.gdal_cache.connect('leave-notify-event',self.gdal_cb)
        box.pack_start(self.gdal_cache,expand=FALSE)

        self.gdal_cache.set_text(str(gdal.GetCacheMax()))

        # GvRaster Cache
        box = gtk.GtkHBox(spacing=3)
        self.ttp.pack_start(box, expand=FALSE)
        box.pack_start(gtk.GtkLabel('GvRaster (bytes):'),expand=FALSE)
        
        self.gvraster_cache = gtk.GtkEntry(maxlen=9)
        self.gvraster_cache.connect('activate',self.rcache_cb)
        self.gvraster_cache.connect('leave-notify-event',self.rcache_cb)
        box.pack_start(self.gvraster_cache,expand=FALSE)

        self.gvraster_cache.set_text(str(gview.raster_cache_get_max()))

    def gdal_cb(self, *args):
        value = int(self.gdal_cache.get_text())
        if value > 1000000:
            gview.set_preference( 'gdal_cache', str(value) )
            gdal.SetCacheMax( value )
        else:
            self.gdal_cache.set_text(str(gdal.GetCacheMax()))

    def rcache_cb(self, *args):
        value = int(self.gvraster_cache.get_text())
        if value > 4000000:
            gview.set_preference( 'gvraster_cache', str(value) )
            gview.raster_cache_set_max(value)
        else:
            self.gvraster_cache.set_text(str(gview.raster_cache_get_max()))

    def create_tracking_tool_prefs(self):
        self.ttp = gtk.GtkVBox(spacing=10)
        self.ttp.set_border_width(10)
        self.notebook.append_page( self.ttp, gtk.GtkLabel('Tracking Tool'))

        # Coordinate
        box = gtk.GtkHBox(spacing=3)
        self.ttp.pack_start(box, expand=FALSE)
        box.pack_start(gtk.GtkLabel('Coordinate:'),expand=FALSE)

        self.coord_om = gvutils.GvOptionMenu(
            ('Off','Raster Pixel/Line','Georeferenced','Geodetic (lat/long)'),
            self.set_coordinate_mode)
        box.pack_start(self.coord_om,expand=FALSE)

        if gview.get_preference('_coordinate_mode') is not None:
            if gview.get_preference('_coordinate_mode') == 'raster':
                self.coord_om.set_history(1)
            elif gview.get_preference('_coordinate_mode') == 'georef':
                self.coord_om.set_history(2)
            elif gview.get_preference('_coordinate_mode') == 'latlong':
                self.coord_om.set_history(3)
            else:
                self.coord_om.set_history(0)
        else:
                self.coord_om.set_history(2)
            
        # Raster Value
        box = gtk.GtkHBox(spacing=3)
        self.ttp.pack_start(box, expand=FALSE)
        box.pack_start(gtk.GtkLabel('Pixel Value:'),expand=FALSE)

        self.pixel_mode_om = \
            gvutils.GvOptionMenu(('On','Off'), self.set_pixel_mode)
        box.pack_start(self.pixel_mode_om,expand=FALSE)

        if gview.get_preference('_pixel_mode') is not None \
           and gview.get_preference('_pixel_mode') == 'off':
            self.pixel_mode_om.set_history(1)
        else:
            self.pixel_mode_om.set_history(0)

    def set_coordinate_mode(self, om):
        if self.coord_om.get_history() == 0:
            gview.set_preference( '_coordinate_mode', 'off')
        elif  self.coord_om.get_history() == 1:
            gview.set_preference( '_coordinate_mode', 'raster')
        elif  self.coord_om.get_history() == 2:
            gview.set_preference( '_coordinate_mode', 'georef')
        elif  self.coord_om.get_history() == 3:
            gview.set_preference( '_coordinate_mode', 'latlong')

    def set_pixel_mode(self, om):
        if om.get_history() == 1:
            gview.set_preference( '_pixel_mode', 'off')
        else:
            gview.set_preference( '_pixel_mode', 'on')

    def set_gcp_warp_mode(self, om):
        if om.get_history() == 1:
            gview.set_preference( 'gcp_warp_mode', 'no' )
        else:
            gview.set_preference( 'gcp_warp_mode', 'yes' )
        
if __name__ == '__main__':
    app = GViewApp()
    app.subscribe('quit',gtk.mainquit)
    app.show()
    app.new_view()

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        app.file_open_by_name(arg)
        i = i + 1
        
    gtk.mainloop()

