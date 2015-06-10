#!/usr/bin/env python
###############################################################################
# $Id: pgutogglebutton.py,v 1.1 2002/08/13 16:07:17 pgs Exp $
#
# Project:  OpenEV Python GTK Utility classes
# Purpose:  Embeddable, configurable toggle widget
# Author:   Paul Spencer, pgs@magma.ca
#
###############################################################################
# Copyright (c) 2000, DM Solutions Group Inc. (www.dmsolutions.on.ca)
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
#  $Log: pgutogglebutton.py,v $
#  Revision 1.1  2002/08/13 16:07:17  pgs
#  new file
#

import gtk
from gtk import TRUE, FALSE
import gview
import os.path

class pguToggleButton(gtk.GtkToggleButton):
    """
    a widget for displaying toggled state (on/off).
    """

    def __init__(self, pix_on = "ck_on_l.xpm", pix_off = "ck_off_l.xpm"):
        """
        """
        gtk.GtkToggleButton.__init__( self )
        
        filename = os.path.join(gview.home_dir, 'pics', pix_on)
        pix, mask = gtk.create_pixmap_from_xpm(self, None, filename)
        self.pix_on = gtk.GtkPixmap( pix, mask )
        self.pix_on.show()
        
        filename = os.path.join(gview.home_dir, 'pics', pix_off)
        pix, mask = gtk.create_pixmap_from_xpm(self, None, filename)
        self.pix_off = gtk.GtkPixmap( pix, mask )
        self.pix_off.show()
        
        self.add( self.pix_off )
        
        self.active_pix = self.pix_off
        
        self.set_usize( pix.width, pix.height )
       
        self.connect( 'toggled', self.expose )
        self.connect( 'expose-event', self.expose )
        self.show()
        
    def expose( self, *args ):
        
        if not self.flags() & gtk.REALIZED:
            return
            
        
        if self.get_active():
            active_pix = self.pix_on
        else:
            active_pix = self.pix_off
        if active_pix != self.active_pix:
            self.remove( self.active_pix )
            self.active_pix = active_pix
            self.add( self.active_pix )
        
if __name__ == "__main__":
    dlg = gtk.GtkDialog()
    filename = os.path.join(gview.home_dir, 'pics')
    print 'pixs from ', filename
    tb = pguToggleButton()
    dlg.vbox.pack_start( tb )
    
    btn = gtk.GtkButton( "OK" )
    btn.connect( 'clicked', gtk.mainquit )
    dlg.action_area.pack_start( btn )
    dlg.connect( 'delete-event', gtk.mainquit )
    dlg.show_all()
    gtk.mainloop()
    