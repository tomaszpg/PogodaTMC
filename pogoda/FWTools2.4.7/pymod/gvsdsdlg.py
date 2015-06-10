##############################################################################
# $Id: gvsdsdlg.py,v 1.5 2008/10/21 22:00:13 warmerda Exp $
#
# Project:  OpenEV
# Purpose:  Subdataset Selection Dialog
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
#  $Log: gvsdsdlg.py,v $
#  Revision 1.5  2008/10/21 22:00:13  warmerda
#  do not reopen sds dialog after selecting an sds
#
#  Revision 1.4  2003/09/09 15:18:46  gmwalter
#  Update openev.py so that if default xml files are not present in xmlconfig
#  directory, old configuration is used.  Get rid of deprecation warnings
#  for python 2.3 by updating clist get_selection_info calls and colour
#  allocation (alloc) calls to use integers instead of floats.
#
#  Revision 1.3  2003/01/08 03:25:18  warmerda
#  avoid having any lines selected
#
#  Revision 1.2  2003/01/07 03:38:09  warmerda
#  added better on/off icons
#
#  Revision 1.1  2001/06/27 14:33:17  warmerda
#  New
#
#

from gtk import *
import gview
import os.path
import gvhtml


class GvSDSDlg(GtkWindow):
    def __init__(self, dataset, viewwindow):
        GtkWindow.__init__(self)
        self.set_title('SubDataset Selection')
        self.set_usize(400, 300)
        self.set_border_width(3)
        self.set_policy(TRUE,TRUE,FALSE)
        self.connect('delete-event',self.close)
        shell = GtkVBox(spacing=3)
        self.add(shell)
        #gvhtml.set_help_topic(self, "layerdlg.html" );

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

        # buttons
        button_box = GtkHButtonBox()
        button_box.set_layout_default(BUTTONBOX_START)
        ok_button = GtkButton('Accept')
        ok_button.connect('clicked', self.accept)
        apply_button = GtkButton('Cancel')
        apply_button.connect('clicked', self.close)
        cancel_button = GtkButton('Help')
        cancel_button.connect('clicked', self.help_cb)
        button_box.pack_start(ok_button, expand=FALSE)
        button_box.pack_start(apply_button, expand=FALSE)
        button_box.pack_start(cancel_button, expand=FALSE)
        shell.pack_start(button_box,expand=FALSE)

        self.connect('realize', self.realize)

        self.sel_pixmap = \
            GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                        'ck_on_l.xpm'))
        self.not_sel_pixmap = \
            GtkPixmap(self,os.path.join(gview.home_dir,'pics',
                                        'ck_off_l.xpm'))
        
        shell.show_all()

        self.dataset = dataset
        self.viewwindow = viewwindow
        self.layerlist = layerlist

        self.sds = dataset.GetSubDatasets()
        self.sds_sel = []
        for entry in self.sds:
            self.sds_sel.append( 0 )
            
        self.show_all()

    def help_cb(self,*args):
        pass
    
    def close(self,*args):
        self.hide()
        return TRUE

    def accept(self,*args):
        for i in range(len(self.sds_sel)):
            if self.sds_sel[i]:
                self.viewwindow.file_open_by_name( self.sds[i][0], sds_check=0)
        self.close()

    def realize(self, widget):
        lst = self.layerlist
        sds = self.sds

        lst.freeze()
        lst.clear()

        i = 0
        for entry in sds:
            lst.append(('', entry[1]))
                
            lst.set_pixmap(i, 0, self.not_sel_pixmap)

            i = i + 1

        lst.thaw()        

    def list_clicked(self, lst, event):
        #print event.type
        
        row, col = lst.get_selection_info(int(event.x), int(event.y))        
	lst.emit_stop_by_name('button-press-event')

        if event.type is GDK._2BUTTON_PRESS:
            for i in range(len(self.sds_sel)):
                self.sds_sel[i] = 0
                
            self.sds_sel[row] = 1
            self.accept()
        else:
            self.sds_sel[row] = not self.sds_sel[row]
        
        if self.sds_sel[row]:
            lst.set_pixmap(row, 0, self.sel_pixmap)
        else:
            lst.set_pixmap(row, 0, self.not_sel_pixmap)
        

