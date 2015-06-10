#!/usr/bin/env python 
###############################################################################
# $Id: Tool_autopan.py,v 1.3 2005/08/01 09:23:11 andrey_kiselev Exp $
#
# Project:  OpenEV
# Purpose:  Test for panning capabilities (an OpenEV tool).
# Author:   Gillian Walter <gillian.walter@atlantis-scientific.com>
#
# Developed by Atlantis Scientific Inc. (www.atlantis-scientific.com) for
# DRDC Ottawa
#
###############################################################################
# Copyright (c) Her majesty the Queen in right of Canada as represented
# by the Minister of National Defence, 2003.
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
#  $Log: Tool_autopan.py,v $
#  Revision 1.3  2005/08/01 09:23:11  andrey_kiselev
#  Return empty string if LD_LIBRARY_PATH/PATH environment variables are not set.
#
#  Revision 1.2  2005/02/22 13:22:39  gmwalter
#  Add autopan tool.
#
#  Revision 1.1.2.1  2005/02/18 01:27:23  gmwalter
#  Added autopan test tool.
#
#  Revision 1.9  2005/01/31 21:17:55  gwalter
#  Update autopan, fix a few gui issues.
#
#  Revision 1.8  2005/01/29 04:14:44  gwalter
#  Add trail test.
#
#  Revision 1.7  2005/01/20 20:11:42  gwalter
#  Update autopan to add path type option,
#  add secondary view to test tool.
#
#  Revision 1.6  2005/01/17 21:24:13  gwalter
#  Avoid problems when window is shut and
#  then opened again.
#
#  Revision 1.5  2005/01/17 16:36:01  gwalter
#  Updated pan test tool.
#
#  Revision 1.4  2005/01/14 15:51:18  gwalter
#  Help and autopan updates.
#
#  Revision 1.3  2004/11/25 21:17:17  gwalter
#  Updated.
#

import gviewapp
import Numeric
import gtk
import time
import gview
import gvutils
import os
import string
import gdal
import vrtutils
import pgucolorsel

class PyAutopanTool(gviewapp.Tool_GViewApp):
    def __init__(self, app=None, startpath=None):
        gviewapp.Tool_GViewApp.__init__(self,app)

        self.init_menu()
        self.view=None
        self.playing=0
        self.id=None
        self.speed = 0.01

        gtk.quit_add(0,self.quit_cb)
        
    def quit_cb(self,*args):
        self.playing = 0

    def init_menu(self):
        self.menu_entries.set_entry("Tools/PyAutopan",1,
                                    self.startpan_cb)

    def startpan_cb(self, *args):
        if self.playing == 1:
            print 'already panning- left click to stop'
            return

        for view in self.app.view_manager.view_list:
            if view.title == args[1]:
                self.app.view_manager.set_active_view(view)
                self.view = view.viewarea
                self.viewwin = view

        xmin,ymin,xmax,ymax = self.view.get_extents()
        xwidth = xmax-xmin
        ywidth = ymax-ymin
        self.id=self.viewwin.connect('button-release-event',self.stoppan_cb)
        self.playing = 1

        self.xmin,self.ymin,self.xwidth,self.ywidth=xmin,ymin,xwidth,ywidth

        self.set_speed(0.01)       
        self.view.fit_extents(self.centers[0][0],self.centers[0][1],
                              xwidth/8,ywidth/8)

        while self.playing == 1:
            self.view.set_translation(self.centers[self.idx][0],
                                      self.centers[self.idx][1])
            self.idx = self.idx+1
            if self.idx > len(self.centers)-1:
                self.idx = 0

            while gtk.events_pending():
                gtk.mainiteration()

    def set_speed(self,speed):
        self.speed = speed
        if self.speed > 0:
            self.speed = min(1.0,max(self.speed,0.000001))
        else:
            self.speed = max(-1.0,min(self.speed,-0.000001))

        self.centers=[]
        xmin,ymin,xwidth,ywidth=self.xmin,self.ymin,self.xwidth,self.ywidth
        
        for dy in Numeric.arange(ymin,ymin+ywidth,ywidth/10):
            for dx in Numeric.arange(xmin,xmin+xwidth,xwidth*speed/8):
                self.centers.append((-dx,-dy))
        if self.speed < 0:
            self.centers.reverse()
        self.idx = 0
        
    def stoppan_cb(self, *args):
        if self.playing == 0:
            return

        event=args[1]
        if event.button == 1:
        
            if self.id is not None:
                self.viewwin.disconnect(self.id)
                self.id = None

            self.playing = 0
            self.view = None
            self.viewwin = None
            self.id = None

        elif event.button == 2:
            self.speed = self.speed*1.25
            self.set_speed(self.speed)
        elif event.button == 3:
            self.speed = self.speed/1.25
            self.set_speed(self.speed)


class AutopanTool(gviewapp.Tool_GViewApp):
    def __init__(self, app=None, startpath=None):
        gviewapp.Tool_GViewApp.__init__(self,app)

        self.init_menu()
        self.view=None
        self.second_view = None
        
        self.playing=0
        self.id=None
        self.tool = gview.GvAutopanTool()
        if os.name != 'nt':
            lp = os.environ.get('LD_LIBRARY_PATH', '')
        else:
            lp = os.environ.get('PATH', '')

        if string.find(lp,'Mesa') == -1:
            self.speed = 0.001
            self.default_speed = 0.001
        else:
            self.speed = 0.01
            self.default_speed = 0.01
            
        self.active = 0
        self.dialog = None
        self.ext = None

    def init_menu(self):
        self.menu_entries.set_entry("Tools/Autopan",1,
                                    self.showgui_cb)

    def showgui_cb(self, *args):
        if self.dialog is None:
            self.dialog = gtk.GtkWindow()
            self.dialog.connect('delete-event',self.close)
            table = gtk.GtkTable(9,4)
            table.set_border_width(10)
            table.set_row_spacings(10)
            table.set_col_spacings(10)
            vbox = gtk.GtkVBox()
            self.dialog.add(vbox)
            vbox.pack_start(table)

            iconbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL,
                                      gtk.TOOLBAR_ICONS)
            
            arrows = []
            atypes = [gtk.ARROW_LEFT,gtk.ARROW_UP,
                      gtk.ARROW_DOWN,gtk.ARROW_RIGHT]

            cbs = [self.rewind_cb, self.speed_up_cb, self.speed_down_cb,
                   self.play_cb]
            for atype,cb in map(None,atypes,cbs):
                arr = gtk.GtkButton()
                arr.set_border_width(0)
                arr.set_relief(gtk.RELIEF_NONE)
                arr.add(gtk.GtkArrow(atype))
                arr.connect('clicked',cb)
                arrows.append(arr)
        
            vbox = gtk.GtkVBox(spacing=0, homogeneous=gtk.FALSE)
            vbox.pack_start(arrows[1], expand=gtk.FALSE)
            vbox.pack_start(arrows[2], expand=gtk.FALSE)
        
            # Now put them in the toolbar
            iconbar.append_widget(arrows[0], 'Rewind', 'Rewind')
            iconbar.append_widget(vbox, 'Adjust speed', 'Adjust speed')
            iconbar.append_widget(arrows[3], 'Play', 'Play')

            table.attach(iconbar,0,1,0,1)
            but = gtk.GtkButton('Stop')
            table.attach(but,1,2,0,1)
            but.connect('clicked',self.stop_pan_cb)
            
            but = gtk.GtkButton('Pause')
            table.attach(but,2,3,0,1)
            but.connect('clicked',self.pause_pan_cb)

            label = gtk.GtkLabel('Block Size Mode:')
            label.set_alignment(0,0.5)
            table.attach(label,0,1,1,2)
            self.block_size_menu = gvutils.GvOptionMenu(
         ('Relative to Pan Extents','View Coordinates','Constant Resolution'),
                self.block_mode_changed)
            table.attach(self.block_size_menu,1,3,1,2)
            
            self.block_label_list=['Block x size (0-1):',
                                  'Block x size:',
                                  'View units/Pixel:']
            self.block_label = gtk.GtkLabel(self.block_label_list[0])
            self.block_label.set_alignment(0,0.5)
            table.attach(self.block_label,0,1,2,3)
            self.block_entry = gtk.GtkEntry()
            self.block_entry.set_editable(gtk.TRUE)
            self.block_entry.set_text('0.125')
            self.block_entry.connect('leave-notify-event',
                                     self.block_size_changed)
            table.attach(self.block_entry,1,3,2,3)

            label = gtk.GtkLabel('Overlap (0-1):')
            label.set_alignment(0,0.5)
            table.attach(label,0,1,3,4)
            self.overlap_entry = gtk.GtkEntry()
            self.overlap_entry.set_editable(gtk.TRUE)
            self.overlap_entry.set_text('0.1')
            self.overlap_entry.connect('leave-notify-event',
                                     self.overlap_changed)
            table.attach(self.overlap_entry,1,3,3,4)

            label = gtk.GtkLabel('Path type:')
            label.set_alignment(0,0.5)
            table.attach(label,0,1,4,5)
            self.path_menu = gvutils.GvOptionMenu(
                           ('0','1','2','3','4'),
                self.path_changed)
            table.attach(self.path_menu,1,3,4,5)

            label = gtk.GtkLabel('Show trail:')
            label.set_alignment(0,0.5)
            table.attach(label,0,1,5,6)
            self.trail_menu = gvutils.GvOptionMenu(
                           ('No','Yes'),
                self.trail_changed)
            table.attach(self.trail_menu,1,2,5,6)
            button = gtk.GtkButton('Clear Trail')
            table.attach(button,2,3,5,6)
            button.connect('clicked', self.clear_trail)

            label = gtk.GtkLabel('Trail Color:')
            label.set_alignment(0,0.5)
            table.attach(label,0,1,6,7)

            self.trail_color = pgucolorsel.ColorControl('Trail Color',
                                                  self.trail_color_cb)
            table.attach(self.trail_color,1,3,6,7)
            self.trail_color.set_color((1.0,0.75,0.0,0.5))
            self.second_view = gview.GvViewArea()
            self.second_view.set_usize(300,300)
            
            table.attach(self.second_view,0,3,7,8)
            
            self.dialog.show_all()
            self.dialog.connect('delete-event',self.close)

        self.viewtitle = args[1]
        self.dialog.show()
        self.dialog.get_window()._raise()

    def close(self,*args):
        if self.view is not None:
            self.tool.deactivate(self.view)
        self.playing = 0
        self.active = 0
        self.view = None
        self.dialog.hide()
        return gtk.TRUE

    def path_changed(self, *args):
        path_type = int(self.path_menu.get_history())
        self.tool.set_standard_path(path_type)

    def block_mode_changed(self,*args):
        mode = self.block_size_menu.get_history()
        self.block_label.set_text(self.block_label_list[mode])
        self.block_size_changed()

    def trail_changed(self, *args):
        if self.view is None:
            return

        self.tool.set_trail_mode(self.second_view,
                                 self.trail_menu.get_history())

    def trail_color_cb(self,*args):
        if self.view is not None:
            self.tool.set_trail_color(self.second_view,
                                  self.trail_color.current_color[0],
                                  self.trail_color.current_color[1],
                                  self.trail_color.current_color[2],
                                  self.trail_color.current_color[3])


    def clear_trail(self, *args):
        self.tool.clear_trail()

    def block_size_changed(self, *args):
        if self.active == 0 or self.playing == 0:
            return
        mode = self.block_size_menu.get_history()
        defaults = [0.1, 0.1*self.ext[2], 0.1*self.ext[2]]
        try:
            xorres = abs(float(self.block_entry.get_text()))
        except:
            if mode == 0:
                msg = 'Relative block size must be a number, 0-1!'
            elif mode == 1:
                msg = 'Block size must be a number!'
            elif mode == 2:
                msg = 'Resolution must be a number!'
            gvutils.error(msg)
            xorres = defaults[mode]
            self.block_size_entry.set_text(str(xorres))

        if (mode == 0) and ((xorres < 0) or (xorres > 1)):
            msg = 'Relative block size must be a number, 0-1!'
            gvutils.error(msg)
            xorres = defaults[mode]
            self.block_size_entry.set_text(str(xorres))

        if mode < 2:
            self.tool.set_block_x_size(xorres, mode)
        else:
            self.tool.set_x_resolution(xorres)

    def overlap_changed(self,*args):
        if self.active == 0:
            return
        txt = self.overlap_entry.get_text()
        try:
            val = float(txt)
        except:
            gvutils.error('Overlap must be a number, 0 <= overlap < 1!')
            val = 0.1
            self.overlap_entry.set_text('0.1')

        if (val < 0) or (val >= 1):
            gvutils.error('Overlap must be a number, 0 <= overlap < 1!')
            val = 0.1
            self.overlap_entry.set_text('0.1')

        self.tool.set_overlap(val)
        

    def pause_pan_cb(self, *args):
        self.playing = 2
        self.tool.pause()
        
    def stop_pan_cb(self, *args):
        self.tool.pause()
        self.playing = 0
        if self.ext is not None:
            if self.view is not None:    
                self.view.fit_extents(self.ext[0],self.ext[1],
                                  self.ext[2],self.ext[3])
                self.tool.deactivate(self.view) 
            self.ext = None   
        self.view = None

    def speed_up_cb(self, *args):
        if self.active == 0:
            return
        self.speed *= 1.25
        self.tool.set_speed(self.speed)

    def speed_down_cb(self, *args):
        if self.active == 0:
            return
        self.speed /= 1.25
        self.tool.set_speed(self.speed)
    
    def rewind_cb(self, *args):
        self.speed = -1*self.default_speed
        if self.playing == 1:
            self.tool.set_speed(self.speed)
            return

        if self.playing == 2:
            self.tool.set_speed(self.speed)
            self.tool.play()
            return
        
        self.setup_playing()
        
        
    def play_cb(self, *args):
        self.speed = self.default_speed
        if self.playing == 1:
            self.tool.set_speed(self.speed)
            return

        if self.playing == 2:
            self.tool.set_speed(self.speed)
            self.tool.play()
            return
        
        self.setup_playing()

    def setup_playing(self, *args):
        if self.view is not None:
            self.tool.deactivate(self.view)
            
        for view in self.app.view_manager.view_list:
            if view.title == self.viewtitle:
                self.app.view_manager.set_active_view(view)
                self.view = view.viewarea
                self.tool.activate(self.view)
                self.tool.register_view(self.second_view,0,1,
                                        self.trail_menu.get_history())
                self.tool.set_trail_color(self.second_view,
                                  self.trail_color.current_color[0],
                                  self.trail_color.current_color[1],
                                  self.trail_color.current_color[2],
                                  self.trail_color.current_color[3])


        # update the secondary view with a background raster
        plyr = self.view.active_layer()
        rst = None
        ds = None
        try:
            rst = plyr.get_parent()
            ds = rst.get_dataset()
        except:
            llist = self.view.list_layers()
            llist.reverse()
            for plyr in llist:
                try:
                    rst = plyr.get_parent()
                    ds = rst.get_dataset()
                    break
                except:
                    pass

        if ds is None:
            gvutils.error('Error- no raster to pan over in active view!')
            return

        dtype = gdal.GetDataTypeName(ds.GetRasterBand(1).DataType)
        
        xsize = ds.RasterXSize
        ysize = ds.RasterYSize
        while (xsize > 512) and (ysize > 512):
            xsize = xsize/2
            ysize = ysize/2
            
        srcrect = [0,0,ds.RasterXSize, ds.RasterYSize]
        dstrect = [0,0,xsize,ysize]

        vrt = vrtutils.VRTDatasetConstructor(xsize,ysize)
        
        fname = ds.GetDescription()
        
        lyrs = self.second_view.list_layers()
        for lyr in lyrs:
            self.second_view.remove_layer(lyr)

        gcps = ds.GetGCPs()
        if len(gcps) > 0:
            vrt.SetGCPs(gcps,ds.GetGCPProjection(),None,
                        srcrect,dstrect)
        else:
            gt = ds.GetGeoTransform()
            if gt != (0.0,1.0,0.0,0.0,0.0,1.0):
                vrt.SetSRS(ds.GetProjection())
            vrt.SetGeoTransform(gt,srcrect,dstrect,1)
                
        for idx in range(0,plyr.sources):
            rst = plyr.get_data(idx)
            if rst is not None:
                cmin = plyr.min_get(idx)
                cmax = plyr.max_get(idx)
                srcdiff=cmax-cmin
                if abs(srcdiff) > 0.0:
                    ratio = 255/srcdiff
                else:
                    ratio = 1.0
                offset = -cmin*ratio
                
                vrt.AddSimpleBand(fname,rst.get_band_number(),dtype,
                                  srcrect,dstrect,ScaleOffset=offset,
                                  ScaleRatio = ratio)
                        
        ds2 = gview.manager.get_dataset(vrt.GetVRTString())
        raster = gview.manager.get_dataset_raster( ds2, 1 )
        options = []
        if ( ds2.RasterCount == 1 ):
            raster_layer = gview.GvRasterLayer( raster, options,
                                       rl_mode = gview.RLM_AUTO ) 
        else:
            raster_layer = gview.GvRasterLayer( raster, options,
                                       rl_mode = gview.RLM_RGBA )

            if ( raster_layer.get_mode() == gview.RLM_RGBA ):

                green_raster = gview.manager.get_dataset_raster( ds2, 2)
                raster_layer.set_source( 1, green_raster ) 
                if ( ds2.RasterCount > 2 ):
                    blue_raster = \
                              gview.manager.get_dataset_raster( ds2, 3 )
                    raster_layer.set_source( 2, blue_raster )

                if ( ds2.RasterCount > 3 ):
                    band = ds2.GetRasterBand(4)
                    if ( band.GetRasterColorInterpretation() ==
                         gdal.GCI_AlphaBand ):
                        raster_layer.blend_mode_set(
                                                gview.RL_BLEND_FILTER )
                        alpha_raster = \
                              gview.manager.get_dataset_raster( ds2, 4 )
                        raster_layer.set_source( 3, alpha_raster )
                        
        self.second_view.add_layer(raster_layer)

        self.active = 1
        xmin,ymin,xmax,ymax = self.view.get_extents()
        xwidth = xmax-xmin
        ywidth = ymax-ymin
        self.ext = (xmin,ymin,xwidth,ywidth)
        self.tool.set_extents((xmin,ymin,xwidth,ywidth))
        self.playing = 1
        self.tool.set_speed(self.speed)
        self.block_size_changed()
        self.overlap_changed()
        self.tool.play()        

TOOL_LIST = ['AutopanTool']
