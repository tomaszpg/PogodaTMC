##############################################################################
# $Id: gvogrdlg.py,v 1.5 2003/09/09 15:18:46 gmwalter Exp $
#
# Project:  OpenEV
# Purpose:  OGR Layer Selection and Loading Dialog.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2003, Frank Warmerdam <warmerdam@pobox.com>
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
#  $Log: gvogrdlg.py,v $
#  Revision 1.5  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.4  2003/01/07 14:56:02  warmerda
#  Removed print statement.
#
#  Revision 1.3  2003/01/07 03:37:53  warmerda
#  lots of upgrades
#
#  Revision 1.2  2003/01/06 22:36:47  warmerda
#  Added prototype ExecuteSQL() support
#
#  Revision 1.1  2003/01/06 21:40:19  warmerda
#  New
#
#

from gtk import *
import gview
import os.path
import gvhtml
import ogr


class GvOGRDlg(GtkWindow):
    def __init__(self, ds, viewwindow):
        GtkWindow.__init__(self)
        self.set_title('Vector Layer Selection')
        self.set_usize(500, 500)
        self.set_border_width(3)
        self.set_policy(TRUE,TRUE,FALSE)
        self.connect('delete-event',self.close)
        shell = GtkVBox(homogeneous=FALSE,spacing=3)
        self.add(shell)
        gvhtml.set_help_topic(self, "veclayerselect.html" );

        # Layer list
        layerbox = GtkScrolledWindow()
        shell.pack_start(layerbox)
        layerlist = GtkCList(cols=2)
            
        layerbox.add_with_viewport(layerlist)
        layerlist.set_shadow_type(SHADOW_NONE)
        layerlist.set_selection_mode(SELECTION_SINGLE)
        layerlist.set_row_height(30)
        layerlist.set_column_width(0, 24)
        #layerlist.connect('select-row', self.layer_selected)
        layerlist.connect('button-press-event', self.list_clicked)

        # Clip to view?

        hbox = GtkHBox(homogeneous=FALSE)
        shell.pack_start( hbox, expand=FALSE )

        self.clip_to_view_btn = GtkCheckButton()
        hbox.pack_start( self.clip_to_view_btn, expand=FALSE )

        hbox.pack_start( GtkLabel('Clip To View' ), expand=FALSE )

        # SQL Box.

        hbox = GtkHBox(homogeneous=FALSE, spacing=3)
        shell.pack_start( hbox,expand=FALSE )
        
        sql_button = GtkButton('Execute SQL:')
        sql_button.connect('clicked', self.execute_sql)
        hbox.pack_start(sql_button, expand=FALSE)
        
        self.sql_cmd = GtkEntry()
        hbox.pack_start(self.sql_cmd,expand=TRUE)

        # buttons
        button_box = GtkHButtonBox()
        button_box.set_layout_default(BUTTONBOX_START)
        ok_button = GtkButton('Accept')
        ok_button.connect('clicked', self.accept)
        loadall_button = GtkButton('Load All')
        loadall_button.connect('clicked', self.load_all)
        cancel_button = GtkButton('Cancel')
        cancel_button.connect('clicked', self.close)
        help_button = GtkButton('Help')
        help_button.connect('clicked', self.help_cb)
        button_box.pack_start(ok_button, expand=FALSE)
        button_box.pack_start(loadall_button, expand=FALSE)
        button_box.pack_start(cancel_button, expand=FALSE)
        button_box.pack_start(help_button, expand=FALSE)
        shell.pack_start(button_box,expand=FALSE)

        self.connect('realize', self.realize)

        self.sel_pixmap = \
            GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                        'ck_on_l.xpm'))
        self.not_sel_pixmap = \
            GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                        'ck_off_l.xpm'))
        
        shell.show_all()

        self.ds = ds
        self.viewwindow = viewwindow
        self.layerlist = layerlist

        layer_count = ds.GetLayerCount()
        self.layer_names = []
        self.layer_sel = []
        for i in range(layer_count):
            layer = ds.GetLayer( i )
            self.layer_names.append( layer.GetName() )
            self.layer_sel.append( 0 )

        self.show_all()

    def help_cb(self,*args):
        gvhtml.LaunchHTML( "veclayerselect.html" );
    
    def close(self,*args):
        self.ds.Destroy()
        self.hide()
        return TRUE

    def load_all(self,*args):
        for i in range(len(self.layer_sel)):
            self.layer_sel[i] = 1
        self.accept()

    def accept(self,*args):

        if self.clip_to_view_btn.get_active():
            xmin, ymin, xmax, ymax = self.viewwindow.viewarea.get_extents()

            wkt = 'POLYGON((%g %g,%g %g,%g %g,%g %g,%g %g))' % \
                   (xmin,ymax,xmax,ymax,xmax,ymin,xmin,ymin,xmin,ymax)
            rect = ogr.CreateGeometryFromWkt( wkt )
        else:
            rect = None
            
        for i in range(len(self.layer_sel)):
            if self.layer_sel[i]:
                layer = self.ds.GetLayer( i )

                if rect is not None:
                    layer.SetSpatialFilter( rect )
                    
                self.viewwindow.file_open_ogr_by_layer( layer )
                
                if rect is not None:
                    layer.SetSpatialFilter( None )

        if rect is not None:
            rect.Destroy()
            
        self.close()

    def realize(self, widget):
        lst = self.layerlist

        lst.freeze()
        lst.clear()

        i = 0
        for entry in self.layer_names:
            lst.append(('', entry))
                
            lst.set_pixmap(i, 0, self.not_sel_pixmap)

            i = i + 1

        lst.thaw()        

    def list_clicked(self, lst, event):
        row, col = lst.get_selection_info(int(event.x), int(event.y))
        lst.emit_stop_by_name('button-press-event')

        if event.type is GDK._2BUTTON_PRESS:
            for i in range(len(self.layer_sel)):
                self.layer_sel[i] = 0
                
            self.layer_sel[row] = 1
            self.accept()
        else:
            self.layer_sel[row] = not self.layer_sel[row]
        
        if self.layer_sel[row]:
            lst.set_pixmap(row, 0, self.sel_pixmap)
        else:
            lst.set_pixmap(row, 0, self.not_sel_pixmap)
        
    def execute_sql(self, *args):

        statement = self.sql_cmd.get_text()

        layer = self.ds.ExecuteSQL( statement )

        if layer is not None:
            self.viewwindow.file_open_ogr_by_layer( layer )
            
            self.ds.ReleaseResultsSet( layer )
